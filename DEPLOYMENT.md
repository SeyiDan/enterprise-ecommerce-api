# Deployment

This service ran on Azure Kubernetes Service. The infrastructure is Terraform
(`terraform/`), the workloads are plain manifests (`k8s/`), and deploys go
through GitHub Actions (`.github/workflows/deploy.yml`).

**The cluster was torn down on purpose.** Everything below is a record of it
running, captured on 2026-09-01. It cost roughly $3.30 a day against a fixed
student credit, and leaving an idle demo running to prove a point is a poor
trade. `terraform apply` rebuilds it; the lock file pins the provider versions
so it rebuilds the same.

---

## What was deployed

    AKS            2 nodes, Standard_B2ps_v2 (Arm64), Free tier control plane
    Nodes          spread across availability zones centralus-1 and centralus-2
    App            2 replicas, one per node, RollingUpdate with maxUnavailable 0
    Database       Azure Database for PostgreSQL Flexible Server, B_Standard_B1ms
    Registry       Azure Container Registry, admin disabled, pulls via managed identity
    Migrations     an alembic Job that must exit 0 before the app rolls
    Availability   PodDisruptionBudget minAvailable 1, so drains cannot take the service down

## Observed state

```
### nodes
NAME                             ARCH    ZONE          VERSION
aks-system-21038576-vmss000000   arm64   centralus-2   v1.35.7
aks-system-21038576-vmss000001   arm64   centralus-1   v1.35.7

### pods
NAME                       READY   NODE                             IMAGE
ecomapi-5dbff5848f-qg8jw   true    aks-...-vmss000000   .../ecomapi:a10e6e8
ecomapi-5dbff5848f-rl4mw   true    aks-...-vmss000001   .../ecomapi:a10e6e8

### service
NAME      TYPE           EXTERNAL-IP     PORT
ecomapi   LoadBalancer   20.84.199.162   80

### pdb
NAME      MIN AVAILABLE   ALLOWED DISRUPTIONS
ecomapi   1               1
```

One pod per node per zone. That is the basis of the availability claim, and it
is asserted on every deploy rather than assumed, because it broke silently once
(see "Defects found by deploying" below).

## Availability, measured

A pod was deleted while 120 sequential requests ran against the public IP:

```
$ kubectl delete pod ecomapi-554764f767-bdspj
$ sort results | uniq -c
    120 200
```

Zero failed requests. `maxUnavailable: 0` brings a replacement to READY before
removing anything, and the Service only routes to READY pods.

## Pipeline

Run `33551201093`, green in 1m06s, on a native `ubuntu-24.04-arm` runner:

```
job.batch/ecomapi-migrate condition met
deployment "ecomapi" successfully rolled out
live at http://20.84.199.162
{"status":"healthy","service":"E-Commerce API","version":"1.0.0"}
distinct nodes running replicas: 2
```

The pipeline fails if migrations do not exit 0, if the rollout stalls, if
`/health` does not answer through the load balancer, or if the replicas are not
on separate nodes.

## Credentials

The correct design is OIDC federation, where GitHub proves its identity per run
and nothing is stored. It requires an Azure AD app registration, and the tenant
this subscription lives in refuses one:

    az ad app create --display-name github-enterprise-ecommerce-api
    ERROR: Insufficient privileges to complete the operation.

Subscription Owner does not help, because registering an application is a
directory permission rather than an RBAC role.

So a credential had to be stored, and the design question became how much a
leaked one is worth:

| | Stored | Blast radius if leaked |
|---|---|---|
| Registry | ACR repository-scoped token | push/pull one repository in one registry |
| Cluster | ServiceAccount bound by a namespaced Role (`k8s/ci-rbac.yaml`) | redeploy this one app in `default` |
| Rejected | the cluster-admin kubeconfig `az aks get-credentials` returns | total cluster takeover, in a public repo's secrets |

Checked in both directions before use:

```
patch deployments      yes        get secrets            no
create jobs            yes        list nodes             no
                                  create rolebindings    no
```

The pipeline deploys the application but cannot read the database password it
deploys against.

## Subscription constraints encoded in the Terraform

Two things about this subscription shaped the design and would not reproduce
elsewhere, so they are documented rather than rediscovered:

- An Azure Policy named "Allowed resource deployment regions" permits only
  `westus, northcentralus, centralus, mexicocentral, canadacentral`. A variable
  validation block fails immediately instead of returning
  `403 RequestDisallowedByAzure` partway through an apply.
- Every x64 2-vCPU family has 0/0 quota, so the nodes are Arm. That single fact
  propagates all the way out to the choice of CI runner: an amd64 image reaches
  the node and dies with `exec format error`.
- ACR Tasks returns `TasksOperationsNotAllowed`, so server-side image builds are
  not available and the build happens on the runner.

## Defects found by deploying

Each of these passed every existing check. They are recorded because "the tests
were green" was true the whole time.

**1. `uvicorn` was never in `requirements.txt`.** The Dockerfile `CMD` and
`docker-compose` both invoke it. Every container this repository had ever
produced died at startup with `exec: "uvicorn": executable file not found`. The
test suite drives the app through httpx's ASGI transport in-process and never
starts a server, so 42 tests and 97% coverage passed against an image that could
not boot.

**2. `.dockerignore` did not exclude `terraform/`,** and the Dockerfile ends with
`COPY . .`. `terraform.tfstate` holds the generated Postgres password in plain
text and would have been baked into a published image layer. Caught before any
build ran. The build context also fell from 335 MB to 363 KB.

**3. The topology spread constraint silently stopped working on every rollout.**
Its `labelSelector` also matched the outgoing ReplicaSet's pods, so the scheduler
balanced new pods against pods about to be deleted, and both replicas ended up on
one node with `whenUnsatisfiable: DoNotSchedule` set and no error anywhere. The
constraint was satisfied at the moment of scheduling and meaningless a minute
later. Fixed with `matchLabelKeys: [pod-template-hash]`, which scopes the spread
to a single revision, and now asserted in CI.

## Rebuilding it

```
cd terraform
cp terraform.tfvars.example terraform.tfvars   # add your subscription id
terraform init && terraform apply

# one-time, from a machine with the Terraform outputs:
kubectl create secret generic ecomapi-secrets \
  --from-literal=DATABASE_URL="$(terraform -chdir=terraform output -raw database_url)" \
  --from-literal=SECRET_KEY="$(openssl rand -hex 32)"

# then push to main, or run k8s/deploy.sh locally
```

Tearing it down is `terraform destroy`.

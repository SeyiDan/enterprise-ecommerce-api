// The AKS cluster.
//
// "Managed Kubernetes" means Azure runs the control plane (the API server, the
// scheduler, etcd) and you run only the worker nodes. The control plane on the
// Free tier costs nothing; the nodes are ordinary VMs and are the entire bill.
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.prefix}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.prefix}-${local.suffix}"
  kubernetes_version  = var.kubernetes_version

  // Free tier: no uptime SLA on the control plane, no charge for it either.
  // Standard buys a financially-backed SLA. For a demo the SLA is worth nothing
  // and the cost is real, so Free is the right call and you should be able to
  // say why.
  sku_tier = "Free"

  default_node_pool {
    name       = "system"
    node_count = var.node_count
    vm_size    = var.node_size

    // Arm64 nodes. See the note on var.node_size: this is forced by quota, and
    // it means the container image must also be built for linux/arm64.
    os_sku = "Ubuntu"

    // Spread nodes across availability zones so the two of them do not land in
    // the same rack. Losing a node is the failure this whole design is about,
    // and two nodes in one zone share a single fault domain.
    zones = ["1", "2"]

    upgrade_settings {
      // During a node upgrade, add one extra node before draining an old one,
      // so capacity never dips below what the workload needs.
      max_surge = "1"
    }
  }

  // A system-assigned identity is created and destroyed with the cluster, so
  // there is no credential to manage and nothing to clean up afterwards.
  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    // Standard load balancer is required for availability zones, which the node
    // pool above uses.
    load_balancer_sku = "standard"
  }

  tags = local.tags
}

# E-Commerce API

A production-shaped REST API built with **FastAPI** and **PostgreSQL**: 13 endpoints across auth,
products and orders plus root and health checks, with 42 tests at 97% statement coverage.

Two things here are worth more than the feature list:

- **I audited it against myself and found a critical privilege escalation.** An anonymous
  visitor could make themselves an administrator and read another customer's email address and
  order history in **four HTTP requests**. There is a script that proves it. [Jump to it](#-security).
- **One endpoint runs ~130x faster than the naive version of itself**, 1 query instead of 1,001,
  with the benchmark published so you can re-run it. [Jump to it](#-measured-performance).

## 🛠 Tech Stack

- **Core**: FastAPI, Python 3.11
- **Database**: PostgreSQL 15, SQLAlchemy 2.0 (ORM + Core)
- **Infrastructure**: Docker, Docker Compose
- **Migrations**: Alembic
- **Quality**: pytest, 42 tests, **97% statement coverage** (`pytest --cov=app`)

## 🚀 Architectural Highlights

- **Security**: OAuth2 + JWT authentication with Role-Based Access Control, enforced through
  FastAPI dependency injection rather than checks scattered through the handlers.
- **Service Layer**: Business logic (stock validation, price snapshotting) sits in `crud/`,
  separate from the HTTP routers, which only handle request and response.
- **Performance**: Order reporting runs as a single SQL aggregate, not per-order ORM lazy loads.
- **Integrity**: Pydantic v2 validation at the boundary, Alembic-versioned schema migrations.

## 🔐 Security

I ran a security audit on my own project, fixed what it found, and wrote a regression test for
every fix. **8 findings**, each with a working proof-of-concept, a fix commit, and a test that
fails if the fix is reverted.

**The headline finding, ECOM-01 (Critical, [CWE-269](https://cwe.mitre.org/data/definitions/269.html)).**
The registration schema exposed an `is_admin` field and copied it straight into the user row.
Nothing checked it. `security/poc/poc_privesc.py` walks the full chain:

```
[1] POST /register  {"is_admin": true}  -> 201, account created as admin
[2] POST /login                         -> 200, bearer token
[3] GET  /orders/                       -> every order in the system, not just mine
[4] GET  /orders/summary                -> victim.customer@example.com, order total 4207.55
```

The point is not that a field was unvalidated. It is that admin was not cosmetic: the summary
endpoint returns every customer's email address and order total, so one missing check exposed
the whole customer table to an anonymous internet user. The script prints `VULNERABLE` before
the fix and `BLOCKED` after.

Full detail, including the other seven findings:

- [**SECURITY-AUDIT.md**](./SECURITY-AUDIT.md): all 8 findings with CWE, severity, fix commit
  and regression test. Verify any row by running its test, then `git revert` the fix and
  watching it fail. Security regression suite: `pytest -m security` (**16 tests**).
- [**docs/threat-model.md**](./docs/threat-model.md): STRIDE model with a data flow diagram
  and CVSS-scored top risks.
- [**.github/workflows/security.yml**](./.github/workflows/security.yml): CI gate running
  Semgrep, Trivy, gitleaks and pip-audit. Blocks any merge with a HIGH+ finding.

## 📊 Measured Performance

The order-reporting endpoint is a single raw SQL aggregate with a `JOIN` and `GROUP BY`. The
naive alternative, resolving each order's owner and item count with per-order lazy loads, issues
**1,001 queries** for one page of 500 orders.

**To be exact about the history:** this endpoint was written as the SQL aggregate in the first
commit. Nothing was rewritten or replaced. The N+1 version exists only inside `bench.py`, written
to measure what the ORM approach would have cost.

Reproduce with `python bench.py` (500 orders x 4 line items = 2,000 `order_items`, SQLite
in-memory, median of 15 runs):

| Approach | Queries | Median | Min | Max |
|---|---|---|---|---|
| Raw SQL aggregate | **1** | **5.42 ms** | 4.65 ms | 7.89 ms |
| Naive ORM (N+1) | **1,001** | 715.07 ms | 684.26 ms | 811.36 ms |

**99.2% fewer queries, roughly 130x faster.** The query count is the structural result and
holds on any database. The timings are hardware-dependent, and the gap widens against
PostgreSQL over a network, where 1,001 round trips cost far more than they do against
in-memory SQLite.

## 📦 Project Structure

```bash
├── app/
│   ├── api/v1/      # HTTP routers (request/response only)
│   ├── crud/        # Service layer (business logic)
│   ├── models/      # SQLAlchemy database models
│   ├── schemas/     # Pydantic validation schemas
│   └── core/        # Security, config, dependencies
├── security/poc/    # Proof-of-concept scripts for the audit findings
├── tests/           # Full integration suite
└── alembic/         # Versioned schema migrations
```

## 🚦 Setup & Usage

```bash
python -m venv .venv && .venv/Scripts/activate   # source .venv/bin/activate on Unix
pip install -r requirements.txt
pytest --cov=app                                  # 42 passed, 97% coverage
```

**Note on the `bcrypt==4.0.1` pin.** This project previously shipped no `requirements.txt`, so
a clean install resolved `bcrypt` 5.x, which removed the `__about__.__version__` attribute that
`passlib` 1.7.4 reads. `passlib` then mis-handles bcrypt's 72-byte password limit and **19 of 21
tests fail** with `ValueError: password cannot be longer than 72 bytes`. Pinning `bcrypt==4.0.1`
restores the suite. Do not unpin without replacing `passlib`.

For Docker commands and API testing guides, see [**QUICKSTART.md**](./QUICKSTART.md).

## 📖 API Documentation

Interactive documentation is available once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---
**License**: MIT

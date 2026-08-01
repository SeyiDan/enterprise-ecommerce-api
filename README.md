# E-Commerce API

Enterprise-grade RESTful API built with **FastAPI** and **PostgreSQL**. Designed for scalability, security, and performance.

## 🚀 Architectural Highlights

- **Security**: Robust OAuth2 + JWT authentication with Role-Based Access Control (RBAC).
- **Service Layer**: Decoupled business logic from HTTP routers for maximum reusability.
- **Performance**: Optimized raw SQL analytics for complex order reporting.
- **Integrity**: Strict data validation using Pydantic v2 and automated database migrations.

## 🛠 Tech Stack

- **Core**: FastAPI, Python 3.11
- **Database**: PostgreSQL 15, SQLAlchemy 2.0 (ORM + Core)
- **Infrastructure**: Docker, Docker Compose
- **Migrations**: Alembic
- **Quality**: Pytest, 42 tests, **97% statement coverage** (`pytest --cov=app`)

## 🔐 Security

This project was self-audited for security. See:

- [**SECURITY-AUDIT.md**](./SECURITY-AUDIT.md): 8 findings, each with a proof-of-concept,
  a fix commit, and a regression test (`pytest -m security`, 16 tests).
- [**docs/threat-model.md**](./docs/threat-model.md): STRIDE model with a data flow diagram
  and CVSS-scored top risks.
- [**.github/workflows/security.yml**](./.github/workflows/security.yml): a CI gate running
  Semgrep, Trivy, gitleaks, and pip-audit that blocks any merge with a HIGH+ finding.

## 📦 Project Structure

```bash
├── app/
│   ├── api/v1/      # HTTP Routers (Request/Response only)
│   ├── crud/        # Service Layer (Business Logic)
│   ├── models/      # SQLAlchemy Database Models
│   ├── schemas/     # Pydantic Validation Schemas
│   └── core/        # Security, Config, Dependencies
├── tests/           # Full Integration Suite
└── alembic/         # Versioned Schema Migrations
```

## 📊 Measured Performance

The order-reporting endpoint originally resolved each order's owner and item count with
per-order lazy loads, so one page of 500 orders issued **1,001 queries**. It now runs as a
single raw SQL aggregate with a `JOIN` and `GROUP BY`.

Reproduce with `python bench.py` (500 orders x 4 line items = 2,000 `order_items`,
SQLite in-memory, median of 15 runs):

| Approach | Queries | Median | Min | Max |
|---|---|---|---|---|
| Raw SQL aggregate | **1** | **5.42 ms** | 4.65 ms | 7.89 ms |
| Naive ORM (N+1) | **1,001** | 715.07 ms | 684.26 ms | 811.36 ms |

**99.2% reduction, roughly 130x faster.** Query count is the structural result and holds on
any database; the timings are hardware-dependent. The gap widens against PostgreSQL over a
network, where 1,001 round trips cost far more than they do against in-memory SQLite.

## 🚦 Setup & Usage

```bash
python -m venv .venv && .venv/Scripts/activate   # source .venv/bin/activate on Unix
pip install -r requirements.txt
pytest --cov=app                                  # 26 passed, 96% coverage
```

**Note on the `bcrypt==4.0.1` pin.** This project previously shipped no `requirements.txt`,
so a clean install resolved `bcrypt` 5.x, which removed the `__about__.__version__` attribute
that `passlib` 1.7.4 reads. `passlib` then mis-handles bcrypt's 72-byte password limit and
**19 of 21 tests fail** with `ValueError: password cannot be longer than 72 bytes`. Pinning
`bcrypt==4.0.1` restores the suite. Do not unpin without replacing `passlib`.

For Docker commands and API testing guides, see [**QUICKSTART.md**](./QUICKSTART.md).

## 📖 API Documentation

Live, interactive documentation is available once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---
**License**: MIT

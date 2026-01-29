# E-Commerce API

Production-ready RESTful API built with **FastAPI** and **PostgreSQL**. Designed for scalability, security, and performance.

## 🚀 Highlights

- **Security**: OAuth2 + JWT with role-based access control (RBAC).
- **Integrity**: Strict data validation using Pydantic v2.
- **Performance**: Optimized SQL queries for complex order analytics.
- **Reliability**: 100% test coverage with automated migrations.

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database  | PostgreSQL 15 |
| ORM       | SQLAlchemy 2.0 |
| Migrations| Alembic |
| Auth      | JWT + Bcrypt |
| Container | Docker |
| Testing   | Pytest |

## 📦 Project Structure

```bash
├── app/
│   ├── api/v1/      # Endpoints & Routing
│   ├── core/        # Security, Config, Dependencies
│   ├── models/      # SQLAlchemy ORM Models
│   ├── schemas/     # Pydantic v2 Schemas
│   └── db/          # Session & Engine Management
├── tests/           # Full Test Suite
└── alembic/         # Schema Migrations
```

## 🚦 Getting Started

The fastest way to run this project is via Docker:

```bash
docker-compose up --build
```

Detailed setup, credentials, and API usage guide can be found in [**QUICKSTART.md**](QUICKSTART.md).

## 📖 API Documentation

Once the server is running, access the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠 Developer Guide

### Database Migrations
```bash
# Generate migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec api alembic upgrade head
```

### Testing
```bash
# Run test suite
docker-compose exec api pytest -v
```

---
**License**: MIT

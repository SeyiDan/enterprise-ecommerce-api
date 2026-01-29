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
- **Quality**: Pytest (100% Coverage)

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

## 🚦 Setup & Usage

For local installation, Docker commands, and API testing guides, please refer to the [**QUICKSTART.md**](./QUICKSTART.md).

## 📖 API Documentation

Live, interactive documentation is available once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---
**License**: MIT

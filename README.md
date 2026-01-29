# E-Commerce API - Production-Ready Backend

A production-ready RESTful API for an e-commerce platform built with FastAPI and PostgreSQL, featuring user authentication, product catalog management, and order processing.

## Features

### Core Functionality
- **User Authentication**: OAuth2 with JWT tokens
- **Role-Based Access Control**: Admin and Customer roles
- **Product Catalog**: Full CRUD operations with SQLAlchemy ORM
- **Order Management**: Create and track orders with inventory management
- **Order Analytics**: Complex reports using raw SQL for performance optimization
- **Data Validation**: Strict schema validation with Pydantic v2
- **Database Migrations**: Alembic for schema version control

### Technical Highlights
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: ORM for database operations
- **Pydantic v2**: Data validation and settings management
- **Docker**: Containerized deployment with docker-compose
- **Pytest**: Comprehensive test suite with fixtures
- **JWT**: Secure authentication tokens
- **CORS**: Cross-origin resource sharing enabled

## Project Structure

```
enterprise-ecommerce-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── products.py      # Product CRUD endpoints
│   │       ├── orders.py        # Order management endpoints
│   │       └── router.py        # API router configuration
│   ├── core/
│   │   ├── config.py            # Application configuration
│   │   ├── security.py          # JWT and password hashing
│   │   └── dependencies.py      # Dependency injection
│   ├── db/
│   │   └── base.py              # Database session management
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── product.py           # Product model
│   │   └── order.py             # Order and OrderItem models
│   ├── schemas/
│   │   ├── user.py              # User Pydantic schemas
│   │   ├── product.py           # Product Pydantic schemas
│   │   └── order.py             # Order Pydantic schemas
│   └── main.py                  # FastAPI application entry point
├── alembic/
│   ├── versions/                # Migration scripts
│   └── env.py                   # Alembic environment configuration
├── tests/
│   ├── conftest.py              # Pytest fixtures and configuration
│   ├── test_auth.py             # Authentication tests
│   ├── test_products.py         # Product endpoint tests
│   └── test_orders.py           # Order endpoint tests
├── .env                         # Environment variables
├── .env.example                 # Environment variables template
├── docker-compose.yml           # Docker services configuration
├── Dockerfile                   # API container configuration
├── requirements.txt             # Python dependencies
└── alembic.ini                  # Alembic configuration
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (optional)

### Installation and Setup

1. **Clone or download the project:**
   ```bash
   cd enterprise-ecommerce-api
   ```

2. **Configure environment variables (optional):**
   ```bash
   # Review and modify .env file if needed
   # Default configuration works out of the box
   ```

3. **Start the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the API:**
   - API Documentation (Swagger UI): http://localhost:8000/docs
   - Alternative Documentation (ReDoc): http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

The database migrations will run automatically on startup!

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register a new user
- `POST /login` - Login and receive JWT token

### Products (`/api/v1/products`)
- `POST /` - Create product (Admin only)
- `GET /` - List all products (with pagination)
- `GET /{id}` - Get product by ID
- `PUT /{id}` - Update product (Admin only)
- `DELETE /{id}` - Delete product (Admin only)

### Orders (`/api/v1/orders`)
- `POST /` - Create a new order
- `GET /` - List user's orders (or all orders for Admin)
- `GET /{id}` - Get order details
- `GET /summary` - Get order summary report (uses raw SQL)

### Health Check
- `GET /health` - API health status

## Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "full_name": "John Doe",
    "is_admin": false
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create a Product (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock_quantity": 50,
    "category": "Electronics"
  }'
```

### 4. Create an Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

## Running Tests

### Run all tests:
```bash
docker-compose exec api pytest
```

### Run with coverage:
```bash
docker-compose exec api pytest --cov=app --cov-report=html
```

### Run specific test file:
```bash
docker-compose exec api pytest tests/test_auth.py
```

### Run tests with verbose output:
```bash
docker-compose exec api pytest -v
```

## Database Migrations

### Create a new migration:
```bash
docker-compose exec api alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
docker-compose exec api alembic upgrade head
```

### Rollback last migration:
```bash
docker-compose exec api alembic downgrade -1
```

### View migration history:
```bash
docker-compose exec api alembic history
```

## Development

### Local Development without Docker

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL locally and update .env file**

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |
| `POSTGRES_DB` | Database name | ecommerce_db |
| `DATABASE_URL` | Full database connection URL | - |
| `SECRET_KEY` | JWT secret key | (change in production) |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `DEBUG` | Debug mode | True |

## Security Considerations

### For Production Deployment:
1. **Change the SECRET_KEY** in `.env` to a strong random string
2. **Use strong database passwords**
3. **Configure CORS** appropriately in `app/main.py`
4. **Enable HTTPS** with a reverse proxy (nginx/traefik)
5. **Set DEBUG=False** in production
6. **Use environment-specific .env files**
7. **Implement rate limiting** for API endpoints
8. **Regular security updates** for dependencies

## Performance Optimization

- **Database Indexing**: Key fields are indexed (email, username, product name)
- **Connection Pooling**: SQLAlchemy connection pool configured
- **Raw SQL**: Complex order summary queries use raw SQL for better performance
- **Pagination**: All list endpoints support pagination
- **Docker Multi-stage builds**: Can be implemented for smaller images

## Troubleshooting

### Database connection issues:
```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs db
docker-compose logs api
```

### Reset database:
```bash
docker-compose down -v
docker-compose up --build
```

### Permission issues:
```bash
# On Linux/Mac, you might need to adjust file permissions
chmod +x scripts/*
```

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please create an issue in the project repository.

## Acknowledgments

- FastAPI documentation: https://fastapi.tiangolo.com/
- SQLAlchemy documentation: https://docs.sqlalchemy.org/
- Pydantic documentation: https://docs.pydantic.dev/

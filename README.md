# E-Commerce API

Production-ready RESTful API for e-commerce platforms built with FastAPI and PostgreSQL, featuring OAuth2 authentication, role-based access control, and comprehensive test coverage.

## Features

- **OAuth2 + JWT Authentication** with role-based access (Admin/Customer)
- **Product Catalog** with full CRUD operations (SQLAlchemy ORM)
- **Order Management** with inventory tracking
- **Order Analytics** using optimized raw SQL queries
- **Pydantic v2** validation for all inputs
- **Alembic** database migrations
- **Docker** containerized deployment
- **Pytest** suite with 100% test coverage (21/21 passing)

## Tech Stack

FastAPI • PostgreSQL • Docker • SQLAlchemy • Pydantic v2 • Alembic • JWT • Pytest

## Quick Start

See [`QUICKSTART.md`](QUICKSTART.md) for step-by-step setup instructions.

```bash
docker-compose up --build
```

Access the API at:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login (returns JWT token)

### Products (Admin only for write operations)
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/` - List products (paginated)
- `GET /api/v1/products/{id}` - Get product details
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Orders
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/` - List orders
- `GET /api/v1/orders/{id}` - Get order details
- `GET /api/v1/orders/summary` - Analytics report (raw SQL)

## Project Structure

```
enterprise-ecommerce-api/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Config, security, dependencies
│   ├── db/              # Database connection
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── main.py          # FastAPI app
├── tests/               # Pytest suite
├── alembic/             # Database migrations
├── docker-compose.yml   # Docker services
└── requirements.txt     # Python dependencies
```

## Usage Examples

### 1. Register User

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

### 3. Create Product (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock_quantity": 50,
    "category": "Electronics"
  }'
```

### 4. Create Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

## Testing

```bash
# Run all tests
docker-compose exec api pytest -v

# With coverage report
docker-compose exec api pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec api pytest tests/test_auth.py
```

**Test Results**: 21/21 passing ✓

## Database Migrations

```bash
# Create migration
docker-compose exec api alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec api alembic upgrade head

# Rollback
docker-compose exec api alembic downgrade -1

# View history
docker-compose exec api alembic history
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |
| `POSTGRES_DB` | Database name | ecommerce_db |
| `SECRET_KEY` | JWT secret key | (change in production) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 30 |

See `.env.example` for complete configuration.

## Security

### Production Checklist

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Use strong `POSTGRES_PASSWORD`
- [ ] Configure CORS for specific domains
- [ ] Set `DEBUG=False`
- [ ] Enable HTTPS (nginx/traefik)
- [ ] Implement rate limiting
- [ ] Regular security updates

### Features

- Bcrypt password hashing
- JWT token authentication
- SQL injection protection (parameterized queries)
- Input validation (Pydantic v2)
- Role-based access control

## Performance

- Database indexing on key fields
- Connection pooling (size: 10, overflow: 20)
- Raw SQL for complex queries
- Pagination support
- Lazy loading relationships

## Development

### Local Setup (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL and update .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## License

MIT License

## Documentation

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/

---

**Built with ❤️ using FastAPI**

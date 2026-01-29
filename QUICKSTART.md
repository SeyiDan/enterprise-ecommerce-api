# Quick Start Guide

Get the E-Commerce API running in under 5 minutes.

## 1. Start the Application

```bash
docker-compose up --build
```

Wait for PostgreSQL to initialize and migrations to run automatically.

## 2. Access the API

Open in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 3. Create Admin User

In Swagger UI, navigate to **POST /api/v1/auth/register** and execute:

```json
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "admin123456",
  "full_name": "Admin User",
  "is_admin": true
}
```

## 4. Login & Authorize

1. Navigate to **POST /api/v1/auth/login**
2. Enter credentials: `admin` / `admin123456`
3. Copy the `access_token`
4. Click **"Authorize"** button (top right)
5. Paste token and click "Authorize"

## 5. Test the API

### Create a Product (Admin)

**POST /api/v1/products/**:
```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic mouse",
  "price": 29.99,
  "stock_quantity": 100,
  "category": "Electronics"
}
```

### Create an Order

1. First, create a customer user (set `"is_admin": false`)
2. Login as customer and authorize
3. **POST /api/v1/orders/**:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

### View Analytics

Navigate to **GET /api/v1/orders/summary** to see the raw SQL analytics.

## Run Tests

```bash
docker-compose exec api pytest -v
```

Expected: 21/21 tests passing ✓

## Stop the Application

```bash
# Graceful shutdown
Ctrl+C

# Or in another terminal
docker-compose down

# Reset database
docker-compose down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change ports in `docker-compose.yml` |
| Database not ready | Wait 10-15 seconds for PostgreSQL initialization |
| Migration errors | Run `docker-compose down -v && docker-compose up --build` |

## Next Steps

- Explore all endpoints in Swagger UI
- Review test files in `tests/` directory
- Check full documentation in `README.md`

---

**You're all set! 🚀**

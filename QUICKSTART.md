# Quick Start Guide

Follow these steps to get the E-Commerce API up and running.

## 1. Launch Services
```bash
docker-compose up --build
```

## 2. Initialize Admin User
Use the **POST `/api/v1/auth/register`** endpoint in Swagger UI (http://localhost:8000/docs):

```json
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "admin123456",
  "full_name": "Admin User",
  "is_admin": true
}
```

## 3. Obtain Access Token
Authenticate via **POST `/api/v1/auth/login`**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123456"
```

Copy the `access_token` and use the **"Authorize"** button in Swagger UI to unlock protected endpoints.

## 4. Example API Operations

### Create Product (Admin Only)
```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "stock_quantity": 10}'
```

### View Order Summary (Raw SQL)
Navigate to **GET `/api/v1/orders/summary`** to view performance-optimized order reports.

## 🛠 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port Conflict | Update `8000:8000` in `docker-compose.yml` |
| DB Connection | Wait 10s for Postgres to initialize |
| Reset System | `docker-compose down -v` then restart |

---
**Happy Testing!** 🚀

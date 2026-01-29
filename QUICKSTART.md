# Quick Start Guide

## Step 1: Start the Application

Open a terminal in the project directory and run:

```bash
docker-compose up --build
```

Wait for the services to start. You should see:
- PostgreSQL database initializing
- API running migrations automatically
- FastAPI server starting on http://localhost:8000

## Step 2: Verify the API is Running

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 3: Create Your First Admin User

### Using the Swagger UI (http://localhost:8000/docs):

1. Navigate to **POST /api/v1/auth/register**
2. Click "Try it out"
3. Enter the following JSON:

```json
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "admin123456",
  "full_name": "Admin User",
  "is_admin": true
}
```

4. Click "Execute"

### Using cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "admin123456",
    "full_name": "Admin User",
    "is_admin": true
  }'
```

## Step 4: Login and Get Your Token

### Using Swagger UI:

1. Navigate to **POST /api/v1/auth/login**
2. Click "Try it out"
3. Enter:
   - username: `admin`
   - password: `admin123456`
4. Click "Execute"
5. Copy the `access_token` from the response

### Using cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123456"
```

## Step 5: Authorize in Swagger UI

1. Click the **"Authorize"** button at the top of the Swagger UI
2. Enter: `Bearer YOUR_ACCESS_TOKEN` (replace with your actual token)
3. Click "Authorize"
4. Click "Close"

Now all endpoints will include your authentication token!

## Step 6: Create Your First Product

1. Navigate to **POST /api/v1/products/**
2. Click "Try it out"
3. Enter:

```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "price": 29.99,
  "stock_quantity": 100,
  "category": "Electronics",
  "is_active": true
}
```

4. Click "Execute"

## Step 7: Create Your First Order

1. First, create a regular user (not admin) following Step 3 but with `"is_admin": false`
2. Login with that user and get a new token
3. Navigate to **POST /api/v1/orders/**
4. Enter:

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

5. Click "Execute"

## Step 8: View Order Summary (Raw SQL Demo)

Navigate to **GET /api/v1/orders/summary** and click "Execute" to see the order analytics using raw SQL queries.

## Running Tests

To run the test suite:

```bash
docker-compose exec api pytest -v
```

## Stopping the Application

Press `Ctrl+C` in the terminal where docker-compose is running, or run:

```bash
docker-compose down
```

To remove all data (reset database):

```bash
docker-compose down -v
```

## Troubleshooting

### Port already in use:
If port 8000 or 5432 is already in use, modify the ports in `docker-compose.yml`

### Database connection failed:
Wait a few more seconds - PostgreSQL takes time to initialize on first run

### Need to reset everything:
```bash
docker-compose down -v
docker-compose up --build
```

## Next Steps

- Explore all endpoints in the Swagger UI
- Check out the test files in the `tests/` directory
- Review the code structure in `app/`
- Read the full README.md for more details

Happy coding! 🚀

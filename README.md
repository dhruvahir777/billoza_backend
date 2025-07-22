# Restaurant Billing API

A FastAPI backend for a restaurant billing system.

## Features

- **User Authentication**: JWT-based authentication
- **Role-Based Access Control**: Owner, Manager, Staff roles
- **Menu Management**: CRUD operations for menu items
- **Order Management**: Create and manage orders
- **Reporting**: Sales and revenue reports
- **File Upload**: Profile and menu item images

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB with Motor async driver
- **Authentication**: JWT with Python-JOSE
- **Password Hashing**: Bcrypt
- **API Documentation**: Swagger/OpenAPI
- **Environment Variables**: python-dotenv

## Project Structure

```
backend/
│
├── app/
│   ├── api/                      # All API route definitions
│   │   ├── auth/                 # Authentication routes
│   │   │   ├── routes.py
│   │   │   └── __init__.py
│   │   ├── users/                # User-related routes (profile, menu, orders)
│   │   │   ├── routes.py
│   │   │   ├── menu.py
│   │   │   ├── orders.py
│   │   │   ├── reports.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── core/                     # Core settings and configurations
│   │   ├── config.py             # Environment, DB settings, CORS, etc.
│   │   ├── jwt.py                # JWT encode/decode utilities
│   │   ├── security.py           # Password hashing, auth utils
│   │   └── __init__.py
│   │
│   ├── db/                       # Database connection and models
│   │   ├── connection.py         # MongoDB connection
│   │   ├── models/               # MongoDB document schemas
│   │   │   ├── user.py
│   │   │   ├── menu.py
│   │   │   ├── order.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── schemas/                  # Pydantic schemas for validation
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── menu.py
│   │   ├── order.py
│   │   ├── report.py
│   │   └── __init__.py
│   │
│   ├── services/                 # Business logic layer
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── menu_service.py
│   │   ├── order_service.py
│   │   ├── report_service.py
│   │   └── __init__.py
│   │
│   ├── middleware/               # Custom middleware
│   │   ├── auth_middleware.py    # JWT validation middleware
│   │   ├── access_control.py     # User ID authorization
│   │   └── __init__.py
│   │
│   ├── utils/                    # Helper utilities (file upload, etc.)
│   │   ├── image_upload.py
│   │   ├── date_utils.py
│   │   └── __init__.py
│   │
│   └── main.py                   # FastAPI app entry point
│
├── .env                          # Environment variables (DB URI, JWT secret)
├── requirements.txt              # Python dependencies
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd restaurant-billing
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env` file:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/restaurant_db?retryWrites=true&w=majority
MONGODB_DB_NAME=restaurant_db
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## License

MIT

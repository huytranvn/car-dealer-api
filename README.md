# Satoshi Backend API

A RESTful API built with FastAPI for managing cars and user authentication.

## 🚀 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Car Management**: CRUD operations for car records
- **Database Migrations**: Alembic for database version control
- **API Documentation**: Auto-generated Swagger UI and ReDoc
- **CORS Support**: Configurable Cross-Origin Resource Sharing for frontend integration
- **Testing**: Comprehensive test suite with pytest

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- pip or pipenv

## 🛠️ Installation

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost/snorlax
SECRET_KEY=your-secret-key-change-this-in-production
CORS_ORIGINS=*
```

**Default values** (if `.env` is not provided):
- `DATABASE_URL`: `postgresql://localhost/snorlax`
- `SECRET_KEY`: `your-secret-key-change-this-in-production`
- `CORS_ORIGINS`: `*` (allows all origins)

**CORS Configuration**:
- Use `*` to allow all origins (development only)
- Use comma-separated URLs for specific origins: `http://localhost:3000,https://example.com`

### 5. Set Up PostgreSQL Database

```bash
# Create the database
createdb snorlax

# Or connect to PostgreSQL and run:
# CREATE DATABASE snorlax;
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Seed the Database (Optional)

Seed the database with an initial admin user and 20 sample cars:

```bash
python seed.py
```

This creates:
- **Admin user** with credentials:
  - Email: `admin@example.com`
  - Password: `admin@example.com`
- **20 sample cars** with realistic data including various brands (Honda, Toyota, Tesla, BMW, etc.)

⚠️ **Important**: Change the admin password after first login in production!

## 🏃 Running the Application

### Run with Python

```bash
cd src
python main.py
```

### Run with Uvicorn (Recommended for Development)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### Run in Production

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 Access the Application

Once the server is running, you can access:

- **API Base URL**: http://localhost:8000
- **Swagger UI** (Interactive API docs): http://localhost:8000/docs
- **ReDoc** (Alternative API docs): http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/ping

## 📚 API Endpoints

### Health Check
- `GET /ping` - Server liveness check

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

### Cars
- `GET /cars` - List all cars
- `POST /cars` - Create a new car
- `PUT /cars/{car_id}` - Update an existing car

For detailed API documentation, visit the Swagger UI at `/docs` after starting the server.

## 🧪 Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_cars_create.py
```

## 📁 Project Structure

```
backend/
├── db/                          # Database migrations
│   ├── versions/               # Alembic migration files
│   ├── env.py                  # Alembic environment config
│   └── script.py.mako          # Migration template
├── src/                        # Source code
│   ├── components/             # Feature modules
│   │   ├── cars/              # Car management
│   │   │   ├── endpoints/     # API endpoints
│   │   │   ├── models.py      # Database models
│   │   │   └── schemas.py     # Pydantic schemas
│   │   └── users/             # User management & auth
│   │       ├── endpoints/     # API endpoints
│   │       ├── models.py      # Database models
│   │       └── schemas.py     # Pydantic schemas
│   ├── configs/               # Configuration
│   │   ├── database.py        # Database connection
│   │   └── settings.py        # App settings
│   ├── utils/                 # Utility functions
│   │   ├── auth.py           # Authentication utilities
│   │   └── logger.py         # Logging setup
│   └── main.py               # Application entry point
├── tests/                     # Test suite
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── pytest.ini               # Pytest configuration
```

## 🗄️ Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

## 🔐 Authentication

This API uses JWT (JSON Web Tokens) for authentication:

1. Register a new user or login to receive a token
2. Include the token in the `Authorization` header for protected endpoints:
   ```
   Authorization: Bearer <your-token>
   ```

## 🛠️ Development

### Code Style

Follow PEP 8 guidelines for Python code style.

### Adding New Features

1. Create feature module in `src/components/`
2. Define database models in `models.py`
3. Define Pydantic schemas in `schemas.py`
4. Create endpoints in `endpoints/` directory
5. Register routers in `src/main.py`
6. Add tests in `tests/` directory

## 🐛 Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running: `pg_ctl status`
- Verify database exists: `psql -l`
- Check DATABASE_URL in `.env` file

### Migration Issues

- Check Alembic configuration in `alembic.ini`
- Ensure database is accessible
- Review migration files in `db/versions/`

### Import Errors

- Ensure you're in the correct directory
- Verify virtual environment is activated
- Check Python path includes the `src` directory

## 📝 License

[Add your license here]

## 👥 Contributors

[Add contributors here]

## 📧 Contact

[Add contact information here]


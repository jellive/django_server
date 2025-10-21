# Jell Server

Django REST Framework API server for Jell project.

## Features

- Django 5.1.3 with Python 3.11
- Django REST Framework with JWT authentication
- API documentation with Swagger/ReDoc (drf-spectacular)
- Health check endpoints
- CORS support
- Code quality tools (black, isort, flake8, mypy, pylint)
- Testing with pytest
- Error monitoring with Sentry (optional)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `DB_*`: Database configuration
- `SENTRY_DSN`: Optional Sentry error tracking

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Create superuser

```bash
python manage.py createsuperuser
```

### 5. Run development server

```bash
python manage.py runserver
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema**: http://localhost:8000/api/schema/

## Authentication

This API uses JWT (JSON Web Tokens) for authentication.

### Obtain token

```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use token in requests

```bash
Authorization: Bearer <access_token>
```

### Refresh token

```bash
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}
```

## Endpoints

- `/admin/` - Django admin interface
- `/api/post/` - Post CRUD operations
- `/api/token/` - Obtain JWT token
- `/api/token/refresh/` - Refresh JWT token
- `/api/token/verify/` - Verify JWT token
- `/api/docs/` - Swagger UI documentation
- `/api/redoc/` - ReDoc documentation
- `/health/` - Health check endpoint

## Development Tools

### Code formatting

```bash
# Format code with black
black .

# Sort imports with isort
isort .
```

### Linting

```bash
# Run flake8
flake8

# Run pylint
pylint jellserver/

# Type checking with mypy
mypy .
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Django Extensions

```bash
# Enhanced shell with IPython
python manage.py shell_plus

# Show URLs
python manage.py show_urls

# Generate secret key
python manage.py generate_secret_key
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure proper `ALLOWED_HOSTS`
3. Set up proper database (MySQL/PostgreSQL)
4. Configure static files serving
5. Use gunicorn or uwsgi for WSGI server
6. Set up HTTPS with proper certificates
7. Configure Sentry for error monitoring

## Security Features

- JWT authentication
- CORS configuration
- Rate limiting ready (django-ratelimit)
- Security headers
- HTTPS enforcement in production
- XSS protection
- CSRF protection

## License

Proprietary

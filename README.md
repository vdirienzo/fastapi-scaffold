# FastAPI Project - Production-Ready Template

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> Modern, production-ready FastAPI project template with async support, authentication, Docker, and comprehensive testing.

## ✨ Features

- 🚀 **FastAPI** - Modern, fast web framework
- 🔒 **JWT Authentication** - Secure user authentication with refresh tokens
- 🗄️ **SQLModel** - Async ORM with type safety
- 🐳 **Docker** - Multi-stage builds for production
- 🧪 **Testing** - Comprehensive test suite with pytest
- 📊 **Logging** - Structured logging with loguru
- 🔐 **Security** - Bandit, Safety, and pre-commit hooks
- 📝 **API Docs** - Auto-generated with Swagger UI and ReDoc
- ⚡ **Redis** - Caching and queue support
- 🔄 **CI/CD** - GitHub Actions workflow

## 🏗️ Project Structure

```
fastapi-project/
├── src/
│   └── fastapi_project/
│       ├── routes/          # API endpoints
│       ├── models/          # SQLModel schemas
│       ├── services/        # Business logic
│       ├── utils/           # Helper functions
│       ├── config.py        # Settings with pydantic
│       ├── database.py      # DB connection
│       ├── dependencies.py  # FastAPI dependencies
│       ├── exceptions.py    # Custom exceptions
│       └── main.py          # Application entry point
├── tests/
│   ├── test_routes/         # Route tests
│   ├── test_services/       # Service tests
│   └── conftest.py          # Pytest fixtures
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── Dockerfile               # Production Docker image
├── docker-compose.yml       # Local development services
├── pyproject.toml           # Project dependencies
├── .env.example             # Environment variables template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Docker & Docker Compose (optional)

### Installation

1. **Clone and setup**

```bash
git clone <your-repo-url>
cd fastapi-project
```

2. **Install dependencies**

```bash
# With uv (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"
```

3. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Setup pre-commit hooks**

```bash
uv run pre-commit install
```

### Running the Application

#### Local Development

```bash
# Start database services
docker-compose up -d db redis

# Run the application
uv run uvicorn fastapi_project.main:app --reload

# Or using python directly
uv run python -m fastapi_project.main
```

API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000/api/v1

#### Docker Compose

```bash
# Start all services
docker-compose up

# Start with pgAdmin
docker-compose --profile tools up
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific tests
uv run pytest tests/test_routes/test_users.py -v

# Run only integration tests
uv run pytest -m integration
```

## 📋 API Endpoints

### Health

- `GET /api/v1/health` - Health check
- `GET /api/v1/health/ready` - Readiness probe
- `GET /api/v1/health/live` - Liveness probe

### Authentication

- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/logout` - Logout

### Users

- `POST /api/v1/users` - Create user (public)
- `GET /api/v1/users/me` - Get current user
- `PATCH /api/v1/users/me` - Update current user
- `GET /api/v1/users/{id}` - Get user by ID (authenticated)
- `PATCH /api/v1/users/{id}` - Update user (superuser)
- `DELETE /api/v1/users/{id}` - Delete user (superuser)

## 🔐 Security

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one digit

### Security Scanning

```bash
# Run security checks
uv run bandit -r src/
uv run safety check

# All pre-commit hooks (includes security)
uv run pre-commit run --all-files
```

## 🛠️ Development

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check --fix .

# Type checking
uv run mypy src/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🐳 Docker

### Build Image

```bash
docker build -t fastapi-project:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://... \
  -e SECRET_KEY=your-secret-key \
  fastapi-project:latest
```

## 📊 Monitoring

### Health Checks

The application provides three health check endpoints:

- `/health` - Basic health status
- `/health/ready` - Readiness (dependencies available)
- `/health/live` - Liveness (application running)

### Logs

Logs are written to:
- Console (stderr) - Colored, human-readable
- `logs/app_YYYY-MM-DD.log` - All logs
- `logs/errors_YYYY-MM-DD.log` - Error logs only

## 🔧 Configuration

All configuration is done via environment variables. See `.env.example` for all available options.

Key configurations:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment (dev/staging/prod) | `dev` |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `REDIS_URL` | Redis connection string | Required |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🚢 Deployment

### Environment Setup

1. Set `ENVIRONMENT=prod`
2. Set `DEBUG=false`
3. Use strong `SECRET_KEY` (32+ random characters)
4. Configure production `DATABASE_URL`
5. Set up proper logging and monitoring

### Production Checklist

- [ ] Change `SECRET_KEY` to random secure value
- [ ] Configure production database
- [ ] Set up Redis for caching
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS for production domains
- [ ] Set up monitoring (Sentry, Datadog, etc.)
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Review security settings

## 📚 Documentation

- **OpenAPI Spec**: Available at `/openapi.json`
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Changelog

### [0.1.0] - 2025-01-04

#### Added
- Initial project setup with FastAPI
- User authentication with JWT
- Complete CRUD for users
- Docker and docker-compose configuration
- GitHub Actions CI/CD pipeline
- Comprehensive test suite
- Security scanning with Bandit
- Pre-commit hooks
- Health check endpoints
- Structured logging with loguru
- API documentation with Swagger UI

## 📄 License

MIT License - see LICENSE file for details

## Autor

Homero Thompson del Lago del Terror

---

**Built with ❤️ using FastAPI, SQLModel, and modern Python practices**

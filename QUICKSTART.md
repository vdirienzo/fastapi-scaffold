# Quick Start Guide

Get your FastAPI application running in **5 minutes** ⚡

## Option 1: Automated Setup (Recommended)

```bash
./setup.sh
```

This will:
- Install all dependencies with uv
- Create `.env` file from template
- Setup pre-commit hooks
- Initialize git repository

## Option 2: Manual Setup

### Step 1: Install Dependencies

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync --all-extras
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit with your values
nano .env
```

**Minimum required changes in `.env`**:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db
SECRET_KEY=your-super-secret-key-min-32-characters
```

### Step 3: Start Services

```bash
# Start PostgreSQL and Redis with Docker
docker-compose up -d db redis

# Or start all services including the app
docker-compose up
```

### Step 4: Run the Application

```bash
# Development mode (with auto-reload)
uv run uvicorn fastapi_project.main:app --reload

# Or using make
make run
```

## Verify Installation

### 1. Check Health

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Access API Docs

Open in browser: http://localhost:8000/docs

### 3. Run Tests

```bash
make test

# Or with coverage
make test-cov
```

## Create Your First User

### Via API Docs (Swagger UI)

1. Go to http://localhost:8000/docs
2. Click on `POST /api/v1/users`
3. Click "Try it out"
4. Enter user data:
   ```json
   {
     "email": "user@example.com",
     "username": "myuser",
     "password": "SecurePass123",
     "full_name": "My Name"
   }
   ```
5. Click "Execute"

### Via curl

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "myuser",
    "password": "SecurePass123",
    "full_name": "My Name"
  }'
```

### Via httpie (if installed)

```bash
http POST http://localhost:8000/api/v1/users \
  email=user@example.com \
  username=myuser \
  password=SecurePass123 \
  full_name="My Name"
```

## Login and Get Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## Use Authenticated Endpoints

```bash
# Get current user info
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Common Commands

```bash
# Show all available commands
make help

# Run linting
make lint

# Format code
make format

# Run security checks
make security

# Run all quality checks
make quality

# View logs (Docker)
make docker-logs

# Stop services
make docker-down

# Clean up
make clean
```

## Troubleshooting

### Database Connection Failed

**Problem**: Can't connect to PostgreSQL

**Solution**:
```bash
# Check if services are running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Port Already in Use

**Problem**: Port 8000 already in use

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uv run uvicorn fastapi_project.main:app --reload --port 8001
```

### Tests Failing

**Problem**: Tests fail with database errors

**Solution**:
```bash
# Make sure test database is configured
export DATABASE_URL=sqlite+aiosqlite:///:memory:

# Run tests
make test
```

### Pre-commit Hooks Failing

**Problem**: Pre-commit hooks fail on commit

**Solution**:
```bash
# Run hooks manually to see errors
make pre-commit

# Fix issues and try again
make lint-fix
make format
git add .
git commit -m "fix: your message"
```

## Next Steps

1. **Read the documentation**:
   - [README.md](README.md) - Full documentation
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   
2. **Customize the project**:
   - Add your models in `src/fastapi_project/models/`
   - Add your routes in `src/fastapi_project/routes/`
   - Add your business logic in `src/fastapi_project/services/`

3. **Write tests**:
   - Add tests in `tests/test_routes/`
   - Add tests in `tests/test_services/`

4. **Deploy**:
   - Build Docker image: `make docker-build`
   - Deploy to your cloud provider
   - Set up CI/CD with GitHub Actions

## Tips for Development

### Hot Reload

When running with `--reload`, the server automatically restarts when you change code.

### Database Migrations

```bash
# Create migration after model changes
make migrate-create

# Apply migrations
make migrate
```

### Interactive Python Shell

```bash
# Open IPython with app context
make shell

# Test things interactively
>>> from fastapi_project.models.user import User
>>> # Play around
```

### Database Shell

```bash
# Open PostgreSQL shell
make db-shell

# Run SQL queries
fastapi_db=# SELECT * FROM users;
```

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Pydantic Docs**: https://docs.pydantic.dev
- **uv Docs**: https://docs.astral.sh/uv

---

**Happy coding! 🎉**

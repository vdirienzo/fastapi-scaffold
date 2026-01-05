.PHONY: help install dev test lint format security clean run docker-up docker-down

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo '$(BLUE)FastAPI Project - Available Commands$(NC)'
	@echo ''
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo '$(BLUE)Installing dependencies...$(NC)'
	uv sync

dev: ## Install dev dependencies
	@echo '$(BLUE)Installing dev dependencies...$(NC)'
	uv sync --all-extras

setup: dev ## Setup development environment
	@echo '$(BLUE)Setting up development environment...$(NC)'
	cp -n .env.example .env || true
	uv run pre-commit install
	@echo '$(GREEN)✓ Setup complete!$(NC)'
	@echo '$(YELLOW)→ Edit .env file with your configuration$(NC)'

run: ## Run development server
	@echo '$(BLUE)Starting development server...$(NC)'
	uv run uvicorn fastapi_project.main:app --reload

test: ## Run tests
	@echo '$(BLUE)Running tests...$(NC)'
	uv run pytest -v

test-cov: ## Run tests with coverage
	@echo '$(BLUE)Running tests with coverage...$(NC)'
	uv run pytest --cov=src --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	@echo '$(BLUE)Running tests in watch mode...$(NC)'
	uv run pytest-watch

lint: ## Run linting
	@echo '$(BLUE)Running linter...$(NC)'
	uv run ruff check .

lint-fix: ## Run linting with auto-fix
	@echo '$(BLUE)Running linter with auto-fix...$(NC)'
	uv run ruff check --fix .

format: ## Format code
	@echo '$(BLUE)Formatting code...$(NC)'
	uv run ruff format .

typecheck: ## Run type checking
	@echo '$(BLUE)Running type checker...$(NC)'
	uv run mypy src/

security: ## Run security checks
	@echo '$(BLUE)Running security checks...$(NC)'
	uv run bandit -r src/
	uv run safety check || true

quality: lint typecheck security ## Run all quality checks
	@echo '$(GREEN)✓ All quality checks passed!$(NC)'

pre-commit: ## Run pre-commit hooks
	@echo '$(BLUE)Running pre-commit hooks...$(NC)'
	uv run pre-commit run --all-files

docker-build: ## Build Docker image
	@echo '$(BLUE)Building Docker image...$(NC)'
	docker build -t fastapi-project:latest .

docker-up: ## Start all services with docker-compose
	@echo '$(BLUE)Starting Docker services...$(NC)'
	docker-compose up -d
	@echo '$(GREEN)✓ Services started!$(NC)'
	@echo '$(YELLOW)→ API: http://localhost:8000$(NC)'
	@echo '$(YELLOW)→ Docs: http://localhost:8000/docs$(NC)'

docker-down: ## Stop all services
	@echo '$(BLUE)Stopping Docker services...$(NC)'
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-clean: ## Clean Docker resources
	@echo '$(BLUE)Cleaning Docker resources...$(NC)'
	docker-compose down -v
	docker system prune -f

migrate: ## Run database migrations
	@echo '$(BLUE)Running migrations...$(NC)'
	alembic upgrade head

migrate-create: ## Create new migration
	@echo '$(BLUE)Creating new migration...$(NC)'
	@read -p "Migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

clean: ## Clean generated files
	@echo '$(BLUE)Cleaning generated files...$(NC)'
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo '$(GREEN)✓ Cleanup complete!$(NC)'

shell: ## Open Python shell with app context
	@echo '$(BLUE)Opening Python shell...$(NC)'
	uv run ipython

db-shell: ## Open database shell
	@echo '$(BLUE)Opening database shell...$(NC)'
	docker-compose exec db psql -U postgres -d fastapi_db

.DEFAULT_GOAL := help

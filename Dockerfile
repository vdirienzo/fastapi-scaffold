# ==========================================
# Build stage
# ==========================================
FROM python:3.12-slim as builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
# If you have uv.lock, copy it
# COPY uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# ==========================================
# Production stage
# ==========================================
FROM python:3.12-slim

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Copy application code
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser pyproject.toml ./

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    ENVIRONMENT=prod \
    DEBUG=false

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health').read()"

# Run the application
CMD ["uvicorn", "fastapi_project.main:app", "--host", "0.0.0.0", "--port", "8000"]

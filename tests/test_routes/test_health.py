#!/usr/bin/env python3
"""
test_health.py - Tests for health check endpoints

Autor: Homero Thompson del Lago del Terror
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient):
    """Test readiness check endpoint."""
    response = await client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.asyncio
async def test_liveness_check(client: AsyncClient):
    """Test liveness check endpoint."""
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

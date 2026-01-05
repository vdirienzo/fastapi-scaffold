#!/usr/bin/env python3
"""
test_auth.py - Tests for authentication endpoints

Autor: Homero Thompson del Lago del Terror
"""

import pytest
from httpx import AsyncClient

from fastapi_project.models.user import User


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User):
    """Test successful login."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "TestPass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """Test login with wrong password fails."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "WrongPassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "Incorrect username or password" in data["detail"]


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent user fails."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "Password123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    """Test logout endpoint."""
    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert "logged out" in data["message"]

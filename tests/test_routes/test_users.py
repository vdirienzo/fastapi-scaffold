#!/usr/bin/env python3
"""
test_users.py - Tests for user endpoints

Autor: Homero Thompson del Lago del Terror
"""

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_project.models.user import User


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "SecurePass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_create_user_duplicate_username(client: AsyncClient, test_user: User):
    """Test creating user with duplicate username fails."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "different@example.com",
            "username": test_user.username,
            "password": "SecurePass123",
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert "already exists" in data["message"]


@pytest.mark.asyncio
async def test_create_user_weak_password(client: AsyncClient):
    """Test creating user with weak password fails."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "user@example.com",
            "username": "username",
            "password": "weak",  # Too short
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user: User, test_user_token: str):
    """Test getting current user info."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_get_user_by_id(
    client: AsyncClient, test_user: User, test_user_token: str
):
    """Test getting user by ID."""
    response = await client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id


@pytest.mark.asyncio
async def test_get_user_unauthorized(client: AsyncClient, test_user: User):
    """Test getting user without authentication fails."""
    response = await client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_current_user(
    client: AsyncClient, test_user: User, test_user_token: str
):
    """Test updating current user."""
    response = await client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_user_as_superuser(
    client: AsyncClient,
    test_user: User,
    test_superuser_token: str,
):
    """Test deleting user as superuser."""
    response = await client.delete(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {test_superuser_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_as_regular_user_fails(
    client: AsyncClient,
    test_superuser: User,
    test_user_token: str,
):
    """Test regular user cannot delete other users."""
    response = await client.delete(
        f"/api/v1/users/{test_superuser.id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 403

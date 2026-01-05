#!/usr/bin/env python3
"""
conftest.py - Pytest configuration and fixtures

Autor: Homero Thompson del Lago del Terror
"""

import pytest
from collections.abc import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from fastapi_project.main import app
from fastapi_project.database import get_session
from fastapi_project.models.user import User
from fastapi_project.services.user_service import UserService


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client."""

    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(session: AsyncSession) -> User:
    """Create a test user."""
    service = UserService(session)
    from fastapi_project.models.user import UserCreate

    user = await service.create(
        UserCreate(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            password="TestPass123",
        )
    )
    return user


@pytest.fixture
async def test_superuser(session: AsyncSession) -> User:
    """Create a test superuser."""
    service = UserService(session)
    from fastapi_project.models.user import UserCreate

    user = await service.create(
        UserCreate(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            password="AdminPass123",
        )
    )
    user.is_superuser = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user: User) -> str:
    """Get auth token for test user."""
    from fastapi_project.dependencies import create_access_token

    token_data = {"user_id": test_user.id, "username": test_user.username}
    return create_access_token(token_data)


@pytest.fixture
def test_superuser_token(test_superuser: User) -> str:
    """Get auth token for test superuser."""
    from fastapi_project.dependencies import create_access_token

    token_data = {"user_id": test_superuser.id, "username": test_superuser.username}
    return create_access_token(token_data)

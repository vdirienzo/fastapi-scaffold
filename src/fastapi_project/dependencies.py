#!/usr/bin/env python3
"""
dependencies.py - FastAPI dependencies for authentication and DI

Autor: Homero Thompson del Lago del Terror
"""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings
from .database import get_session
from .exceptions import AuthenticationError
from .models.user import TokenData, User
from .services.user_service import UserService


security = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> TokenData:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: int | None = payload.get("user_id")
        username: str | None = payload.get("username")
        if user_id is None or username is None:
            raise AuthenticationError("Invalid token payload")
        return TokenData(user_id=user_id, username=username)
    except JWTError as e:
        raise AuthenticationError(f"Invalid token: {e}") from e


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    """Dependency for UserService."""
    return UserService(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Dependency to get the current authenticated user."""
    token = credentials.credentials
    token_data = decode_token(token)

    user = await user_service.get_by_id(token_data.user_id)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to get current user if they are a superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


# Type aliases for cleaner annotations
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSuperUser = Annotated[User, Depends(get_current_active_superuser)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

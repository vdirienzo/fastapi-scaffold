#!/usr/bin/env python3
"""
auth.py - Authentication endpoints

Autor: Homero Thompson del Lago del Terror
"""

from fastapi import APIRouter, status, HTTPException
from loguru import logger

from ..dependencies import UserServiceDep, create_access_token, create_refresh_token
from ..models.user import Token, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(credentials: UserLogin, user_service: UserServiceDep) -> Token:
    """Authenticate user and return JWT tokens."""
    user = await user_service.authenticate(
        credentials.username, credentials.password
    )

    if not user:
        logger.warning(f"Failed login attempt for username: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    token_data = {"user_id": user.id, "username": user.username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    logger.info(f"User {user.username} logged in successfully")

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout() -> dict[str, str]:
    """Logout endpoint (client should delete tokens)."""
    # TODO: Implement token blacklisting if needed
    return {"message": "Successfully logged out"}

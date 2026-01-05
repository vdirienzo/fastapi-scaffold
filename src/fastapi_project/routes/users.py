#!/usr/bin/env python3
"""
users.py - User CRUD endpoints

Autor: Homero Thompson del Lago del Terror
"""

from fastapi import APIRouter, status
from loguru import logger

from ..dependencies import CurrentUser, CurrentSuperUser, UserServiceDep
from ..models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, user_service: UserServiceDep
) -> UserResponse:
    """Create a new user (public endpoint)."""
    user = await user_service.create(user_data)
    logger.info(f"New user created: {user.username}")
    return UserResponse.model_validate(user)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """Get current authenticated user information."""
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
    current_user: CurrentUser,
) -> UserResponse:
    """Get user by ID (authenticated users only)."""
    user = await user_service.get_by_id(user_id)
    return UserResponse.model_validate(user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: CurrentUser,
    user_service: UserServiceDep,
) -> UserResponse:
    """Update current user information."""
    user = await user_service.update(current_user.id, user_data)
    logger.info(f"User {user.username} updated their profile")
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserServiceDep,
    current_superuser: CurrentSuperUser,
) -> UserResponse:
    """Update any user (superuser only)."""
    user = await user_service.update(user_id, user_data)
    logger.info(f"Superuser {current_superuser.username} updated user {user.username}")
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserServiceDep,
    current_superuser: CurrentSuperUser,
) -> None:
    """Delete a user (superuser only)."""
    await user_service.delete(user_id)
    logger.info(f"Superuser {current_superuser.username} deleted user {user_id}")

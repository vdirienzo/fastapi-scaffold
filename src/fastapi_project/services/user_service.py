#!/usr/bin/env python3
"""
user_service.py - Business logic for user operations

Autor: Homero Thompson del Lago del Terror
"""

from typing import Optional

from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..exceptions import ConflictError, NotFoundError
from ..models.user import User, UserCreate, UserUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service class for user business logic."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    async def get_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if username exists
        existing_user = await self.get_by_username(user_data.username)
        if existing_user:
            raise ConflictError("User", "username", user_data.username)

        # Check if email exists
        existing_email = await self.get_by_email(user_data.email)
        if existing_email:
            raise ConflictError("User", "email", user_data.email)

        # Create user
        user = User(
            **user_data.model_dump(exclude={"password"}),
            hashed_password=self.hash_password(user_data.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        """Update a user."""
        user = await self.get_by_id(user_id)

        # Update only provided fields
        update_dict = user_data.model_dump(exclude_unset=True, exclude_none=True)

        # Handle password separately
        if "password" in update_dict:
            password = update_dict.pop("password")
            user.hashed_password = self.hash_password(password)

        # Check username uniqueness if being updated
        if "username" in update_dict and update_dict["username"] != user.username:
            existing = await self.get_by_username(update_dict["username"])
            if existing:
                raise ConflictError("User", "username", update_dict["username"])

        # Check email uniqueness if being updated
        if "email" in update_dict and update_dict["email"] != user.email:
            existing = await self.get_by_email(update_dict["email"])
            if existing:
                raise ConflictError("User", "email", update_dict["email"])

        # Apply updates
        for field, value in update_dict.items():
            setattr(user, field, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        """Delete a user."""
        user = await self.get_by_id(user_id)
        await self.session.delete(user)
        await self.session.commit()

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = await self.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

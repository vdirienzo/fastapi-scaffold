#!/usr/bin/env python3
"""
user.py - User model and schemas

Autor: Homero Thompson del Lago del Terror
"""

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base User schema with shared fields."""

    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(min_length=3, max_length=50, unique=True, index=True)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username is alphanumeric."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username must be alphanumeric (can include _ and -)")
        return v.lower()


class User(UserBase, table=True):
    """User database model."""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(SQLModel):
    """Schema for updating a user."""

    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=100)
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response (excludes password)."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(SQLModel):
    """Schema for user login."""

    username: str
    password: str


class Token(SQLModel):
    """Token response schema."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class TokenData(SQLModel):
    """Token payload data."""

    user_id: int
    username: str

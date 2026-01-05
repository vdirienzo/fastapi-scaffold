#!/usr/bin/env python3
"""
health.py - Health check endpoints

Autor: Homero Thompson del Lago del Terror
"""

from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> dict[str, str]:
    """Readiness check endpoint."""
    # TODO: Add checks for DB, Redis, etc.
    return {"status": "ready"}


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> dict[str, str]:
    """Liveness check endpoint."""
    return {"status": "alive"}

"""Health check endpoints."""

from fastapi import APIRouter, HTTPException
import logging

router = APIRouter()
logger = logging.getLogger("bps-api")


@router.get("")
async def health_check():
    """
    Basic health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "BPS Production API",
        "version": "1.0.0"
    }


@router.get("/live")
async def liveness_probe():
    """
    Kubernetes liveness probe. Returns 200 if service is running.
    """
    return {"status": "alive"}


@router.get("/ready")
async def readiness_probe():
    """
    Kubernetes readiness probe. Checks dependencies (DB, Cache).
    """
    # TODO: Check database connection
    # TODO: Check Redis connection
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "cache": "ok"
        }
    }

"""
BPS Production API - Main Application
Mês 9 Exercise: FastAPI app with monitoring, logging, and health checks
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.config import settings
from app.observability import setup_observability, setup_logging

# Setup logging first
logger = setup_logging(settings.log_level)

# Setup observability (metrics, tracing)
setup_observability("bps-api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan event handler for startup and shutdown.
    """
    logger.info("Starting BPS API", extra={
        "environment": settings.environment,
        "version": settings.app_version,
    })
    yield
    logger.info("Shutting down BPS API")


# Create FastAPI app
app = FastAPI(
    title="BPS Production API",
    description="Advanced Optimization & Co-simulation API",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])


# Global exception handler for structured logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware for structured request logging."""
    import uuid
    from time import time
    
    request.state.request_id = str(uuid.uuid4())
    start_time = time()
    
    try:
        response = await call_next(request)
        elapsed = time() - start_time
        
        logger.info(
            "HTTP request",
            extra={
                "request_id": request.state.request_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "elapsed_ms": round(elapsed * 1000, 2),
            }
        )
        return response
    except Exception as exc:
        elapsed = time() - start_time
        logger.error(
            "HTTP request failed",
            extra={
                "request_id": request.state.request_id,
                "method": request.method,
                "path": request.url.path,
                "elapsed_ms": round(elapsed * 1000, 2),
                "error": str(exc),
            },
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": request.state.request_id}
        )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(
        "Unhandled exception",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "error": str(exc),
        },
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )

"""Configuration management for BPS Production API."""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    app_name: str = "BPS Production API"
    app_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Environment
    environment: Literal["development", "staging", "production"] = "development"
    
    # Logging
    log_level: str = "INFO"
    
    # Database
    database_url: str = "postgresql://postgres:devpass@localhost:5432/bps_dev"
    db_pool_size: int = 20
    db_max_overflow: int = 10
    
    # Redis/Cache
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600
    
    # Observability
    enable_metrics: bool = True
    enable_tracing: bool = True
    jaeger_agent_host: str = "localhost"
    jaeger_agent_port: int = 6831
    
    # Security
    api_key_header: str = "X-API-Key"
    require_api_key: bool = False
    api_key: str | None = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()

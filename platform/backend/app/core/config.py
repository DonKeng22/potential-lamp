"""
Core configuration settings for the application
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Field Hockey Broadcasting Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql://user:password@db:5432/app"
    
    # Redis/Celery
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"
    
    # Security
    secret_key: str = "development-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    # File uploads
    upload_dir: str = "data/uploads"
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_video_extensions: List[str] = [".mp4", ".mov", ".avi"]
    
    class Config:
        env_file = ".env"


settings = Settings()
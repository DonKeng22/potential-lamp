"""
Configuration settings for the Field Hockey Broadcasting Platform.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "Field Hockey Broadcasting Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/field_hockey_broadcast"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_FORMATS: List[str] = [".mp4", ".avi", ".mov", ".mkv"]
    
    # Video Processing
    FFMPEG_PATH: str = "ffmpeg"
    HLS_SEGMENT_DURATION: int = 6
    HLS_PLAYLIST_LENGTH: int = 10
    
    # AI Models
    MODEL_CACHE_DIR: str = "models"
    YOLO_MODEL_PATH: str = "models/yolov8n.pt"
    NLP_MODEL_PATH: str = "models/commentary_generator"
    TTS_MODEL_PATH: str = "models/tts_model"
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Training
    TRAINING_DATA_DIR: str = "../data/raw_videos"
    ANNOTATIONS_DIR: str = "../data/annotations"
    MODEL_OUTPUT_DIR: str = "models/trained"
    
    # Community Features
    ENABLE_CHAT: bool = True
    ENABLE_POLLS: bool = True
    ENABLE_GAMIFICATION: bool = True
    
    # Analytics
    ENABLE_PLAYER_TRACKING: bool = True
    ENABLE_REAL_TIME_ANALYTICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_CACHE_DIR, exist_ok=True)
os.makedirs(settings.MODEL_OUTPUT_DIR, exist_ok=True) 
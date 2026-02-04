from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    # Database - SQLite for development
    DATABASE_URL: str = Field(
        default="sqlite:///./water_delivery.db",
        description="Database connection URL"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL"
    )
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # API Settings
    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")
    PROJECT_NAME: str = Field(
        default="Water Delivery Management System",
        description="Project name"
    )
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", description="Upload directory")
    MAX_FILE_SIZE: int = Field(default=10485760, description="Max file size (10MB)")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
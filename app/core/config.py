"""
Configuration settings for the AI-Powered Meeting Scheduler
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./meeting_scheduler.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Calendar API
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"
    
    # Microsoft Graph API
    microsoft_client_id: Optional[str] = None
    microsoft_client_secret: Optional[str] = None
    microsoft_redirect_uri: str = "http://localhost:8000/auth/microsoft/callback"
    
    # Redis for caching
    redis_url: str = "redis://localhost:6379"
    
    # AI/ML Settings
    ml_model_path: str = "./models"
    enable_ai_suggestions: bool = True
    min_training_data_points: int = 10
    
    # Meeting defaults
    default_meeting_duration: int = 30  # minutes
    buffer_time: int = 15  # minutes between meetings
    working_hours_start: int = 9  # 9 AM
    working_hours_end: int = 17  # 5 PM
    
    class Config:
        env_file = ".env"

settings = Settings()


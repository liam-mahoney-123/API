"""
Pydantic schemas for user-related API operations
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str
    timezone: str = "UTC"

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    timezone: Optional[str] = None
    is_active: Optional[bool] = None
    preferences: Optional[Dict[str, Any]] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    preferences: Dict[str, Any] = {}
    learned_patterns: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True

class UserPreferences(BaseModel):
    # Working hours
    working_hours_start: int = 9  # 24-hour format
    working_hours_end: int = 17
    working_days: list[int] = [1, 2, 3, 4, 5]  # Monday=1, Sunday=7
    
    # Meeting preferences
    preferred_meeting_duration: int = 30  # minutes
    buffer_time_before: int = 5  # minutes
    buffer_time_after: int = 5  # minutes
    max_meetings_per_day: int = 8
    
    # Time preferences
    preferred_meeting_times: list[str] = ["morning", "afternoon"]  # morning, afternoon, evening
    avoid_lunch_hours: bool = True
    lunch_start: int = 12  # 24-hour format
    lunch_end: int = 13
    
    # Communication preferences
    advance_notice_hours: int = 24
    reminder_preferences: Dict[str, bool] = {
        "email": True,
        "calendar": True,
        "push": False
    }
    
    # AI preferences
    enable_ai_suggestions: bool = True
    ai_learning_consent: bool = True
    suggestion_aggressiveness: str = "moderate"  # conservative, moderate, aggressive


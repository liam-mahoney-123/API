"""
Pydantic schemas for meeting-related API operations
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from enum import Enum

class MeetingStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ParticipantResponse(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    TENTATIVE = "tentative"

# Base schemas
class MeetingParticipantBase(BaseModel):
    user_id: int
    is_required: bool = True
    response_status: ParticipantResponse = ParticipantResponse.PENDING

class MeetingParticipantCreate(MeetingParticipantBase):
    pass

class MeetingParticipant(MeetingParticipantBase):
    id: int
    meeting_id: int
    response_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class MeetingBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    timezone: str = "UTC"
    location: Optional[str] = None
    meeting_url: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None

class MeetingCreate(MeetingBase):
    participant_emails: List[EmailStr]
    organizer_id: int

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    meeting_url: Optional[str] = None
    status: Optional[MeetingStatusEnum] = None

class Meeting(MeetingBase):
    id: int
    status: MeetingStatusEnum
    organizer_id: int
    ai_confidence_score: int = 0
    suggested_by_ai: bool = False
    optimization_factors: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    participants: List[MeetingParticipant] = []
    
    class Config:
        from_attributes = True

# Scheduling request schemas
class SchedulingRequestBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    participant_emails: List[EmailStr]
    preferred_times: Optional[List[Dict[str, Any]]] = None
    avoid_times: Optional[List[Dict[str, Any]]] = None
    earliest_date: Optional[datetime] = None
    latest_date: Optional[datetime] = None

class SchedulingRequestCreate(SchedulingRequestBase):
    requester_id: int

class SchedulingRequest(SchedulingRequestBase):
    id: int
    requester_id: int
    ai_suggestions: Optional[List[Dict[str, Any]]] = None
    selected_suggestion: Optional[Dict[str, Any]] = None
    status: str
    created_meeting_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# AI suggestion schemas
class TimeSlotSuggestion(BaseModel):
    start_time: datetime
    end_time: datetime
    confidence_score: int  # 0-100
    participants_available: List[int]  # user IDs
    optimization_factors: Dict[str, Any]
    reasoning: str

class MeetingSuggestions(BaseModel):
    request_id: int
    suggestions: List[TimeSlotSuggestion]
    generated_at: datetime
    total_participants: int
    constraints_applied: Dict[str, Any]


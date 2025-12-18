"""
Meeting-related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.database import Base

class MeetingStatus(PyEnum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String, default="UTC")
    location = Column(String, nullable=True)
    meeting_url = Column(String, nullable=True)  # For virtual meetings
    
    # Status and metadata
    status = Column(Enum(MeetingStatus), default=MeetingStatus.SCHEDULED)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String, nullable=True)
    
    # Organizer
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organizer = relationship("User", foreign_keys=[organizer_id], back_populates="meetings_organized")
    
    # AI-related fields
    ai_confidence_score = Column(Integer, default=0)  # 0-100
    suggested_by_ai = Column(Boolean, default=False)
    optimization_factors = Column(Text, nullable=True)  # JSON string of factors considered
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    participants = relationship("MeetingParticipant", back_populates="meeting", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Meeting(id={self.id}, title='{self.title}', start_time='{self.start_time}')>"

class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Participation details
    is_required = Column(Boolean, default=True)
    response_status = Column(String, default="pending")  # pending, accepted, declined, tentative
    response_time = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="participants")
    user = relationship("User", back_populates="meeting_participants")
    
    def __repr__(self):
        return f"<MeetingParticipant(meeting_id={self.meeting_id}, user_id={self.user_id}, status='{self.response_status}')>"


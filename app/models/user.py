"""
User model for the meeting scheduler
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    timezone = Column(String, default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Calendar integration
    google_calendar_token = Column(Text, nullable=True)
    microsoft_calendar_token = Column(Text, nullable=True)
    
    # AI preferences and learned patterns
    preferences = Column(JSON, default={})
    learned_patterns = Column(JSON, default={})
    
    # Relationships
    meetings_organized = relationship("Meeting", foreign_keys="Meeting.organizer_id", back_populates="organizer")
    availabilities = relationship("Availability", back_populates="user")
    meeting_participants = relationship("MeetingParticipant", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"


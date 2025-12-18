"""
Availability and scheduling models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Availability(Base):
    __tablename__ = "availabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Time slots
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String, default="UTC")
    
    # Availability type
    is_available = Column(Boolean, default=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String, nullable=True)  # daily, weekly, monthly
    
    # Priority and preferences
    priority = Column(Integer, default=1)  # 1-5, higher is more preferred
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="availabilities")
    
    def __repr__(self):
        return f"<Availability(user_id={self.user_id}, start='{self.start_time}', available={self.is_available})>"

class SchedulingRequest(Base):
    __tablename__ = "scheduling_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Meeting requirements
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    participant_emails = Column(JSON)  # List of participant emails
    
    # Scheduling preferences
    preferred_times = Column(JSON, nullable=True)  # List of preferred time slots
    avoid_times = Column(JSON, nullable=True)  # List of times to avoid
    earliest_date = Column(DateTime(timezone=True), nullable=True)
    latest_date = Column(DateTime(timezone=True), nullable=True)
    
    # AI suggestions
    ai_suggestions = Column(JSON, nullable=True)  # AI-generated time suggestions
    selected_suggestion = Column(JSON, nullable=True)  # User's selected option
    
    # Status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SchedulingRequest(id={self.id}, title='{self.title}', status='{self.status}')>"


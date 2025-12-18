"""
Meeting API endpoints for the AI-Powered Meeting Scheduler
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Meeting, SchedulingRequest, User
from app.schemas.meeting import (
    MeetingCreate, Meeting as MeetingSchema, MeetingUpdate,
    SchedulingRequestCreate, SchedulingRequest as SchedulingRequestSchema,
    MeetingSuggestions, TimeSlotSuggestion
)
from app.services.scheduler import AIScheduler
from app.services.calendar.base import MockCalendarService

router = APIRouter()

# Initialize services (in production, use dependency injection)
calendar_service = MockCalendarService()

@router.post("/schedule", response_model=SchedulingRequestSchema)
async def create_scheduling_request(
    request: SchedulingRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new scheduling request for AI-powered meeting scheduling
    """
    # Validate that all participant emails exist as users
    participants = db.query(User).filter(User.email.in_(request.participant_emails)).all()
    found_emails = {p.email for p in participants}
    missing_emails = set(request.participant_emails) - found_emails
    
    if missing_emails:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Users not found for emails: {list(missing_emails)}"
        )
    
    # Create scheduling request
    db_request = SchedulingRequest(
        requester_id=request.requester_id,
        title=request.title,
        description=request.description,
        duration_minutes=request.duration_minutes,
        participant_emails=request.participant_emails,
        preferred_times=request.preferred_times,
        avoid_times=request.avoid_times,
        earliest_date=request.earliest_date,
        latest_date=request.latest_date,
        status="pending"
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return db_request

@router.get("/suggestions/{request_id}", response_model=MeetingSuggestions)
async def get_meeting_suggestions(
    request_id: int,
    max_suggestions: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get AI-powered meeting time suggestions for a scheduling request
    """
    # Get the scheduling request
    request = db.query(SchedulingRequest).filter(SchedulingRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduling request not found"
        )
    
    # Initialize AI scheduler
    scheduler = AIScheduler(db, calendar_service)
    
    try:
        # Generate suggestions
        suggestions = await scheduler.suggest_meeting_times(request, max_suggestions)
        
        # Update request with AI suggestions
        request.ai_suggestions = [s.dict() for s in suggestions.suggestions]
        request.status = "processing"
        db.commit()
        
        return suggestions
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )

@router.post("/confirm/{request_id}", response_model=MeetingSchema)
async def confirm_meeting(
    request_id: int,
    suggestion_index: int,
    db: Session = Depends(get_db)
):
    """
    Confirm a meeting based on selected AI suggestion
    """
    # Get the scheduling request
    request = db.query(SchedulingRequest).filter(SchedulingRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduling request not found"
        )
    
    if not request.ai_suggestions or suggestion_index >= len(request.ai_suggestions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid suggestion index"
        )
    
    # Get the selected suggestion
    selected_suggestion_data = request.ai_suggestions[suggestion_index]
    selected_suggestion = TimeSlotSuggestion(**selected_suggestion_data)
    
    # Initialize AI scheduler
    scheduler = AIScheduler(db, calendar_service)
    
    try:
        # Create the meeting
        meeting = await scheduler.schedule_meeting(request, selected_suggestion)
        return meeting
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create meeting: {str(e)}"
        )

@router.get("/", response_model=List[MeetingSchema])
async def get_meetings(
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get meetings with optional filtering
    """
    query = db.query(Meeting)
    
    if user_id:
        query = query.filter(
            (Meeting.organizer_id == user_id) |
            (Meeting.participants.any(user_id=user_id))
        )
    
    if start_date:
        query = query.filter(Meeting.start_time >= start_date)
    
    if end_date:
        query = query.filter(Meeting.end_time <= end_date)
    
    meetings = query.offset(skip).limit(limit).all()
    return meetings

@router.get("/{meeting_id}", response_model=MeetingSchema)
async def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """
    Get a specific meeting by ID
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    return meeting

@router.put("/{meeting_id}", response_model=MeetingSchema)
async def update_meeting(
    meeting_id: int,
    meeting_update: MeetingUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a meeting
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Update fields
    update_data = meeting_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meeting, field, value)
    
    db.commit()
    db.refresh(meeting)
    
    return meeting

@router.delete("/{meeting_id}")
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """
    Delete a meeting
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    db.delete(meeting)
    db.commit()
    
    return {"message": "Meeting deleted successfully"}

@router.get("/requests/", response_model=List[SchedulingRequestSchema])
async def get_scheduling_requests(
    requester_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get scheduling requests with optional filtering
    """
    query = db.query(SchedulingRequest)
    
    if requester_id:
        query = query.filter(SchedulingRequest.requester_id == requester_id)
    
    if status:
        query = query.filter(SchedulingRequest.status == status)
    
    requests = query.offset(skip).limit(limit).all()
    return requests


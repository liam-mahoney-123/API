"""
Availability API endpoints
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Availability, User
from app.services.availability_analyzer import AvailabilityAnalyzer
from app.services.calendar.base import MockCalendarService

router = APIRouter()
calendar_service = MockCalendarService()

@router.get("/{user_id}")
async def get_user_availability(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """Get availability for a specific user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    analyzer = AvailabilityAnalyzer(db, calendar_service)
    
    try:
        busy_times = await analyzer._get_participant_busy_times(
            user, start_date, end_date, "UTC"
        )
        
        return {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "busy_times": busy_times,
            "timezone": user.timezone
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get availability: {str(e)}"
        )

@router.post("/check-common")
async def check_common_availability(
    participant_ids: List[int],
    duration_minutes: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """Check common availability for multiple participants"""
    # Validate participants exist
    participants = db.query(User).filter(User.id.in_(participant_ids)).all()
    if len(participants) != len(participant_ids):
        found_ids = {p.id for p in participants}
        missing_ids = set(participant_ids) - found_ids
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Users not found for IDs: {list(missing_ids)}"
        )
    
    analyzer = AvailabilityAnalyzer(db, calendar_service)
    
    try:
        common_slots = await analyzer.find_common_availability(
            participant_ids=participant_ids,
            duration_minutes=duration_minutes,
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "participant_ids": participant_ids,
            "duration_minutes": duration_minutes,
            "start_date": start_date,
            "end_date": end_date,
            "available_slots": common_slots[:10]  # Return top 10 slots
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find common availability: {str(e)}"
        )


"""
User preferences API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.user import UserPreferences

router = APIRouter()

@router.get("/{user_id}", response_model=UserPreferences)
async def get_user_preferences(user_id: int, db: Session = Depends(get_db)):
    """Get user preferences"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return preferences with defaults
    preferences = user.preferences or {}
    return UserPreferences(**preferences)

@router.put("/{user_id}", response_model=UserPreferences)
async def update_user_preferences(
    user_id: int,
    preferences: UserPreferences,
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update preferences
    user.preferences = preferences.dict()
    db.commit()
    db.refresh(user)
    
    return preferences


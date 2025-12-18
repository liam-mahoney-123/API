"""
Core scheduling service with AI-powered optimization
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pytz
from sqlalchemy.orm import Session
from app.models import User, Meeting, Availability, SchedulingRequest
from app.schemas.meeting import TimeSlotSuggestion, MeetingSuggestions
from app.services.availability_analyzer import AvailabilityAnalyzer
from app.services.calendar.base import CalendarService
from app.ml.time_optimizer import TimeOptimizer
from app.core.config import settings

class AIScheduler:
    """
    AI-Powered Meeting Scheduler that combines rule-based logic with ML optimization
    """
    
    def __init__(self, db: Session, calendar_service: CalendarService):
        self.db = db
        self.calendar_service = calendar_service
        self.availability_analyzer = AvailabilityAnalyzer(db, calendar_service)
        self.time_optimizer = TimeOptimizer() if settings.enable_ai_suggestions else None
    
    async def suggest_meeting_times(
        self, 
        request: SchedulingRequest,
        max_suggestions: int = 5
    ) -> MeetingSuggestions:
        """
        Generate AI-powered meeting time suggestions
        """
        # Get participant information
        participants = await self._get_participants_by_emails(request.participant_emails)
        
        # Analyze availability for all participants
        availability_windows = await self.availability_analyzer.find_common_availability(
            participant_ids=[p.id for p in participants],
            duration_minutes=request.duration_minutes,
            start_date=request.earliest_date or datetime.now(),
            end_date=request.latest_date or (datetime.now() + timedelta(days=30))
        )
        
        # Apply basic constraints
        filtered_windows = self._apply_constraints(availability_windows, request)
        
        # Generate AI-optimized suggestions
        suggestions = []
        if self.time_optimizer and len(filtered_windows) > 0:
            # Use ML model to rank and optimize suggestions
            ai_ranked_windows = await self.time_optimizer.optimize_time_slots(
                windows=filtered_windows,
                participants=participants,
                request=request
            )
            
            for window in ai_ranked_windows[:max_suggestions]:
                suggestion = TimeSlotSuggestion(
                    start_time=window['start_time'],
                    end_time=window['end_time'],
                    confidence_score=window['confidence_score'],
                    participants_available=window['participants_available'],
                    optimization_factors=window['optimization_factors'],
                    reasoning=window['reasoning']
                )
                suggestions.append(suggestion)
        else:
            # Fallback to rule-based suggestions
            for window in filtered_windows[:max_suggestions]:
                suggestion = TimeSlotSuggestion(
                    start_time=window['start_time'],
                    end_time=window['end_time'],
                    confidence_score=self._calculate_rule_based_score(window, participants),
                    participants_available=window['participants_available'],
                    optimization_factors={'method': 'rule_based'},
                    reasoning="Based on availability and basic preferences"
                )
                suggestions.append(suggestion)
        
        return MeetingSuggestions(
            request_id=request.id,
            suggestions=suggestions,
            generated_at=datetime.now(),
            total_participants=len(participants),
            constraints_applied=self._get_applied_constraints(request)
        )
    
    async def schedule_meeting(
        self, 
        request: SchedulingRequest, 
        selected_suggestion: TimeSlotSuggestion
    ) -> Meeting:
        """
        Create a meeting based on the selected AI suggestion
        """
        # Create the meeting
        meeting = Meeting(
            title=request.title,
            description=request.description,
            start_time=selected_suggestion.start_time,
            end_time=selected_suggestion.end_time,
            organizer_id=request.requester_id,
            ai_confidence_score=selected_suggestion.confidence_score,
            suggested_by_ai=True,
            optimization_factors=str(selected_suggestion.optimization_factors)
        )
        
        self.db.add(meeting)
        self.db.commit()
        self.db.refresh(meeting)
        
        # Add participants
        participants = await self._get_participants_by_emails(request.participant_emails)
        for participant in participants:
            from app.models.meeting import MeetingParticipant
            meeting_participant = MeetingParticipant(
                meeting_id=meeting.id,
                user_id=participant.id,
                is_required=True
            )
            self.db.add(meeting_participant)
        
        # Create calendar events for all participants
        await self._create_calendar_events(meeting, participants)
        
        # Update the scheduling request
        request.status = "completed"
        request.created_meeting_id = meeting.id
        request.selected_suggestion = selected_suggestion.dict()
        
        self.db.commit()
        
        # Learn from this scheduling decision for future AI improvements
        if self.time_optimizer:
            await self.time_optimizer.record_scheduling_decision(
                request=request,
                selected_suggestion=selected_suggestion,
                participants=participants
            )
        
        return meeting
    
    def _apply_constraints(
        self, 
        windows: List[Dict], 
        request: SchedulingRequest
    ) -> List[Dict]:
        """Apply scheduling constraints to filter availability windows"""
        filtered = []
        
        for window in windows:
            # Check preferred times
            if request.preferred_times:
                if not self._matches_preferred_times(window, request.preferred_times):
                    continue
            
            # Check avoid times
            if request.avoid_times:
                if self._conflicts_with_avoid_times(window, request.avoid_times):
                    continue
            
            # Check working hours (basic implementation)
            start_hour = window['start_time'].hour
            if start_hour < settings.working_hours_start or start_hour >= settings.working_hours_end:
                continue
            
            filtered.append(window)
        
        return filtered
    
    def _calculate_rule_based_score(self, window: Dict, participants: List[User]) -> int:
        """Calculate a confidence score based on rules"""
        score = 50  # Base score
        
        # Prefer times during working hours
        start_hour = window['start_time'].hour
        if settings.working_hours_start <= start_hour < settings.working_hours_end:
            score += 20
        
        # Prefer times with all participants available
        if len(window['participants_available']) == len(participants):
            score += 20
        
        # Prefer morning meetings (9-11 AM)
        if 9 <= start_hour <= 11:
            score += 10
        
        return min(score, 100)
    
    def _matches_preferred_times(self, window: Dict, preferred_times: List[Dict]) -> bool:
        """Check if window matches preferred time constraints"""
        # Simplified implementation - would need more sophisticated logic
        return True
    
    def _conflicts_with_avoid_times(self, window: Dict, avoid_times: List[Dict]) -> bool:
        """Check if window conflicts with times to avoid"""
        # Simplified implementation - would need more sophisticated logic
        return False
    
    def _get_applied_constraints(self, request: SchedulingRequest) -> Dict:
        """Get summary of constraints applied during scheduling"""
        return {
            "working_hours": f"{settings.working_hours_start}-{settings.working_hours_end}",
            "buffer_time": settings.buffer_time,
            "has_preferred_times": bool(request.preferred_times),
            "has_avoid_times": bool(request.avoid_times),
            "date_range": {
                "earliest": request.earliest_date.isoformat() if request.earliest_date else None,
                "latest": request.latest_date.isoformat() if request.latest_date else None
            }
        }
    
    async def _get_participants_by_emails(self, emails: List[str]) -> List[User]:
        """Get user objects from email addresses"""
        return self.db.query(User).filter(User.email.in_(emails)).all()
    
    async def _create_calendar_events(self, meeting: Meeting, participants: List[User]):
        """Create calendar events for all participants"""
        for participant in participants:
            try:
                await self.calendar_service.create_event(
                    user=participant,
                    title=meeting.title,
                    description=meeting.description,
                    start_time=meeting.start_time,
                    end_time=meeting.end_time,
                    attendees=[p.email for p in participants]
                )
            except Exception as e:
                # Log error but don't fail the entire scheduling process
                print(f"Failed to create calendar event for {participant.email}: {e}")
                continue


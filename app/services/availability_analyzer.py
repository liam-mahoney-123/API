"""
Availability analysis service for finding optimal meeting times
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pytz
from sqlalchemy.orm import Session
from app.models import User, Availability, Meeting
from app.services.calendar.base import CalendarService
from app.core.config import settings

class AvailabilityAnalyzer:
    """
    Analyzes participant availability across multiple calendar sources
    """
    
    def __init__(self, db: Session, calendar_service: CalendarService):
        self.db = db
        self.calendar_service = calendar_service
    
    async def find_common_availability(
        self,
        participant_ids: List[int],
        duration_minutes: int,
        start_date: datetime,
        end_date: datetime,
        timezone: str = "UTC"
    ) -> List[Dict]:
        """
        Find time slots where all participants are available
        """
        # Get all participants
        participants = self.db.query(User).filter(User.id.in_(participant_ids)).all()
        
        # Collect availability data from all sources
        all_busy_times = []
        for participant in participants:
            busy_times = await self._get_participant_busy_times(
                participant, start_date, end_date, timezone
            )
            all_busy_times.extend(busy_times)
        
        # Find free time slots
        free_slots = self._find_free_time_slots(
            busy_times=all_busy_times,
            start_date=start_date,
            end_date=end_date,
            duration_minutes=duration_minutes,
            timezone=timezone
        )
        
        # Enhance slots with participant availability info
        enhanced_slots = []
        for slot in free_slots:
            participants_available = await self._check_participants_availability(
                participants, slot['start_time'], slot['end_time']
            )
            
            enhanced_slot = {
                **slot,
                'participants_available': [p.id for p in participants_available],
                'total_participants': len(participants),
                'availability_percentage': len(participants_available) / len(participants) * 100
            }
            enhanced_slots.append(enhanced_slot)
        
        # Sort by availability percentage and preference scores
        enhanced_slots.sort(
            key=lambda x: (x['availability_percentage'], x.get('preference_score', 0)),
            reverse=True
        )
        
        return enhanced_slots
    
    async def _get_participant_busy_times(
        self,
        participant: User,
        start_date: datetime,
        end_date: datetime,
        timezone: str
    ) -> List[Dict]:
        """
        Get all busy times for a participant from various sources
        """
        busy_times = []
        
        # Get from external calendars (Google, Outlook, etc.)
        try:
            calendar_events = await self.calendar_service.get_events(
                user=participant,
                start_time=start_date,
                end_time=end_date
            )
            
            for event in calendar_events:
                busy_times.append({
                    'start_time': event['start_time'],
                    'end_time': event['end_time'],
                    'source': 'external_calendar',
                    'title': event.get('title', 'Busy'),
                    'user_id': participant.id
                })
        except Exception as e:
            print(f"Failed to get calendar events for {participant.email}: {e}")
        
        # Get from internal meetings
        internal_meetings = self.db.query(Meeting).join(
            Meeting.participants
        ).filter(
            Meeting.start_time >= start_date,
            Meeting.end_time <= end_date,
            Meeting.participants.any(user_id=participant.id)
        ).all()
        
        for meeting in internal_meetings:
            busy_times.append({
                'start_time': meeting.start_time,
                'end_time': meeting.end_time,
                'source': 'internal_meeting',
                'title': meeting.title,
                'user_id': participant.id
            })
        
        # Get explicit unavailability periods
        unavailable_periods = self.db.query(Availability).filter(
            Availability.user_id == participant.id,
            Availability.is_available == False,
            Availability.start_time >= start_date,
            Availability.end_time <= end_date
        ).all()
        
        for period in unavailable_periods:
            busy_times.append({
                'start_time': period.start_time,
                'end_time': period.end_time,
                'source': 'explicit_unavailable',
                'title': 'Unavailable',
                'user_id': participant.id
            })
        
        return busy_times
    
    def _find_free_time_slots(
        self,
        busy_times: List[Dict],
        start_date: datetime,
        end_date: datetime,
        duration_minutes: int,
        timezone: str
    ) -> List[Dict]:
        """
        Find free time slots by analyzing busy periods
        """
        # Sort busy times by start time
        busy_times.sort(key=lambda x: x['start_time'])
        
        # Merge overlapping busy periods
        merged_busy = self._merge_overlapping_periods(busy_times)
        
        # Find gaps between busy periods
        free_slots = []
        current_time = start_date
        
        for busy_period in merged_busy:
            # Check if there's a gap before this busy period
            if current_time < busy_period['start_time']:
                gap_duration = (busy_period['start_time'] - current_time).total_seconds() / 60
                
                if gap_duration >= duration_minutes + settings.buffer_time:
                    # Create time slots within this gap
                    slots_in_gap = self._create_slots_in_period(
                        start_time=current_time,
                        end_time=busy_period['start_time'],
                        duration_minutes=duration_minutes,
                        timezone=timezone
                    )
                    free_slots.extend(slots_in_gap)
            
            current_time = max(current_time, busy_period['end_time'])
        
        # Check for time after the last busy period
        if current_time < end_date:
            gap_duration = (end_date - current_time).total_seconds() / 60
            if gap_duration >= duration_minutes + settings.buffer_time:
                slots_in_gap = self._create_slots_in_period(
                    start_time=current_time,
                    end_time=end_date,
                    duration_minutes=duration_minutes,
                    timezone=timezone
                )
                free_slots.extend(slots_in_gap)
        
        return free_slots
    
    def _merge_overlapping_periods(self, periods: List[Dict]) -> List[Dict]:
        """
        Merge overlapping time periods
        """
        if not periods:
            return []
        
        merged = [periods[0]]
        
        for current in periods[1:]:
            last_merged = merged[-1]
            
            # Check if current period overlaps with the last merged period
            if current['start_time'] <= last_merged['end_time']:
                # Merge the periods
                last_merged['end_time'] = max(last_merged['end_time'], current['end_time'])
            else:
                # No overlap, add as new period
                merged.append(current)
        
        return merged
    
    def _create_slots_in_period(
        self,
        start_time: datetime,
        end_time: datetime,
        duration_minutes: int,
        timezone: str
    ) -> List[Dict]:
        """
        Create meeting slots within a free time period
        """
        slots = []
        current_start = start_time
        slot_duration = timedelta(minutes=duration_minutes)
        buffer_duration = timedelta(minutes=settings.buffer_time)
        
        while current_start + slot_duration <= end_time:
            # Check if this slot is within working hours
            if self._is_within_working_hours(current_start):
                slot_end = current_start + slot_duration
                
                slots.append({
                    'start_time': current_start,
                    'end_time': slot_end,
                    'duration_minutes': duration_minutes,
                    'timezone': timezone,
                    'preference_score': self._calculate_time_preference_score(current_start)
                })
            
            # Move to next potential slot (with buffer)
            current_start += timedelta(minutes=30)  # 30-minute increments
        
        return slots
    
    def _is_within_working_hours(self, time: datetime) -> bool:
        """
        Check if time is within standard working hours
        """
        hour = time.hour
        weekday = time.weekday()  # 0 = Monday, 6 = Sunday
        
        # Check if it's a weekday
        if weekday >= 5:  # Weekend
            return False
        
        # Check working hours
        return settings.working_hours_start <= hour < settings.working_hours_end
    
    def _calculate_time_preference_score(self, time: datetime) -> int:
        """
        Calculate preference score based on time of day
        """
        hour = time.hour
        
        # Morning preference (9-11 AM)
        if 9 <= hour <= 11:
            return 90
        # Early afternoon (1-3 PM)
        elif 13 <= hour <= 15:
            return 80
        # Late morning (11 AM - 12 PM)
        elif 11 <= hour <= 12:
            return 70
        # Late afternoon (3-5 PM)
        elif 15 <= hour <= 17:
            return 60
        # Early morning (8-9 AM)
        elif 8 <= hour <= 9:
            return 50
        else:
            return 30
    
    async def _check_participants_availability(
        self,
        participants: List[User],
        start_time: datetime,
        end_time: datetime
    ) -> List[User]:
        """
        Check which participants are actually available for a specific time slot
        """
        available_participants = []
        
        for participant in participants:
            is_available = await self._is_participant_available(
                participant, start_time, end_time
            )
            if is_available:
                available_participants.append(participant)
        
        return available_participants
    
    async def _is_participant_available(
        self,
        participant: User,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """
        Check if a specific participant is available for a time slot
        """
        # Check for conflicts in external calendar
        try:
            conflicts = await self.calendar_service.check_conflicts(
                user=participant,
                start_time=start_time,
                end_time=end_time
            )
            if conflicts:
                return False
        except Exception:
            # If we can't check external calendar, assume available
            pass
        
        # Check for conflicts in internal meetings
        conflicting_meetings = self.db.query(Meeting).join(
            Meeting.participants
        ).filter(
            Meeting.participants.any(user_id=participant.id),
            Meeting.start_time < end_time,
            Meeting.end_time > start_time
        ).count()
        
        if conflicting_meetings > 0:
            return False
        
        # Check explicit unavailability
        unavailable_periods = self.db.query(Availability).filter(
            Availability.user_id == participant.id,
            Availability.is_available == False,
            Availability.start_time < end_time,
            Availability.end_time > start_time
        ).count()
        
        return unavailable_periods == 0


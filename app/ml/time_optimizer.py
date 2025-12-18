"""
AI/ML Time Optimization Engine for intelligent meeting scheduling
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from app.core.config import settings
from app.models import User, Meeting, SchedulingRequest

class TimeOptimizer:
    """
    Machine Learning-powered time optimization for meeting scheduling
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = os.path.join(settings.ml_model_path, "time_optimizer.joblib")
        self.scaler_path = os.path.join(settings.ml_model_path, "time_scaler.joblib")
        
        # Create model directory if it doesn't exist
        os.makedirs(settings.ml_model_path, exist_ok=True)
        
        # Load existing model if available
        self._load_model()
    
    async def optimize_time_slots(
        self,
        windows: List[Dict],
        participants: List[User],
        request: SchedulingRequest
    ) -> List[Dict]:
        """
        Use ML model to optimize and rank time slots
        """
        if not self.is_trained or len(windows) == 0:
            # Fallback to rule-based ranking
            return self._rule_based_ranking(windows, participants, request)
        
        # Extract features for each time window
        features_list = []
        for window in windows:
            features = self._extract_features(window, participants, request)
            features_list.append(features)
        
        if not features_list:
            return windows
        
        # Predict scores using ML model
        features_array = np.array(features_list)
        features_scaled = self.scaler.transform(features_array)
        predicted_scores = self.model.predict(features_scaled)
        
        # Add ML predictions to windows
        for i, window in enumerate(windows):
            window['confidence_score'] = int(min(max(predicted_scores[i] * 100, 0), 100))
            window['optimization_factors'] = {
                'method': 'ml_optimized',
                'model_confidence': predicted_scores[i],
                'features_used': self._get_feature_names()
            }
            window['reasoning'] = self._generate_reasoning(window, predicted_scores[i])
        
        # Sort by predicted score
        windows.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return windows
    
    def _extract_features(
        self,
        window: Dict,
        participants: List[User],
        request: SchedulingRequest
    ) -> List[float]:
        """
        Extract features for ML model prediction
        """
        start_time = window['start_time']
        
        features = [
            # Time-based features
            start_time.hour,  # Hour of day
            start_time.weekday(),  # Day of week (0=Monday)
            start_time.day,  # Day of month
            
            # Availability features
            window.get('availability_percentage', 100),
            len(window.get('participants_available', [])),
            len(participants),
            
            # Meeting characteristics
            request.duration_minutes,
            window.get('preference_score', 50),
            
            # Participant features (aggregated)
            self._get_avg_participant_preference_score(participants, start_time),
            self._get_participant_timezone_spread(participants),
            
            # Historical features
            self._get_historical_success_rate(start_time.hour, start_time.weekday()),
            self._get_time_slot_popularity(start_time.hour),
            
            # Contextual features
            1 if self._is_morning(start_time) else 0,
            1 if self._is_afternoon(start_time) else 0,
            1 if self._is_peak_hours(start_time) else 0,
            1 if self._is_lunch_time(start_time) else 0,
        ]
        
        return features
    
    def _get_feature_names(self) -> List[str]:
        """Get names of features used in the model"""
        return [
            'hour', 'weekday', 'day_of_month',
            'availability_percentage', 'available_participants', 'total_participants',
            'duration_minutes', 'preference_score',
            'avg_participant_preference', 'timezone_spread',
            'historical_success_rate', 'time_slot_popularity',
            'is_morning', 'is_afternoon', 'is_peak_hours', 'is_lunch_time'
        ]
    
    def _get_avg_participant_preference_score(self, participants: List[User], time: datetime) -> float:
        """Calculate average participant preference for this time"""
        if not participants:
            return 50.0
        
        scores = []
        for participant in participants:
            # Extract preferences from user data
            prefs = participant.preferences or {}
            working_hours_start = prefs.get('working_hours_start', 9)
            working_hours_end = prefs.get('working_hours_end', 17)
            
            if working_hours_start <= time.hour < working_hours_end:
                scores.append(80.0)
            else:
                scores.append(30.0)
        
        return np.mean(scores)
    
    def _get_participant_timezone_spread(self, participants: List[User]) -> float:
        """Calculate timezone spread among participants"""
        timezones = [p.timezone for p in participants if p.timezone]
        return len(set(timezones)) if timezones else 1.0
    
    def _get_historical_success_rate(self, hour: int, weekday: int) -> float:
        """Get historical success rate for this time slot"""
        # This would query historical meeting data
        # For now, return a simple heuristic
        if 9 <= hour <= 11 and weekday < 5:  # Morning weekdays
            return 0.85
        elif 13 <= hour <= 15 and weekday < 5:  # Afternoon weekdays
            return 0.75
        elif weekday >= 5:  # Weekends
            return 0.3
        else:
            return 0.6
    
    def _get_time_slot_popularity(self, hour: int) -> float:
        """Get popularity score for this hour"""
        popularity_map = {
            9: 0.9, 10: 0.95, 11: 0.8, 12: 0.4, 13: 0.7,
            14: 0.85, 15: 0.75, 16: 0.6, 17: 0.4
        }
        return popularity_map.get(hour, 0.3)
    
    def _is_morning(self, time: datetime) -> bool:
        return 6 <= time.hour < 12
    
    def _is_afternoon(self, time: datetime) -> bool:
        return 12 <= time.hour < 18
    
    def _is_peak_hours(self, time: datetime) -> bool:
        return time.hour in [10, 11, 14, 15]
    
    def _is_lunch_time(self, time: datetime) -> bool:
        return 12 <= time.hour < 14
    
    def _generate_reasoning(self, window: Dict, score: float) -> str:
        """Generate human-readable reasoning for the suggestion"""
        start_time = window['start_time']
        hour = start_time.hour
        
        reasons = []
        
        if score > 0.8:
            reasons.append("High confidence based on historical success patterns")
        elif score > 0.6:
            reasons.append("Good match based on participant preferences")
        else:
            reasons.append("Available slot with moderate confidence")
        
        if 9 <= hour <= 11:
            reasons.append("Morning time slot preferred by most users")
        elif 13 <= hour <= 15:
            reasons.append("Early afternoon slot with good availability")
        
        if window.get('availability_percentage', 0) == 100:
            reasons.append("All participants available")
        
        return ". ".join(reasons)
    
    def _rule_based_ranking(
        self,
        windows: List[Dict],
        participants: List[User],
        request: SchedulingRequest
    ) -> List[Dict]:
        """
        Fallback rule-based ranking when ML model is not available
        """
        for window in windows:
            score = 50  # Base score
            start_time = window['start_time']
            
            # Time of day preferences
            if 9 <= start_time.hour <= 11:
                score += 25
            elif 13 <= start_time.hour <= 15:
                score += 20
            elif 8 <= start_time.hour <= 9:
                score += 10
            
            # Availability percentage
            availability_pct = window.get('availability_percentage', 0)
            score += availability_pct * 0.3
            
            # Weekday preference
            if start_time.weekday() < 5:  # Weekday
                score += 15
            
            window['confidence_score'] = int(min(score, 100))
            window['optimization_factors'] = {'method': 'rule_based'}
            window['reasoning'] = "Based on standard scheduling preferences and availability"
        
        windows.sort(key=lambda x: x['confidence_score'], reverse=True)
        return windows
    
    async def record_scheduling_decision(
        self,
        request: SchedulingRequest,
        selected_suggestion: Any,
        participants: List[User]
    ):
        """
        Record a scheduling decision for future model training
        """
        # This would store the decision data for later training
        # Implementation would depend on your data storage strategy
        pass
    
    async def train_model(self, training_data: pd.DataFrame):
        """
        Train the ML model with historical scheduling data
        """
        if len(training_data) < settings.min_training_data_points:
            print(f"Insufficient training data: {len(training_data)} < {settings.min_training_data_points}")
            return
        
        # Prepare features and target
        feature_columns = self._get_feature_names()
        X = training_data[feature_columns].values
        y = training_data['success_score'].values  # 0-1 success score
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Model trained - Train score: {train_score:.3f}, Test score: {test_score:.3f}")
        
        # Save model
        self._save_model()
        self.is_trained = True
    
    def _save_model(self):
        """Save the trained model and scaler"""
        if self.model is not None:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
    
    def _load_model(self):
        """Load existing model and scaler"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                print("ML model loaded successfully")
        except Exception as e:
            print(f"Failed to load ML model: {e}")
            self.is_trained = False


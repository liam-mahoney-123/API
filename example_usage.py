"""
Example usage of the AI-Powered Meeting Scheduler API
"""
import asyncio
import requests
from datetime import datetime, timedelta
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def create_sample_users():
    """Create sample users for testing"""
    users = [
        {
            "email": "alice@company.com",
            "name": "Alice Johnson",
            "timezone": "America/New_York"
        },
        {
            "email": "bob@company.com", 
            "name": "Bob Smith",
            "timezone": "America/Los_Angeles"
        },
        {
            "email": "charlie@company.com",
            "name": "Charlie Brown",
            "timezone": "Europe/London"
        }
    ]
    
    created_users = []
    for user_data in users:
        try:
            response = requests.post(f"{BASE_URL}/users/", json=user_data)
            if response.status_code == 200:
                created_users.append(response.json())
                print(f"✅ Created user: {user_data['name']}")
            else:
                print(f"❌ Failed to create user {user_data['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Error creating user {user_data['name']}: {e}")
    
    return created_users

def create_scheduling_request(requester_id: int):
    """Create a scheduling request"""
    # Calculate dates for next week
    now = datetime.now()
    earliest_date = now + timedelta(days=1)
    latest_date = now + timedelta(days=7)
    
    request_data = {
        "title": "AI Team Planning Meeting",
        "description": "Quarterly planning session for the AI development team",
        "duration_minutes": 60,
        "participant_emails": [
            "alice@company.com",
            "bob@company.com", 
            "charlie@company.com"
        ],
        "requester_id": requester_id,
        "earliest_date": earliest_date.isoformat(),
        "latest_date": latest_date.isoformat(),
        "preferred_times": [
            {
                "type": "time_range",
                "start_hour": 10,
                "end_hour": 15,
                "days": ["monday", "tuesday", "wednesday", "thursday"]
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/meetings/schedule", json=request_data)
        if response.status_code == 200:
            request = response.json()
            print(f"✅ Created scheduling request: {request['title']}")
            print(f"   Request ID: {request['id']}")
            return request
        else:
            print(f"❌ Failed to create scheduling request: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating scheduling request: {e}")
        return None

def get_ai_suggestions(request_id: int):
    """Get AI-powered meeting suggestions"""
    try:
        response = requests.get(f"{BASE_URL}/meetings/suggestions/{request_id}")
        if response.status_code == 200:
            suggestions = response.json()
            print(f"✅ Generated {len(suggestions['suggestions'])} AI suggestions:")
            
            for i, suggestion in enumerate(suggestions['suggestions']):
                start_time = datetime.fromisoformat(suggestion['start_time'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(suggestion['end_time'].replace('Z', '+00:00'))
                
                print(f"   {i+1}. {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}")
                print(f"      Confidence: {suggestion['confidence_score']}%")
                print(f"      Available: {len(suggestion['participants_available'])}/{suggestions['total_participants']} participants")
                print(f"      Reasoning: {suggestion['reasoning']}")
                print()
            
            return suggestions
        else:
            print(f"❌ Failed to get suggestions: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error getting suggestions: {e}")
        return None

def confirm_meeting(request_id: int, suggestion_index: int = 0):
    """Confirm a meeting based on AI suggestion"""
    try:
        response = requests.post(f"{BASE_URL}/meetings/confirm/{request_id}?suggestion_index={suggestion_index}")
        if response.status_code == 200:
            meeting = response.json()
            start_time = datetime.fromisoformat(meeting['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(meeting['end_time'].replace('Z', '+00:00'))
            
            print(f"✅ Meeting confirmed!")
            print(f"   Title: {meeting['title']}")
            print(f"   Time: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}")
            print(f"   Meeting ID: {meeting['id']}")
            print(f"   AI Confidence: {meeting['ai_confidence_score']}%")
            print(f"   Suggested by AI: {meeting['suggested_by_ai']}")
            
            return meeting
        else:
            print(f"❌ Failed to confirm meeting: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error confirming meeting: {e}")
        return None

def check_availability(user_id: int):
    """Check user availability"""
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    try:
        response = requests.get(
            f"{BASE_URL}/availability/{user_id}",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        if response.status_code == 200:
            availability = response.json()
            print(f"✅ Availability for user {user_id}:")
            print(f"   Busy periods: {len(availability['busy_times'])}")
            for busy in availability['busy_times'][:3]:  # Show first 3
                start = datetime.fromisoformat(busy['start_time'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(busy['end_time'].replace('Z', '+00:00'))
                print(f"   - {start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}: {busy['title']}")
            
            return availability
        else:
            print(f"❌ Failed to check availability: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error checking availability: {e}")
        return None

def update_user_preferences(user_id: int):
    """Update user preferences"""
    preferences = {
        "working_hours_start": 9,
        "working_hours_end": 17,
        "working_days": [1, 2, 3, 4, 5],  # Monday to Friday
        "preferred_meeting_duration": 30,
        "buffer_time_before": 10,
        "buffer_time_after": 5,
        "max_meetings_per_day": 6,
        "preferred_meeting_times": ["morning", "afternoon"],
        "avoid_lunch_hours": True,
        "lunch_start": 12,
        "lunch_end": 13,
        "advance_notice_hours": 24,
        "enable_ai_suggestions": True,
        "ai_learning_consent": True,
        "suggestion_aggressiveness": "moderate"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/preferences/{user_id}", json=preferences)
        if response.status_code == 200:
            print(f"✅ Updated preferences for user {user_id}")
            return response.json()
        else:
            print(f"❌ Failed to update preferences: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error updating preferences: {e}")
        return None

def main():
    """Main example workflow"""
    print("🤖 AI-Powered Meeting Scheduler - Example Usage")
    print("=" * 50)
    
    # Step 1: Create sample users
    print("\n1. Creating sample users...")
    users = create_sample_users()
    
    if not users:
        print("❌ Failed to create users. Exiting.")
        return
    
    # Step 2: Update preferences for first user
    print("\n2. Setting up user preferences...")
    update_user_preferences(users[0]['id'])
    
    # Step 3: Check availability
    print("\n3. Checking user availability...")
    check_availability(users[0]['id'])
    
    # Step 4: Create scheduling request
    print("\n4. Creating scheduling request...")
    request = create_scheduling_request(users[0]['id'])
    
    if not request:
        print("❌ Failed to create scheduling request. Exiting.")
        return
    
    # Step 5: Get AI suggestions
    print("\n5. Getting AI-powered suggestions...")
    suggestions = get_ai_suggestions(request['id'])
    
    if not suggestions or not suggestions['suggestions']:
        print("❌ No suggestions available. Exiting.")
        return
    
    # Step 6: Confirm the best suggestion
    print("\n6. Confirming the top AI suggestion...")
    meeting = confirm_meeting(request['id'], 0)
    
    if meeting:
        print("\n🎉 Successfully scheduled meeting using AI optimization!")
        print(f"The AI system analyzed participant availability and preferences")
        print(f"to suggest the optimal time with {meeting['ai_confidence_score']}% confidence.")
    
    print("\n" + "=" * 50)
    print("✅ Example workflow completed!")

if __name__ == "__main__":
    print("Make sure the API server is running on http://localhost:8000")
    print("Start the server with: python main.py")
    print()
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/../health")
        if response.status_code == 200:
            main()
        else:
            print("❌ API server is not responding. Please start the server first.")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Please start the server first.")
        print("Run: python main.py")


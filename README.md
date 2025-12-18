# AI-Powered Meeting Scheduler

An intelligent meeting scheduling system that uses AI/ML to automatically suggest optimal meeting times based on participants' availability, preferences, and past behavior patterns.

## 🚀 Features

### Core Functionality
- **Smart Availability Analysis** - Multi-participant calendar analysis with timezone handling
- **AI-Powered Optimization** - Machine learning models for preference learning and optimal time suggestions
- **External Calendar Integration** - Support for Google Calendar, Outlook, and other providers
- **Flexible Preference System** - Both explicit user preferences and implicit behavior learning
- **Real-time Scheduling** - Dynamic availability checking and instant suggestions

### AI/ML Components
- **Preference Learning** - Collaborative filtering to understand user scheduling patterns
- **Time Optimization** - ML models to suggest optimal meeting times based on historical success
- **Behavior Tracking** - System learns from user interactions to improve suggestions over time
- **Confidence Scoring** - Each suggestion includes a confidence score based on multiple factors

## 🏗️ Architecture

```
├── app/
│   ├── api/           # FastAPI route handlers
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic schemas for API serialization
│   ├── services/      # Business logic and external integrations
│   ├── ml/           # Machine learning components
│   ├── core/         # Configuration and utilities
│   └── utils/        # Helper functions
├── tests/            # Test suite
└── main.py          # FastAPI application entry point
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.8+)
- **Database**: SQLAlchemy with PostgreSQL/SQLite
- **AI/ML**: Scikit-learn, Pandas, NumPy
- **Calendar Integration**: Google Calendar API, Microsoft Graph API
- **Authentication**: OAuth2
- **Caching**: Redis (optional)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-meeting-scheduler
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 🔧 Configuration

Key environment variables:

```env
# Database
DATABASE_URL=sqlite:///./meeting_scheduler.db

# Google Calendar API
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Microsoft Graph API
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret

# AI/ML Settings
ENABLE_AI_SUGGESTIONS=true
ML_MODEL_PATH=./models
MIN_TRAINING_DATA_POINTS=10
```

## 📚 API Usage

### 1. Create a Scheduling Request

```bash
POST /api/v1/meetings/schedule
{
  "title": "Team Standup",
  "description": "Daily team synchronization",
  "duration_minutes": 30,
  "participant_emails": ["alice@company.com", "bob@company.com"],
  "requester_id": 1,
  "earliest_date": "2024-01-15T09:00:00Z",
  "latest_date": "2024-01-19T17:00:00Z"
}
```

### 2. Get AI-Powered Suggestions

```bash
GET /api/v1/meetings/suggestions/1
```

Response:
```json
{
  "request_id": 1,
  "suggestions": [
    {
      "start_time": "2024-01-15T10:00:00Z",
      "end_time": "2024-01-15T10:30:00Z",
      "confidence_score": 95,
      "participants_available": [1, 2],
      "reasoning": "High confidence based on historical success patterns. Morning time slot preferred by most users. All participants available."
    }
  ],
  "generated_at": "2024-01-14T15:30:00Z",
  "total_participants": 2
}
```

### 3. Confirm Meeting

```bash
POST /api/v1/meetings/confirm/1?suggestion_index=0
```

## 🤖 AI/ML Features

### Time Optimization Algorithm

The system uses a Random Forest model trained on historical scheduling data to predict the success probability of different time slots. Features include:

- **Temporal Features**: Hour of day, day of week, month
- **Availability Features**: Participant availability percentage, timezone spread
- **Historical Features**: Success rates for similar time slots
- **Preference Features**: User-specific time preferences
- **Contextual Features**: Meeting duration, participant count

### Learning from User Behavior

The system continuously learns from:
- **Meeting Confirmations**: Which suggested times users actually select
- **Meeting Outcomes**: Whether meetings happen as scheduled
- **Preference Updates**: Explicit preference changes by users
- **Response Patterns**: How quickly users respond to different time suggestions

## 🔌 Calendar Integration

### Supported Providers
- **Google Calendar** - Full OAuth2 integration
- **Microsoft Outlook** - Graph API integration
- **Mock Service** - For development and testing

### Integration Features
- **Real-time Availability** - Fetch current calendar events
- **Conflict Detection** - Identify scheduling conflicts
- **Event Creation** - Automatically create calendar events
- **Free/Busy Information** - Get availability without event details

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 🚀 Deployment

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t ai-meeting-scheduler .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

### Production Considerations

- Use PostgreSQL for production database
- Set up Redis for caching and session storage
- Configure proper OAuth2 credentials
- Set up monitoring and logging
- Use HTTPS in production
- Configure rate limiting

## 📈 Performance

### Optimization Features
- **Database Indexing** - Optimized queries for availability checking
- **Caching** - Redis caching for frequently accessed data
- **Async Processing** - Non-blocking calendar API calls
- **Batch Operations** - Efficient multi-participant processing

### Scalability
- **Horizontal Scaling** - Stateless API design
- **Database Optimization** - Efficient schema and queries
- **ML Model Caching** - Pre-trained models loaded in memory
- **Rate Limiting** - Protect against API abuse

## 🔒 Security

- **OAuth2 Authentication** - Secure calendar access
- **Data Encryption** - Sensitive data encrypted at rest
- **API Rate Limiting** - Prevent abuse
- **Input Validation** - Comprehensive request validation
- **Privacy Controls** - User consent for AI learning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API examples

---

**Built with ❤️ using FastAPI and AI/ML technologies**


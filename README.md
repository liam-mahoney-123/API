# ClickUp Codegen Agent

A powerful AI-powered agent that integrates with ClickUp to automatically generate code based on task requirements. The agent monitors ClickUp tasks, processes code generation requests using AI providers (OpenAI/Anthropic), and provides results back to ClickUp with generated code, explanations, and file attachments.

## Features

🤖 **AI-Powered Code Generation**
- Support for OpenAI GPT and Anthropic Claude models
- Intelligent requirements analysis and code review
- Multi-language support (Python, JavaScript, TypeScript, Java, Go, Rust, etc.)
- Framework-aware generation (React, Django, Flask, Express, etc.)

📋 **ClickUp Integration**
- Automatic task monitoring and processing
- Task status updates and progress tracking
- Comment generation with explanations and suggestions
- File attachment creation for generated code
- Custom field and tag support

🔄 **Robust Processing**
- Asynchronous task processing with concurrency limits
- Comprehensive error handling and retry logic
- Database persistence for task history and metrics
- Real-time monitoring and health checks

🌐 **Web API Interface**
- RESTful API for manual task submission
- Real-time metrics and status monitoring
- Agent control (start/stop) endpoints
- Health check and configuration endpoints

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd clickup-codegen-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# ClickUp Configuration
CLICKUP_API_TOKEN=your_clickup_api_token_here
CLICKUP_TEAM_ID=your_team_id_here
CLICKUP_SPACE_ID=your_space_id_here  # Optional

# AI Provider (choose one)
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Agent Configuration
AGENT_NAME=CodegenAgent
POLLING_INTERVAL=30
MAX_CONCURRENT_TASKS=5
```

### 3. Running the Agent

#### Command Line Interface
```bash
python -m src.agent
```

#### Web API Server
```bash
python -m src.api
# Or using uvicorn directly:
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

### ClickUp Task Processing

The agent automatically processes ClickUp tasks that meet certain criteria:

1. **Task Assignment**: Tasks assigned to the agent user
2. **Tags**: Tasks with tags like `codegen`, `ai-agent`, or `code-generation`
3. **Keywords**: Tasks with titles/descriptions containing keywords like "generate code", "implement", "create function"

### Task Requirements Format

Structure your ClickUp task descriptions for best results:

```markdown
# Task Title: Create User Authentication System

## Description
Implement a secure user authentication system with login, registration, and password reset functionality.

## Requirements
- User registration with email validation
- Secure password hashing (bcrypt)
- JWT token-based authentication
- Password reset via email
- Rate limiting for login attempts
- Input validation and sanitization

## Technical Details
- Language: Python
- Framework: Flask
- Database: PostgreSQL
```

### Custom Fields Support

The agent recognizes these custom fields in ClickUp:
- **Programming Language**: Specify the target language
- **Framework**: Specify the framework to use
- **File Paths**: Target file locations for generated code

### API Usage

#### Submit Manual Task
```bash
curl -X POST "http://localhost:8000/tasks/manual" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Create REST API endpoint",
    "description": "Create a REST API endpoint for user management",
    "requirements": [
      "GET /users - List all users",
      "POST /users - Create new user",
      "PUT /users/{id} - Update user",
      "DELETE /users/{id} - Delete user"
    ],
    "programming_language": "python",
    "framework": "fastapi",
    "priority": "high"
  }'
```

#### Check Task Status
```bash
curl "http://localhost:8000/tasks/{task_id}/status"
```

#### Get Agent Metrics
```bash
curl "http://localhost:8000/metrics"
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   ClickUp API   │◄──►│  Codegen Agent   │◄──►│   AI Provider   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Database     │
                       │   (SQLite/PG)   │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Web API       │
                       │   (FastAPI)     │
                       └─────────────────┘
```

### Core Components

- **Agent**: Main orchestrator that monitors ClickUp and processes tasks
- **ClickUp Client**: Handles all ClickUp API interactions
- **AI Providers**: Abstraction layer for OpenAI/Anthropic integration
- **Task Processor**: Core logic for analyzing requirements and generating code
- **Database Manager**: Persistence layer for tasks, metrics, and history
- **Web API**: RESTful interface for monitoring and manual task submission

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `CLICKUP_API_TOKEN` | ClickUp API token | Required |
| `CLICKUP_TEAM_ID` | ClickUp team/workspace ID | Required |
| `CLICKUP_SPACE_ID` | Specific space to monitor (optional) | All spaces |
| `OPENAI_API_KEY` | OpenAI API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic API key | Optional |
| `AGENT_NAME` | Agent display name | CodegenAgent |
| `POLLING_INTERVAL` | Task polling interval (seconds) | 30 |
| `MAX_CONCURRENT_TASKS` | Maximum concurrent tasks | 5 |
| `DATABASE_URL` | Database connection URL | sqlite:///./agent_tasks.db |
| `LOG_LEVEL` | Logging level | INFO |

## Development

### Project Structure

```
src/
├── __init__.py
├── agent.py           # Main agent class
├── api.py            # FastAPI web interface
├── clickup_client.py # ClickUp API client
├── ai_providers.py   # AI provider integrations
├── task_processor.py # Task processing logic
├── database.py       # Database management
├── models.py         # Data models
└── config.py         # Configuration management

tests/
├── test_agent.py
├── test_clickup_client.py
├── test_ai_providers.py
└── test_task_processor.py
```

### Running Tests

```bash
pytest tests/ -v
```

### Adding New AI Providers

1. Implement the `AIProvider` abstract base class
2. Add the provider to `AIProviderFactory`
3. Update configuration and documentation

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Update documentation
4. Submit pull request

## Monitoring and Metrics

The agent provides comprehensive monitoring capabilities:

### Metrics Tracked
- Task completion rates and success rates
- Average execution times
- Generated code statistics (lines, files)
- Error rates and failure analysis
- System resource usage

### Health Checks
- ClickUp API connectivity
- AI provider availability
- Database connection status
- Active task monitoring

### Logging
- Structured logging with configurable levels
- Task processing traces
- Error tracking and debugging
- Performance monitoring

## Troubleshooting

### Common Issues

**Agent not processing tasks:**
- Verify ClickUp API token and permissions
- Check task assignment and tags
- Review agent logs for errors

**AI generation failures:**
- Verify API keys are valid and have credits
- Check rate limits and quotas
- Review task requirements for clarity

**Database errors:**
- Ensure database file permissions
- Check disk space availability
- Verify connection string format

**Performance issues:**
- Adjust `MAX_CONCURRENT_TASKS` setting
- Monitor system resources
- Review task complexity and requirements

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python -m src.agent
```

## Security Considerations

- Store API keys securely using environment variables
- Use HTTPS for all external API communications
- Implement proper input validation and sanitization
- Regular security updates for dependencies
- Monitor for potential code injection in generated output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Update documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the logs for error details

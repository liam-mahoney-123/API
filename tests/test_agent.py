"""Tests for the main agent functionality."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from src.agent import CodegenAgent
from src.models import ClickUpTask, TaskStatus


@pytest.fixture
def mock_clickup_task():
    """Create a mock ClickUp task for testing."""
    return ClickUpTask(
        id="test_task_123",
        name="Test Code Generation Task",
        description="Generate a Python function to calculate fibonacci numbers",
        status="open",
        priority="normal",
        assignees=[{"id": "user_123", "username": "testuser"}],
        due_date=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        url="https://app.clickup.com/t/test_task_123",
        custom_fields={},
        tags=["codegen", "python"]
    )


@pytest.fixture
def mock_agent():
    """Create a mock agent for testing."""
    with patch('src.agent.ClickUpClient'), \
         patch('src.agent.AIProviderFactory'), \
         patch('src.agent.TaskProcessor'), \
         patch('src.agent.DatabaseManager'):
        agent = CodegenAgent()
        agent.clickup_client = Mock()
        agent.ai_provider = Mock()
        agent.task_processor = Mock()
        agent.db_manager = Mock()
        return agent


class TestCodegenAgent:
    """Test cases for the CodegenAgent class."""
    
    def test_agent_initialization(self, mock_agent):
        """Test agent initialization."""
        assert mock_agent.active_tasks == {}
        assert mock_agent.is_running is False
    
    def test_is_task_for_agent_with_tags(self, mock_agent, mock_clickup_task):
        """Test task filtering by tags."""
        # Task with codegen tag should be processed
        mock_clickup_task.tags = ["codegen"]
        assert mock_agent._is_task_for_agent(mock_clickup_task) is True
        
        # Task without relevant tags should not be processed
        mock_clickup_task.tags = ["bug", "frontend"]
        assert mock_agent._is_task_for_agent(mock_clickup_task) is False
    
    def test_is_task_for_agent_with_keywords(self, mock_agent, mock_clickup_task):
        """Test task filtering by keywords."""
        # Task with relevant keywords should be processed
        mock_clickup_task.name = "Generate code for user authentication"
        mock_clickup_task.tags = []
        assert mock_agent._is_task_for_agent(mock_clickup_task) is True
        
        # Task without relevant keywords should not be processed
        mock_clickup_task.name = "Fix bug in login form"
        mock_clickup_task.description = "The login form has a styling issue"
        assert mock_agent._is_task_for_agent(mock_clickup_task) is False
    
    def test_extract_requirements(self, mock_agent):
        """Test requirements extraction from task description."""
        description = """
        Create a user management system with the following features:
        - User registration with email validation
        - Password hashing using bcrypt
        - JWT token authentication
        - User profile management
        
        Additional requirement: The system should handle rate limiting.
        """
        
        requirements = mock_agent._extract_requirements(description)
        
        assert len(requirements) >= 4
        assert any("User registration" in req for req in requirements)
        assert any("Password hashing" in req for req in requirements)
        assert any("JWT token" in req for req in requirements)
    
    def test_create_codegen_request(self, mock_agent, mock_clickup_task):
        """Test creation of codegen request from ClickUp task."""
        mock_clickup_task.tags = ["python", "flask"]
        mock_clickup_task.description = "- Create REST API\n- Add authentication\n- Include error handling"
        
        request = mock_agent._create_codegen_request(mock_clickup_task)
        
        assert request.task_id == mock_clickup_task.id
        assert request.title == mock_clickup_task.name
        assert len(request.requirements) == 3
        assert "python" in [tag.lower() for tag in mock_clickup_task.tags]
    
    @pytest.mark.asyncio
    async def test_handle_new_task_already_processing(self, mock_agent, mock_clickup_task):
        """Test handling of task that's already being processed."""
        # Add task to active tasks
        mock_agent.active_tasks[mock_clickup_task.id] = Mock()
        
        # Mock the task filtering to return True
        mock_agent._is_task_for_agent = Mock(return_value=True)
        
        # Should not create new task
        await mock_agent._handle_new_task(mock_clickup_task)
        
        # Verify no new processing was started
        assert len(mock_agent.active_tasks) == 1
    
    @pytest.mark.asyncio
    async def test_handle_new_task_max_concurrent_reached(self, mock_agent, mock_clickup_task):
        """Test handling when max concurrent tasks is reached."""
        # Fill up active tasks to max capacity
        from src.config import settings
        for i in range(settings.max_concurrent_tasks):
            mock_agent.active_tasks[f"task_{i}"] = Mock()
        
        # Mock the task filtering to return True
        mock_agent._is_task_for_agent = Mock(return_value=True)
        
        # Should not process new task
        await mock_agent._handle_new_task(mock_clickup_task)
        
        # Verify task was not added
        assert mock_clickup_task.id not in mock_agent.active_tasks
    
    @pytest.mark.asyncio
    async def test_process_task_success(self, mock_agent, mock_clickup_task):
        """Test successful task processing."""
        # Mock dependencies
        mock_agent.clickup_client.update_task_status = Mock(return_value=True)
        mock_agent.clickup_client.add_task_comment = Mock(return_value=True)
        mock_agent.db_manager.create_task = AsyncMock(return_value=Mock(id=1))
        mock_agent.db_manager.update_task_result = AsyncMock()
        
        # Mock task processor
        from src.models import CodegenTaskResponse
        mock_response = CodegenTaskResponse(
            task_id=mock_clickup_task.id,
            status=TaskStatus.COMPLETED,
            generated_code="def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
            execution_time=2.5
        )
        mock_agent.task_processor.process_task = AsyncMock(return_value=mock_response)
        mock_agent._update_clickup_task = AsyncMock()
        
        # Process the task
        await mock_agent._process_task(mock_clickup_task)
        
        # Verify interactions
        mock_agent.clickup_client.update_task_status.assert_called()
        mock_agent.clickup_client.add_task_comment.assert_called()
        mock_agent.db_manager.create_task.assert_called_once()
        mock_agent.task_processor.process_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_task_failure(self, mock_agent, mock_clickup_task):
        """Test task processing failure handling."""
        # Mock dependencies to raise exception
        mock_agent.clickup_client.update_task_status = Mock(return_value=True)
        mock_agent.clickup_client.add_task_comment = Mock(return_value=True)
        mock_agent.db_manager.create_task = AsyncMock(side_effect=Exception("Database error"))
        
        # Process the task (should handle exception)
        await mock_agent._process_task(mock_clickup_task)
        
        # Verify error handling
        mock_agent.clickup_client.update_task_status.assert_called_with(mock_clickup_task.id, "failed")
        mock_agent.clickup_client.add_task_comment.assert_called()
    
    @pytest.mark.asyncio
    async def test_get_lists_to_monitor_with_space_id(self, mock_agent):
        """Test getting lists to monitor when space ID is configured."""
        with patch('src.config.settings') as mock_settings:
            mock_settings.clickup_space_id = "space_123"
            mock_agent.clickup_client.get_lists = Mock(return_value=[
                {"id": "list_1", "name": "Development"},
                {"id": "list_2", "name": "Code Review"}
            ])
            
            lists = await mock_agent._get_lists_to_monitor()
            
            assert lists == ["list_1", "list_2"]
            mock_agent.clickup_client.get_lists.assert_called_once_with("space_123")
    
    @pytest.mark.asyncio
    async def test_get_lists_to_monitor_all_spaces(self, mock_agent):
        """Test getting lists to monitor from all spaces."""
        with patch('src.config.settings') as mock_settings:
            mock_settings.clickup_space_id = None
            mock_settings.clickup_team_id = "team_123"
            
            mock_agent.clickup_client.get_spaces = Mock(return_value=[
                {"id": "space_1", "name": "Development"},
                {"id": "space_2", "name": "Testing"}
            ])
            mock_agent.clickup_client.get_lists = Mock(side_effect=[
                [{"id": "list_1"}, {"id": "list_2"}],
                [{"id": "list_3"}]
            ])
            
            lists = await mock_agent._get_lists_to_monitor()
            
            assert lists == ["list_1", "list_2", "list_3"]
            mock_agent.clickup_client.get_spaces.assert_called_once_with("team_123")
            assert mock_agent.clickup_client.get_lists.call_count == 2

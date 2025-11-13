"""Data models for the ClickUp Codegen Agent."""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class ClickUpTask(BaseModel):
    """ClickUp task model."""
    id: str
    name: str
    description: Optional[str] = None
    status: str
    priority: Optional[str] = None
    assignees: List[Dict[str, Any]] = []
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    url: str
    custom_fields: Dict[str, Any] = {}
    tags: List[str] = []


class CodegenTaskRequest(BaseModel):
    """Request model for codegen tasks."""
    task_id: str
    title: str
    description: str
    requirements: List[str] = []
    programming_language: Optional[str] = None
    framework: Optional[str] = None
    file_paths: List[str] = []
    priority: TaskPriority = TaskPriority.NORMAL
    deadline: Optional[datetime] = None
    context: Dict[str, Any] = {}


class CodegenTaskResponse(BaseModel):
    """Response model for codegen tasks."""
    task_id: str
    status: TaskStatus
    generated_code: Optional[str] = None
    file_changes: List[Dict[str, str]] = []
    explanation: Optional[str] = None
    suggestions: List[str] = []
    errors: List[str] = []
    execution_time: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentTask(Base):
    """Database model for agent tasks."""
    __tablename__ = "agent_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    clickup_task_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default=TaskStatus.PENDING)
    priority = Column(String, default=TaskPriority.NORMAL)
    
    # Task details
    requirements = Column(JSON)
    programming_language = Column(String)
    framework = Column(String)
    file_paths = Column(JSON)
    context = Column(JSON)
    
    # Results
    generated_code = Column(Text)
    file_changes = Column(JSON)
    explanation = Column(Text)
    suggestions = Column(JSON)
    errors = Column(JSON)
    
    # Metadata
    execution_time = Column(Integer)  # in seconds
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime)
    
    # ClickUp integration
    clickup_status = Column(String)
    last_synced_at = Column(DateTime)


class AgentMetrics(Base):
    """Database model for agent performance metrics."""
    __tablename__ = "agent_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Task metrics
    tasks_completed = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)
    average_execution_time = Column(Integer, default=0)  # in seconds
    
    # Performance metrics
    success_rate = Column(Integer, default=0)  # percentage
    total_lines_generated = Column(Integer, default=0)
    total_files_modified = Column(Integer, default=0)
    
    # System metrics
    cpu_usage = Column(Integer, default=0)  # percentage
    memory_usage = Column(Integer, default=0)  # MB
    active_tasks = Column(Integer, default=0)

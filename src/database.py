"""Database management for the ClickUp Codegen Agent."""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .config import settings
from .models import Base, AgentTask, AgentMetrics, TaskStatus, ClickUpTask, CodegenTaskResponse

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database operations for the agent."""
    
    def __init__(self):
        # Convert sync database URL to async if needed
        db_url = settings.database_url
        if db_url.startswith("sqlite:///"):
            db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
        elif db_url.startswith("mysql://"):
            db_url = db_url.replace("mysql://", "mysql+aiomysql://")
        
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def initialize(self):
        """Initialize the database."""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def create_task(self, clickup_task: ClickUpTask) -> AgentTask:
        """Create a new agent task from a ClickUp task."""
        try:
            async with self.async_session() as session:
                # Check if task already exists
                existing_task = await session.execute(
                    select(AgentTask).where(AgentTask.clickup_task_id == clickup_task.id)
                )
                existing_task = existing_task.scalar_one_or_none()
                
                if existing_task:
                    logger.debug(f"Task {clickup_task.id} already exists in database")
                    return existing_task
                
                # Create new task
                db_task = AgentTask(
                    clickup_task_id=clickup_task.id,
                    title=clickup_task.name,
                    description=clickup_task.description,
                    status=TaskStatus.PENDING,
                    clickup_status=clickup_task.status,
                    context={
                        "url": clickup_task.url,
                        "tags": clickup_task.tags,
                        "custom_fields": clickup_task.custom_fields,
                        "assignees": [{"id": a["id"], "username": a.get("username", "")} for a in clickup_task.assignees],
                        "due_date": clickup_task.due_date.isoformat() if clickup_task.due_date else None
                    }
                )
                
                session.add(db_task)
                await session.commit()
                await session.refresh(db_task)
                
                logger.info(f"Created database task for ClickUp task {clickup_task.id}")
                return db_task
                
        except Exception as e:
            logger.error(f"Failed to create task in database: {e}")
            raise
    
    async def update_task_status(self, task_id: int, status: TaskStatus, error_message: str = None):
        """Update task status in the database."""
        try:
            async with self.async_session() as session:
                stmt = (
                    update(AgentTask)
                    .where(AgentTask.id == task_id)
                    .values(
                        status=status,
                        updated_at=datetime.utcnow(),
                        completed_at=datetime.utcnow() if status in [TaskStatus.COMPLETED, TaskStatus.FAILED] else None,
                        errors=[error_message] if error_message else None
                    )
                )
                
                await session.execute(stmt)
                await session.commit()
                
                logger.debug(f"Updated task {task_id} status to {status}")
                
        except Exception as e:
            logger.error(f"Failed to update task status: {e}")
            raise
    
    async def update_task_result(self, task_id: int, response: CodegenTaskResponse):
        """Update task with processing results."""
        try:
            async with self.async_session() as session:
                stmt = (
                    update(AgentTask)
                    .where(AgentTask.id == task_id)
                    .values(
                        status=response.status,
                        generated_code=response.generated_code,
                        file_changes=response.file_changes,
                        explanation=response.explanation,
                        suggestions=response.suggestions,
                        errors=response.errors,
                        execution_time=int(response.execution_time) if response.execution_time else None,
                        updated_at=datetime.utcnow(),
                        completed_at=datetime.utcnow() if response.status in [TaskStatus.COMPLETED, TaskStatus.FAILED] else None
                    )
                )
                
                await session.execute(stmt)
                await session.commit()
                
                logger.debug(f"Updated task {task_id} with processing results")
                
        except Exception as e:
            logger.error(f"Failed to update task result: {e}")
            raise
    
    async def get_task_status(self, clickup_task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status by ClickUp task ID."""
        try:
            async with self.async_session() as session:
                result = await session.execute(
                    select(AgentTask).where(AgentTask.clickup_task_id == clickup_task_id)
                )
                task = result.scalar_one_or_none()
                
                if not task:
                    return None
                
                return {
                    "id": task.id,
                    "clickup_task_id": task.clickup_task_id,
                    "title": task.title,
                    "status": task.status,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "completed_at": task.completed_at,
                    "execution_time": task.execution_time,
                    "has_generated_code": bool(task.generated_code),
                    "has_file_changes": bool(task.file_changes),
                    "error_count": len(task.errors) if task.errors else 0
                }
                
        except Exception as e:
            logger.error(f"Failed to get task status: {e}")
            return None
    
    async def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get all active (in progress) tasks."""
        try:
            async with self.async_session() as session:
                result = await session.execute(
                    select(AgentTask).where(AgentTask.status == TaskStatus.IN_PROGRESS)
                )
                tasks = result.scalars().all()
                
                return [
                    {
                        "id": task.id,
                        "clickup_task_id": task.clickup_task_id,
                        "title": task.title,
                        "created_at": task.created_at,
                        "execution_time": task.execution_time
                    }
                    for task in tasks
                ]
                
        except Exception as e:
            logger.error(f"Failed to get active tasks: {e}")
            return []
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        try:
            async with self.async_session() as session:
                # Get task counts by status
                completed_result = await session.execute(
                    select(AgentTask).where(AgentTask.status == TaskStatus.COMPLETED)
                )
                completed_tasks = completed_result.scalars().all()
                
                failed_result = await session.execute(
                    select(AgentTask).where(AgentTask.status == TaskStatus.FAILED)
                )
                failed_tasks = failed_result.scalars().all()
                
                in_progress_result = await session.execute(
                    select(AgentTask).where(AgentTask.status == TaskStatus.IN_PROGRESS)
                )
                in_progress_tasks = in_progress_result.scalars().all()
                
                # Calculate metrics
                total_tasks = len(completed_tasks) + len(failed_tasks)
                success_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
                
                # Calculate average execution time
                execution_times = [task.execution_time for task in completed_tasks if task.execution_time]
                avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
                
                # Count generated files
                total_files_generated = 0
                total_lines_generated = 0
                
                for task in completed_tasks:
                    if task.file_changes:
                        total_files_generated += len(task.file_changes)
                    
                    if task.generated_code:
                        total_lines_generated += len(task.generated_code.split('\n'))
                
                return {
                    "total_tasks": total_tasks,
                    "completed_tasks": len(completed_tasks),
                    "failed_tasks": len(failed_tasks),
                    "active_tasks": len(in_progress_tasks),
                    "success_rate": round(success_rate, 2),
                    "average_execution_time": round(avg_execution_time, 2),
                    "total_files_generated": total_files_generated,
                    "total_lines_generated": total_lines_generated,
                    "last_updated": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {}
    
    async def cleanup_old_tasks(self, days: int = 30):
        """Clean up old completed tasks."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            async with self.async_session() as session:
                # Delete old completed tasks
                stmt = (
                    delete(AgentTask)
                    .where(
                        AgentTask.status.in_([TaskStatus.COMPLETED, TaskStatus.FAILED]),
                        AgentTask.completed_at < cutoff_date
                    )
                )
                
                result = await session.execute(stmt)
                await session.commit()
                
                logger.info(f"Cleaned up {result.rowcount} old tasks")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old tasks: {e}")
    
    async def save_metrics_snapshot(self):
        """Save current metrics as a snapshot."""
        try:
            metrics = await self.get_metrics()
            
            async with self.async_session() as session:
                snapshot = AgentMetrics(
                    date=datetime.utcnow(),
                    tasks_completed=metrics.get("completed_tasks", 0),
                    tasks_failed=metrics.get("failed_tasks", 0),
                    average_execution_time=int(metrics.get("average_execution_time", 0)),
                    success_rate=int(metrics.get("success_rate", 0)),
                    total_lines_generated=metrics.get("total_lines_generated", 0),
                    total_files_modified=metrics.get("total_files_generated", 0),
                    active_tasks=metrics.get("active_tasks", 0)
                )
                
                session.add(snapshot)
                await session.commit()
                
                logger.debug("Saved metrics snapshot")
                
        except Exception as e:
            logger.error(f"Failed to save metrics snapshot: {e}")
    
    async def close(self):
        """Close database connections."""
        await self.engine.dispose()
        logger.info("Database connections closed")

"""FastAPI web interface for the ClickUp Codegen Agent."""

import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .agent import CodegenAgent
from .models import TaskStatus, CodegenTaskRequest
from .config import settings

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ClickUp Codegen Agent API",
    description="API interface for the ClickUp Codegen Agent",
    version="1.0.0"
)

# Global agent instance
agent: Optional[CodegenAgent] = None


class TaskStatusResponse(BaseModel):
    """Response model for task status."""
    task_id: str
    status: str
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
    execution_time: Optional[int] = None
    has_generated_code: bool
    has_file_changes: bool
    error_count: int


class MetricsResponse(BaseModel):
    """Response model for agent metrics."""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    active_tasks: int
    success_rate: float
    average_execution_time: float
    total_files_generated: int
    total_lines_generated: int
    last_updated: str


class ManualTaskRequest(BaseModel):
    """Request model for manually submitting tasks."""
    title: str
    description: str
    requirements: List[str] = []
    programming_language: Optional[str] = None
    framework: Optional[str] = None
    file_paths: List[str] = []
    priority: str = "normal"


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    global agent
    try:
        agent = CodegenAgent()
        logger.info("Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    global agent
    if agent:
        await agent.stop()
        logger.info("Agent stopped")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ClickUp Codegen Agent API",
        "version": "1.0.0",
        "status": "running" if agent else "not initialized"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return {
        "status": "healthy",
        "agent_running": agent.is_running,
        "active_tasks": len(agent.active_tasks)
    }


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get agent performance metrics."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        metrics = await agent.get_agent_metrics()
        return MetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


@app.get("/tasks/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get the status of a specific task."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        status = await agent.get_task_status(task_id)
        if not status:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskStatusResponse(
            task_id=status["clickup_task_id"],
            status=status["status"],
            created_at=status["created_at"].isoformat(),
            updated_at=status["updated_at"].isoformat(),
            completed_at=status["completed_at"].isoformat() if status["completed_at"] else None,
            execution_time=status["execution_time"],
            has_generated_code=status["has_generated_code"],
            has_file_changes=status["has_file_changes"],
            error_count=status["error_count"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task status")


@app.get("/tasks/active")
async def get_active_tasks():
    """Get all currently active tasks."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        active_tasks = await agent.db_manager.get_active_tasks()
        return {"active_tasks": active_tasks}
    except Exception as e:
        logger.error(f"Failed to get active tasks: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve active tasks")


@app.post("/tasks/manual")
async def submit_manual_task(task_request: ManualTaskRequest, background_tasks: BackgroundTasks):
    """Manually submit a task for processing."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Generate a unique task ID for manual tasks
        import uuid
        task_id = f"manual_{uuid.uuid4().hex[:8]}"
        
        # Create a codegen request
        from .models import TaskPriority
        priority_map = {
            "low": TaskPriority.LOW,
            "normal": TaskPriority.NORMAL,
            "high": TaskPriority.HIGH,
            "urgent": TaskPriority.URGENT
        }
        
        request = CodegenTaskRequest(
            task_id=task_id,
            title=task_request.title,
            description=task_request.description,
            requirements=task_request.requirements,
            programming_language=task_request.programming_language,
            framework=task_request.framework,
            file_paths=task_request.file_paths,
            priority=priority_map.get(task_request.priority, TaskPriority.NORMAL),
            context={"source": "manual_api"}
        )
        
        # Process the task in the background
        background_tasks.add_task(agent.task_processor.process_task, request)
        
        return {
            "message": "Task submitted successfully",
            "task_id": task_id,
            "status": "queued"
        }
        
    except Exception as e:
        logger.error(f"Failed to submit manual task: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit task")


@app.post("/agent/start")
async def start_agent():
    """Start the agent monitoring."""
    global agent
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if agent.is_running:
        return {"message": "Agent is already running"}
    
    try:
        # Start agent in background
        import asyncio
        asyncio.create_task(agent.start())
        return {"message": "Agent started successfully"}
    except Exception as e:
        logger.error(f"Failed to start agent: {e}")
        raise HTTPException(status_code=500, detail="Failed to start agent")


@app.post("/agent/stop")
async def stop_agent():
    """Stop the agent monitoring."""
    global agent
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not agent.is_running:
        return {"message": "Agent is not running"}
    
    try:
        await agent.stop()
        return {"message": "Agent stopped successfully"}
    except Exception as e:
        logger.error(f"Failed to stop agent: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop agent")


@app.get("/config")
async def get_config():
    """Get current agent configuration (without sensitive data)."""
    return {
        "agent_name": settings.agent_name,
        "polling_interval": settings.polling_interval,
        "max_concurrent_tasks": settings.max_concurrent_tasks,
        "log_level": settings.log_level,
        "has_openai_key": bool(settings.openai_api_key),
        "has_anthropic_key": bool(settings.anthropic_api_key),
        "has_clickup_token": bool(settings.clickup_api_token),
        "clickup_team_id": settings.clickup_team_id,
        "clickup_space_id": settings.clickup_space_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
        reload=True
    )

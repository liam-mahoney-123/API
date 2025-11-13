"""Main ClickUp Codegen Agent implementation."""

import asyncio
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import settings
from .models import Base, AgentTask, TaskStatus, TaskPriority, ClickUpTask, CodegenTaskRequest, CodegenTaskResponse
from .clickup_client import ClickUpClient
from .ai_providers import AIProviderFactory, AIProvider
from .task_processor import TaskProcessor
from .database import DatabaseManager

logger = logging.getLogger(__name__)


class CodegenAgent:
    """Main ClickUp Codegen Agent class."""
    
    def __init__(self):
        self.clickup_client = ClickUpClient()
        self.ai_provider = AIProviderFactory.create_provider()
        self.task_processor = TaskProcessor(self.ai_provider)
        self.db_manager = DatabaseManager()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.is_running = False
        
    async def start(self):
        """Start the agent."""
        logger.info("Starting ClickUp Codegen Agent...")
        
        # Initialize database
        await self.db_manager.initialize()
        
        # Verify ClickUp connection
        user_info = self.clickup_client.get_user_info()
        if not user_info:
            raise RuntimeError("Failed to connect to ClickUp API")
        
        logger.info(f"Connected to ClickUp as: {user_info.get('username', 'Unknown')}")
        
        # Get monitoring configuration
        lists_to_monitor = await self._get_lists_to_monitor()
        if not lists_to_monitor:
            logger.warning("No lists configured for monitoring")
            return
        
        logger.info(f"Monitoring {len(lists_to_monitor)} lists")
        
        # Start task monitoring
        self.is_running = True
        await self.clickup_client.monitor_tasks(
            list_ids=lists_to_monitor,
            callback=self._handle_new_task,
            interval=settings.polling_interval
        )
    
    async def stop(self):
        """Stop the agent."""
        logger.info("Stopping ClickUp Codegen Agent...")
        self.is_running = False
        
        # Cancel all active tasks
        for task_id, task in self.active_tasks.items():
            logger.info(f"Cancelling task: {task_id}")
            task.cancel()
        
        # Wait for tasks to complete
        if self.active_tasks:
            await asyncio.gather(*self.active_tasks.values(), return_exceptions=True)
        
        logger.info("Agent stopped")
    
    async def _get_lists_to_monitor(self) -> List[str]:
        """Get list IDs to monitor based on configuration."""
        lists_to_monitor = []
        
        try:
            # If space ID is configured, get all lists in that space
            if settings.clickup_space_id:
                lists = self.clickup_client.get_lists(settings.clickup_space_id)
                lists_to_monitor.extend([lst["id"] for lst in lists])
            else:
                # Get all spaces in the team and their lists
                spaces = self.clickup_client.get_spaces(settings.clickup_team_id)
                for space in spaces:
                    lists = self.clickup_client.get_lists(space["id"])
                    lists_to_monitor.extend([lst["id"] for lst in lists])
            
        except Exception as e:
            logger.error(f"Failed to get lists to monitor: {e}")
        
        return lists_to_monitor
    
    async def _handle_new_task(self, clickup_task: ClickUpTask):
        """Handle a new or updated ClickUp task."""
        try:
            # Check if this task is assigned to the agent
            if not self._is_task_for_agent(clickup_task):
                return
            
            # Check if we're already processing this task
            if clickup_task.id in self.active_tasks:
                logger.debug(f"Task {clickup_task.id} is already being processed")
                return
            
            # Check if we've reached the maximum concurrent tasks
            if len(self.active_tasks) >= settings.max_concurrent_tasks:
                logger.warning(f"Maximum concurrent tasks reached ({settings.max_concurrent_tasks})")
                return
            
            logger.info(f"Processing new task: {clickup_task.name} ({clickup_task.id})")
            
            # Create async task for processing
            task = asyncio.create_task(self._process_task(clickup_task))
            self.active_tasks[clickup_task.id] = task
            
            # Add callback to clean up when done
            task.add_done_callback(lambda t: self.active_tasks.pop(clickup_task.id, None))
            
        except Exception as e:
            logger.error(f"Error handling new task {clickup_task.id}: {e}")
    
    def _is_task_for_agent(self, task: ClickUpTask) -> bool:
        """Check if a task should be processed by this agent."""
        # Check if task has specific tags indicating it's for the agent
        agent_tags = ["codegen", "ai-agent", "code-generation"]
        task_tags = [tag.lower() for tag in task.tags]
        
        if any(tag in task_tags for tag in agent_tags):
            return True
        
        # Check if task is assigned to the agent (if we have user info)
        user_info = self.clickup_client.get_user_info()
        if user_info:
            agent_user_id = str(user_info["id"])
            assignee_ids = [str(assignee["id"]) for assignee in task.assignees]
            if agent_user_id in assignee_ids:
                return True
        
        # Check task title/description for keywords
        keywords = ["generate code", "implement", "create function", "write script"]
        text_to_check = f"{task.name} {task.description or ''}".lower()
        
        return any(keyword in text_to_check for keyword in keywords)
    
    async def _process_task(self, clickup_task: ClickUpTask):
        """Process a single ClickUp task."""
        start_time = time.time()
        
        try:
            # Update task status to in progress
            self.clickup_client.update_task_status(clickup_task.id, "in progress")
            self.clickup_client.add_task_comment(
                clickup_task.id,
                f"🤖 {settings.agent_name} is now processing this task..."
            )
            
            # Save task to database
            db_task = await self.db_manager.create_task(clickup_task)
            
            # Convert to codegen request
            request = self._create_codegen_request(clickup_task)
            
            # Process the task
            response = await self.task_processor.process_task(request)
            
            # Update database
            await self.db_manager.update_task_result(db_task.id, response)
            
            # Update ClickUp task
            await self._update_clickup_task(clickup_task.id, response)
            
            execution_time = time.time() - start_time
            logger.info(f"Task {clickup_task.id} completed in {execution_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error processing task {clickup_task.id}: {e}")
            
            # Update task as failed
            self.clickup_client.update_task_status(clickup_task.id, "failed")
            self.clickup_client.add_task_comment(
                clickup_task.id,
                f"❌ Task processing failed: {str(e)}"
            )
            
            # Update database
            if 'db_task' in locals():
                await self.db_manager.update_task_status(db_task.id, TaskStatus.FAILED, str(e))
    
    def _create_codegen_request(self, clickup_task: ClickUpTask) -> CodegenTaskRequest:
        """Create a codegen request from a ClickUp task."""
        # Extract requirements from task description
        requirements = self._extract_requirements(clickup_task.description or "")
        
        # Extract programming language and framework from custom fields or tags
        programming_language = None
        framework = None
        
        for tag in clickup_task.tags:
            tag_lower = tag.lower()
            if tag_lower in ["python", "javascript", "java", "go", "rust", "typescript"]:
                programming_language = tag_lower
            elif tag_lower in ["react", "vue", "angular", "django", "flask", "express"]:
                framework = tag_lower
        
        # Check custom fields
        for field_name, field_value in clickup_task.custom_fields.items():
            if "language" in field_name.lower() and field_value:
                programming_language = field_value
            elif "framework" in field_name.lower() and field_value:
                framework = field_value
        
        # Determine priority
        priority = TaskPriority.NORMAL
        if clickup_task.priority:
            priority_map = {
                "urgent": TaskPriority.URGENT,
                "high": TaskPriority.HIGH,
                "normal": TaskPriority.NORMAL,
                "low": TaskPriority.LOW
            }
            priority = priority_map.get(clickup_task.priority.lower(), TaskPriority.NORMAL)
        
        return CodegenTaskRequest(
            task_id=clickup_task.id,
            title=clickup_task.name,
            description=clickup_task.description or "",
            requirements=requirements,
            programming_language=programming_language,
            framework=framework,
            priority=priority,
            deadline=clickup_task.due_date,
            context={
                "clickup_url": clickup_task.url,
                "tags": clickup_task.tags,
                "custom_fields": clickup_task.custom_fields
            }
        )
    
    def _extract_requirements(self, description: str) -> List[str]:
        """Extract requirements from task description."""
        if not description:
            return []
        
        requirements = []
        lines = description.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                requirements.append(line[1:].strip())
            elif line and any(keyword in line.lower() for keyword in ['requirement', 'need', 'should', 'must']):
                requirements.append(line)
        
        # If no structured requirements found, use the entire description
        if not requirements:
            requirements = [description]
        
        return requirements
    
    async def _update_clickup_task(self, task_id: str, response: CodegenTaskResponse):
        """Update ClickUp task with the processing results."""
        try:
            if response.status == TaskStatus.COMPLETED:
                # Update status to completed
                self.clickup_client.update_task_status(task_id, "complete")
                
                # Add success comment with results
                comment = f"✅ **Task completed successfully!**\n\n"
                
                if response.explanation:
                    comment += f"**Explanation:**\n{response.explanation}\n\n"
                
                if response.generated_code:
                    comment += f"**Generated Code:**\n```\n{response.generated_code[:1000]}{'...' if len(response.generated_code) > 1000 else ''}\n```\n\n"
                
                if response.suggestions:
                    comment += f"**Suggestions:**\n" + "\n".join([f"• {s}" for s in response.suggestions])
                
                self.clickup_client.add_task_comment(task_id, comment)
                
                # Create attachments for generated files
                if response.file_changes:
                    for file_change in response.file_changes:
                        if file_change.get("content"):
                            filename = file_change.get("filename", "generated_code.txt")
                            # Save file temporarily and attach
                            temp_path = f"/tmp/{filename}"
                            with open(temp_path, 'w') as f:
                                f.write(file_change["content"])
                            
                            self.clickup_client.create_task_attachment(task_id, temp_path, filename)
            
            elif response.status == TaskStatus.FAILED:
                self.clickup_client.update_task_status(task_id, "failed")
                
                error_comment = f"❌ **Task processing failed**\n\n"
                if response.errors:
                    error_comment += "**Errors:**\n" + "\n".join([f"• {e}" for e in response.errors])
                
                self.clickup_client.add_task_comment(task_id, error_comment)
            
        except Exception as e:
            logger.error(f"Failed to update ClickUp task {task_id}: {e}")
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task."""
        return await self.db_manager.get_task_status(task_id)
    
    async def get_agent_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        return await self.db_manager.get_metrics()


# CLI interface
async def main():
    """Main entry point for the agent."""
    import logging
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )
    
    agent = CodegenAgent()
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Agent failed: {e}")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())

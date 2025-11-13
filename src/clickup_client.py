"""ClickUp API client for the Codegen Agent."""

import asyncio
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import settings
from .models import ClickUpTask

logger = logging.getLogger(__name__)


class ClickUpClient:
    """Client for interacting with ClickUp API."""
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or settings.clickup_api_token
        self.base_url = "https://api.clickup.com/api/v2"
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        })
        
        return session
    
    def get_teams(self) -> List[Dict[str, Any]]:
        """Get all teams for the authenticated user."""
        try:
            response = self.session.get(f"{self.base_url}/team")
            response.raise_for_status()
            return response.json().get("teams", [])
        except requests.RequestException as e:
            logger.error(f"Failed to get teams: {e}")
            return []
    
    def get_spaces(self, team_id: str) -> List[Dict[str, Any]]:
        """Get all spaces for a team."""
        try:
            response = self.session.get(f"{self.base_url}/team/{team_id}/space")
            response.raise_for_status()
            return response.json().get("spaces", [])
        except requests.RequestException as e:
            logger.error(f"Failed to get spaces for team {team_id}: {e}")
            return []
    
    def get_lists(self, space_id: str) -> List[Dict[str, Any]]:
        """Get all lists in a space."""
        try:
            response = self.session.get(f"{self.base_url}/space/{space_id}/list")
            response.raise_for_status()
            return response.json().get("lists", [])
        except requests.RequestException as e:
            logger.error(f"Failed to get lists for space {space_id}: {e}")
            return []
    
    def get_tasks(self, list_id: str, assignee_id: Optional[str] = None) -> List[ClickUpTask]:
        """Get tasks from a list, optionally filtered by assignee."""
        try:
            params = {}
            if assignee_id:
                params["assignees[]"] = assignee_id
                
            response = self.session.get(
                f"{self.base_url}/list/{list_id}/task",
                params=params
            )
            response.raise_for_status()
            
            tasks_data = response.json().get("tasks", [])
            tasks = []
            
            for task_data in tasks_data:
                try:
                    task = self._parse_task(task_data)
                    tasks.append(task)
                except Exception as e:
                    logger.warning(f"Failed to parse task {task_data.get('id', 'unknown')}: {e}")
                    
            return tasks
            
        except requests.RequestException as e:
            logger.error(f"Failed to get tasks for list {list_id}: {e}")
            return []
    
    def get_task(self, task_id: str) -> Optional[ClickUpTask]:
        """Get a specific task by ID."""
        try:
            response = self.session.get(f"{self.base_url}/task/{task_id}")
            response.raise_for_status()
            
            task_data = response.json()
            return self._parse_task(task_data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to get task {task_id}: {e}")
            return None
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update the status of a task."""
        try:
            data = {"status": status}
            response = self.session.put(
                f"{self.base_url}/task/{task_id}",
                json=data
            )
            response.raise_for_status()
            logger.info(f"Updated task {task_id} status to {status}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to update task {task_id} status: {e}")
            return False
    
    def add_task_comment(self, task_id: str, comment: str) -> bool:
        """Add a comment to a task."""
        try:
            data = {"comment_text": comment}
            response = self.session.post(
                f"{self.base_url}/task/{task_id}/comment",
                json=data
            )
            response.raise_for_status()
            logger.info(f"Added comment to task {task_id}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to add comment to task {task_id}: {e}")
            return False
    
    def create_task_attachment(self, task_id: str, file_path: str, filename: str) -> bool:
        """Create an attachment for a task."""
        try:
            with open(file_path, 'rb') as file:
                files = {'attachment': (filename, file)}
                response = self.session.post(
                    f"{self.base_url}/task/{task_id}/attachment",
                    files=files
                )
                response.raise_for_status()
                logger.info(f"Added attachment {filename} to task {task_id}")
                return True
                
        except (requests.RequestException, IOError) as e:
            logger.error(f"Failed to add attachment to task {task_id}: {e}")
            return False
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the authenticated user."""
        try:
            response = self.session.get(f"{self.base_url}/user")
            response.raise_for_status()
            return response.json().get("user")
            
        except requests.RequestException as e:
            logger.error(f"Failed to get user info: {e}")
            return None
    
    def _parse_task(self, task_data: Dict[str, Any]) -> ClickUpTask:
        """Parse task data from ClickUp API response."""
        # Parse dates
        created_at = datetime.fromtimestamp(int(task_data["date_created"]) / 1000)
        updated_at = datetime.fromtimestamp(int(task_data["date_updated"]) / 1000)
        
        due_date = None
        if task_data.get("due_date"):
            due_date = datetime.fromtimestamp(int(task_data["due_date"]) / 1000)
        
        # Parse custom fields
        custom_fields = {}
        for field in task_data.get("custom_fields", []):
            custom_fields[field["name"]] = field.get("value")
        
        # Parse tags
        tags = [tag["name"] for tag in task_data.get("tags", [])]
        
        return ClickUpTask(
            id=task_data["id"],
            name=task_data["name"],
            description=task_data.get("description", ""),
            status=task_data["status"]["status"],
            priority=task_data.get("priority", {}).get("priority"),
            assignees=task_data.get("assignees", []),
            due_date=due_date,
            created_at=created_at,
            updated_at=updated_at,
            url=task_data["url"],
            custom_fields=custom_fields,
            tags=tags
        )
    
    async def monitor_tasks(self, list_ids: List[str], callback, interval: int = 30):
        """Monitor tasks in specified lists and call callback for new/updated tasks."""
        logger.info(f"Starting task monitoring for lists: {list_ids}")
        known_tasks = set()
        
        while True:
            try:
                for list_id in list_ids:
                    tasks = self.get_tasks(list_id)
                    
                    for task in tasks:
                        task_key = f"{task.id}_{task.updated_at.timestamp()}"
                        
                        if task_key not in known_tasks:
                            known_tasks.add(task_key)
                            await callback(task)
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in task monitoring: {e}")
                await asyncio.sleep(interval)

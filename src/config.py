"""Configuration management for the ClickUp Codegen Agent."""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # ClickUp Configuration
    clickup_api_token: str = Field(..., env="CLICKUP_API_TOKEN")
    clickup_team_id: str = Field(..., env="CLICKUP_TEAM_ID")
    clickup_space_id: Optional[str] = Field(None, env="CLICKUP_SPACE_ID")
    
    # AI Provider Configuration
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Agent Configuration
    agent_name: str = Field("CodegenAgent", env="AGENT_NAME")
    polling_interval: int = Field(30, env="POLLING_INTERVAL")
    max_concurrent_tasks: int = Field(5, env="MAX_CONCURRENT_TASKS")
    
    # Database Configuration
    database_url: str = Field("sqlite:///./agent_tasks.db", env="DATABASE_URL")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("agent.log", env="LOG_FILE")
    
    # GitHub Integration (optional)
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    github_repo_owner: Optional[str] = Field(None, env="GITHUB_REPO_OWNER")
    github_repo_name: Optional[str] = Field(None, env="GITHUB_REPO_NAME")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

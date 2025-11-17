"""
Configuration management for the Code Review Assistant.

This module loads all configuration from environment variables and a .env file,
using Pydantic for validation.
"""

import os
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, model_validator
import google.auth
from google.auth.exceptions import DefaultCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentConfig(BaseSettings):
    """
    Defines and validates all configuration settings for the application.
    Loads values from a .env file and environment variables.
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    # --- Google Cloud Configuration ---
    google_cloud_project: Optional[str] = Field(
        default=None, description="GCP project ID, auto-detected if not set."
    )
    google_cloud_location: str = Field(
        default="us-central1", description="GCP region for deployments."
    )

    # --- Cloud Run Database Configuration (for cloud-run deployment) ---
    cloud_sql_instance_name: Optional[str] = Field(
        default=None, description="The name of the Cloud SQL instance."
    )
    db_user: Optional[str] = Field(
        default=None, description="The username for the database."
    )
    db_password: Optional[str] = Field(
        default=None, description="The password for the database user."
    )
    db_name: Optional[str] = Field(
        default=None, description="The name of the database."
    )

    # --- Agent Engine Configuration (for agent-engine deployment) ---
    agent_engine_id: Optional[str] = Field(
        default=None, description="ID of the deployed Vertex AI Agent Engine."
    )
    staging_bucket: Optional[str] = Field(
        default=None, description="GCS staging bucket for Agent Engine deployments."
    )

    # --- Artifact Storage Configuration ---
    artifact_bucket: Optional[str] = Field(
        default=None, description="GCS bucket for artifact storage (e.g., 'your-project-artifacts')"
    )

    # --- Model Configuration ---
    google_genai_use_vertexai: bool = Field(
        default=True, description="Use Vertex AI (True) or Google AI Studio (False)."
    )
    google_api_key: Optional[str] = Field(
        default=None, description="API key for Google AI Studio (if not using Vertex AI)."
    )
    # Using -latest tags is a best practice to stay current.
    worker_model: str = Field(
        default="gemini-2.5-flash", description="Model for fast analysis tasks."
    )
    critic_model: str = Field(
        default="gemini-2.5-pro", description="Advanced model for nuanced feedback."
    )

    # --- Grading Parameters ---
    passing_score_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    style_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    test_weight: float = Field(default=0.5, ge=0.0, le=1.0)
    structure_weight: float = Field(default=0.2, ge=0.0, le=1.0)

    # --- Application Limits ---
    max_grading_attempts: int = Field(default=3, gt=0)

    # --- Logging & Debugging ---
    log_level: str = Field(default="INFO")
    debug_mode: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_weights(self):
        """Ensure grading weights sum to 1.0."""
        total = self.style_weight + self.test_weight + self.structure_weight
        if abs(total - 1.0) > 0.001:  # Allow for float precision issues
            raise ValueError(f"Grading weights must sum to 1.0, but got {total}")
        return self

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is a valid choice."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log_level: {v}. Must be one of {valid_levels}")
        return v.upper()

    @field_validator('google_cloud_project', mode='before')
    @classmethod
    def set_google_cloud_project(cls, v: Optional[str]) -> Optional[str]:
        """Try to auto-detect GCP project if not explicitly set."""
        if v:
            return v
        try:
            _, project_id = google.auth.default()
            if project_id:
                logger.info(f"Auto-detected GCP project: {project_id}")
                return project_id
        except (DefaultCredentialsError, FileNotFoundError):
            if os.getenv('K_SERVICE'): # Check if running in Cloud Run
                logger.warning("Running in a cloud environment but GOOGLE_CLOUD_PROJECT is not set.")
        return None

# --- Global Configuration Instance ---
# This single instance is imported and used throughout the application.
config = AgentConfig()

# Configure the root logger based on the loaded settings.
logging.getLogger().setLevel(config.log_level)
logger.info("Logging configured to level: %s", config.log_level)

# Set environment variables that the underlying ADK or Google Cloud libraries may expect.
# This ensures consistency even if other libraries read from the environment directly.
if config.google_cloud_project:
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", config.google_cloud_project)
if config.google_cloud_location:
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", config.google_cloud_location)
if config.google_api_key:
    os.environ.setdefault("GOOGLE_API_KEY", config.google_api_key)

# Log a summary of the most important configuration values on startup.
logger.info("Code Review Assistant Configuration Loaded:")
logger.info(f"  - GCP Project: {config.google_cloud_project or 'Not set'}")
logger.info(f"  - Artifact Bucket: {config.artifact_bucket or 'In-memory (local only)'}")
logger.info(f"  - Models: worker={config.worker_model}, critic={config.critic_model}")
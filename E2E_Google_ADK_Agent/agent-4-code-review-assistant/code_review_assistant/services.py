"""
Service initialization utilities for the Code Review Assistant.
"""
import os
from google.adk.artifacts import GcsArtifactService, InMemoryArtifactService
from google.adk.sessions import InMemorySessionService, DatabaseSessionService, VertexAiSessionService
from .config import config


def get_artifact_service():
    """Initialize artifact service based on environment."""
    if config.artifact_bucket:
        return GcsArtifactService(bucket_name=config.artifact_bucket)
    else:
        return InMemoryArtifactService()


def get_session_service():
    """Initialize session service based on environment."""
    # Check if we have a DATABASE_URL or SESSION_SERVICE_URI
    session_uri = os.environ.get('SESSION_SERVICE_URI', '')

    if session_uri:
        if 'postgresql' in session_uri or 'sqlite' in session_uri:
            return DatabaseSessionService(db_url=session_uri)
        elif 'vertexai://' in session_uri:
            # Parse Agent Engine ID from URI
            agent_engine_id = session_uri.replace('vertexai://', '')
            return VertexAiSessionService(
                project=config.google_cloud_project,
                location=config.google_cloud_location,
                agent_engine_id=agent_engine_id
            )

    # Default to in-memory
    return InMemorySessionService()

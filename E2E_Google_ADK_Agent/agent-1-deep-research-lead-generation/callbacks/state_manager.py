import json
import os
from pathlib import Path
from models import SessionState
from typing import Optional
import uuid


SESSION_DIR = Path(".sessions")
SESSION_DIR.mkdir(exist_ok=True)


def load_or_create_session(session_id: Optional[str] = None) -> SessionState:
    """Load existing session or create new one."""
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    session_file = SESSION_DIR / f"{session_id}.json"
    
    if session_file.exists():
        with open(session_file, 'r') as f:
            data = json.load(f)
            return SessionState(**data)
    else:
        return SessionState(session_id=session_id)


def save_session(state: SessionState):
    """Save session state to disk."""
    session_file = SESSION_DIR / f"{state.session_id}.json"
    
    with open(session_file, 'w') as f:
        json.dump(state.model_dump(), f, indent=2, default=str)

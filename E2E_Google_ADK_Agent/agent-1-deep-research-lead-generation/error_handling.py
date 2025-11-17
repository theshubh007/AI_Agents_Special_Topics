import time
from typing import Any, Callable


class AgentError(Exception):
    """Custom exception for agent errors."""
    
    def __init__(self, agent_name: str, error_type: str, message: str, recoverable: bool = True):
        self.agent_name = agent_name
        self.error_type = error_type
        self.message = message
        self.recoverable = recoverable
        super().__init__(f"[{agent_name}] {error_type}: {message}")


def retry_with_backoff(func: Callable, max_retries: int = 3, initial_delay: float = 1.0) -> Any:
    """Retry a function with exponential backoff."""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise AgentError(
                    agent_name="RetryHandler",
                    error_type="MAX_RETRIES_EXCEEDED",
                    message=f"Failed after {max_retries} attempts: {str(e)}",
                    recoverable=False
                )
            
            print(f"⚠️  Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2


def handle_agent_error(error: AgentError) -> dict:
    """Handle agent errors with appropriate recovery strategies."""
    print(f"❌ Error in {error.agent_name}: {error.message}")
    
    if not error.recoverable:
        return {
            "status": "failed",
            "error": error.message,
            "recoverable": False
        }
    
    return {
        "status": "error",
        "error": error.message,
        "recoverable": True,
        "suggestion": "Retrying with adjusted parameters..."
    }

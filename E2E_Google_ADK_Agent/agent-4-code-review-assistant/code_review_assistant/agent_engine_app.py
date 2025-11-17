"""Agent Engine application wrapper."""
from vertexai import agent_engines
from code_review_assistant.agent import root_agent

# Wrap the agent in an AdkApp object as per documentation
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

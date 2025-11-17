# code_review_assistant/__init__.py
"""
Code Review Assistant - An intelligent code grading system using ADK.

This package provides a multi-agent system for reviewing Python code,
checking style compliance, running tests, and providing personalized feedback.
"""

try:
    from .agent import root_agent
    __all__ = ["root_agent"]
except (ImportError, AttributeError):
    # Module 5 not completed yet
    __all__ = []
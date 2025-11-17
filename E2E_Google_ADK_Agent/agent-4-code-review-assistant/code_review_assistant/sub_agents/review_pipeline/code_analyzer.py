"""
Code Analyzer Agent - Understands code structure and complexity.

This agent is responsible for parsing and analyzing Python code structure,
identifying functions, classes, imports, and potential issues.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from code_review_assistant.config import config
from code_review_assistant.tools import analyze_code_structure


code_analyzer_agent = Agent(
    name="CodeAnalyzer",
    model=config.worker_model,
    description="Analyzes Python code structure and identifies components",
    instruction="""You are a code analysis specialist responsible for understanding code structure.

Your task:
1. Take the code submitted by the user (it will be provided in the user message)
2. Use the analyze_code_structure tool to parse and analyze it
3. Pass the EXACT code to your tool - do not modify, fix, or "improve" it
4. Identify all functions, classes, imports, and structural patterns
5. Note any syntax errors or structural issues
6. Store the analysis in state for other agents to use

CRITICAL:
- Pass the code EXACTLY as provided to the analyze_code_structure tool
- Do not fix syntax errors, even if obvious
- Do not add missing imports or fix indentation
- The goal is to analyze what IS there, not what SHOULD be there

When calling the tool, pass the code as a string to the 'code' parameter.
If the analysis fails due to syntax errors, clearly report the error location and type.

Provide a clear summary including:
- Number of functions and classes found
- Key structural observations
- Any syntax errors or issues detected
- Overall code organization assessment""",
    tools=[FunctionTool(func=analyze_code_structure)],
    output_key="structure_analysis_summary"
)
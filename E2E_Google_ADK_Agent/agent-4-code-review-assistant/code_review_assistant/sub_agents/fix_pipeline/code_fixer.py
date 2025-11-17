"""
Code Fixer Agent - Generates fixes for all identified issues.

This agent takes the analysis results from the review pipeline
and generates corrected code that addresses all issues.
"""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.utils import instructions_utils
from code_review_assistant.config import config


async def code_fixer_instruction_provider(context: ReadonlyContext) -> str:
    """Dynamic instruction provider that injects state variables."""
    template = """You are an expert code fixing specialist.

Original Code:
{code_to_review}

Analysis Results:
- Style Score: {style_score}/100
- Style Issues: {style_issues}
- Test Results: {test_execution_summary}

Based on the test results, identify and fix ALL issues including:
- Interface bugs (e.g., if start parameter expects wrong type)
- Logic errors (e.g., KeyError when accessing graph nodes)
- Style violations
- Missing documentation

YOUR TASK:
Generate the complete fixed Python code that addresses all identified issues.

CRITICAL INSTRUCTIONS:
- Output ONLY the corrected Python code
- Do NOT include markdown code blocks (```python)
- Do NOT include any explanations or commentary
- The output should be valid, executable Python code and nothing else

Common fixes to apply based on test results:
- If tests show AttributeError with 'pop', fix: stack = [start] instead of stack = start
- If tests show KeyError accessing graph, fix: use graph.get(current, [])
- Add docstrings if missing
- Fix any style violations identified

Output the complete fixed code now:"""

    return await instructions_utils.inject_session_state(template, context)


code_fixer_agent = Agent(
    name="CodeFixer",
    model=config.worker_model,
    description="Generates comprehensive fixes for all identified code issues",
    instruction=code_fixer_instruction_provider,
    code_executor=BuiltInCodeExecutor(),
    output_key="code_fixes"
)
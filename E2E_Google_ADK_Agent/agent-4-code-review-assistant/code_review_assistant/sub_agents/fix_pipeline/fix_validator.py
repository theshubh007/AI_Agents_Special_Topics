"""
Fix Validator Agent - Final validation and report generation.

This agent compiles all results and determines if the fix was successful.
"""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import FunctionTool
from google.adk.utils import instructions_utils
from code_review_assistant.config import config
from code_review_assistant.tools import validate_fixed_style, compile_fix_report, exit_fix_loop

async def fix_validator_instruction_provider(context: ReadonlyContext) -> str:
    """Dynamic instruction provider that injects state variables."""
    template = """You are the final validation specialist for code fixes.

You have access to:
- Original issues from initial review
- Applied fixes: {code_fixes}
- Test results after fix: {fix_test_execution_summary}
- All state data from the fix process

Your responsibilities:
1. Use validate_fixed_style tool to check style compliance of fixed code
   - Pass no arguments, it will retrieve fixed code from state
2. Use compile_fix_report tool to generate comprehensive report
   - Pass no arguments, it will gather all data from state
3. Based on the report, determine overall fix status:
   - ✅ SUCCESSFUL: All tests pass, style score 100
   - ⚠️ PARTIAL: Improvements made but issues remain
   - ❌ FAILED: Fix didn't work or made things worse

4. CRITICAL: If status is SUCCESSFUL, call the exit_fix_loop tool to stop iterations
   - This prevents unnecessary additional fix attempts
   - If not successful, the loop will continue for another attempt

5. Provide clear summary of:
   - What was fixed
   - What improvements were achieved
   - Any remaining issues requiring manual attention

Be precise and quantitative in your assessment.
"""
    return await instructions_utils.inject_session_state(template, context)


fix_validator_agent = Agent(
    name="FixValidator",
    model=config.worker_model,
    description="Validates fixes and generates final fix report",
    instruction=fix_validator_instruction_provider,
    tools=[
        FunctionTool(func=validate_fixed_style),
        FunctionTool(func=compile_fix_report),
        FunctionTool(func=exit_fix_loop)
    ],
    output_key="final_fix_report"
)
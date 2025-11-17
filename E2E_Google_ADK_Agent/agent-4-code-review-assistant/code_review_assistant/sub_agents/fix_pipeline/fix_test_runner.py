"""
Fix Test Runner Agent - Validates fixes by running tests on corrected code.

This agent executes the same test suite on the fixed code to verify
that all issues have been resolved.
"""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.utils import instructions_utils
from code_review_assistant.config import config


async def fix_test_runner_instruction_provider(context: ReadonlyContext) -> str:
    """Dynamic instruction provider that uses the clean code from the previous step."""
    template = """You are responsible for validating the fixed code by running tests.

THE FIXED CODE TO TEST:
{code_fixes}

ORIGINAL TEST RESULTS: {test_execution_summary}

YOUR TASK:
1. Understand the fixes that were applied
2. Generate the same comprehensive tests (15-20 test cases)
3. Execute the tests on the FIXED code using your code executor
4. Compare results with original test results
5. Output a detailed JSON analysis

TESTING METHODOLOGY:
- Run the same tests that revealed issues in the original code
- Verify that previously failing tests now pass
- Ensure no regressions were introduced
- Document the improvement

Execute your tests and output ONLY valid JSON with this structure:
- "passed": number of tests that passed
- "failed": number of tests that failed  
- "total": total number of tests
- "pass_rate": percentage as a number
- "comparison": object with "original_pass_rate", "new_pass_rate", "improvement"
- "newly_passing_tests": array of test names that now pass
- "still_failing_tests": array of test names still failing

Do NOT output the test code itself, only the JSON analysis."""

    return await instructions_utils.inject_session_state(template, context)


fix_test_runner_agent = Agent(
    name="FixTestRunner",
    model=config.critic_model,
    description="Runs comprehensive tests on fixed code to verify all issues are resolved",
    instruction=fix_test_runner_instruction_provider,
    code_executor=BuiltInCodeExecutor(),
    output_key="fix_test_execution_summary"
)
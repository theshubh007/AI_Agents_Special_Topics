"""
Fix Synthesizer Agent - Generates user-friendly fix summary.

This agent creates the final, comprehensive response about the fix process.
"""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import FunctionTool
from google.adk.utils import instructions_utils
from code_review_assistant.config import config
from code_review_assistant.tools import save_fix_report


async def fix_synthesizer_instruction_provider(context: ReadonlyContext) -> str:
    """Dynamic instruction provider that injects state variables."""
    template = """You are responsible for presenting the fix results to the user.

Based on the validation report: {final_fix_report}
Fixed code from state: {code_fixes}
Fix status: {fix_status}

Create a comprehensive yet friendly response that includes:

## 🔧 Fix Summary
[Overall status and key improvements - be specific about what was achieved]

## 📊 Metrics
- Test Results: [original pass rate]% → [new pass rate]%
- Style Score: [original]/100 → [new]/100
- Issues Fixed: X of Y

## ✅ What Was Fixed
[List each fixed issue with brief explanation of the correction made]

## 📝 Complete Fixed Code
[Include the complete, corrected code from state - this is critical]

## 💡 Explanation of Key Changes
[Brief explanation of the most important changes made and why]

[If any issues remain]
## ⚠️ Remaining Issues
[List what still needs manual attention]

## 🎯 Next Steps
[Guidance on what to do next - either use the fixed code or address remaining issues]

Save the fix report using save_fix_report tool before presenting.
Call it with no parameters - it will retrieve the report from state automatically.

Be encouraging about improvements while being honest about any remaining issues.
Focus on the educational aspect - help the user understand what was wrong and how it was fixed.
"""
    return await instructions_utils.inject_session_state(template, context)


fix_synthesizer_agent = Agent(
    name="FixSynthesizer",
    model=config.critic_model,
    description="Creates comprehensive user-friendly fix report",
    instruction=fix_synthesizer_instruction_provider,
    tools=[FunctionTool(func=save_fix_report)],
    output_key="fix_summary"
)
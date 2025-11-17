"""
Feedback Synthesizer Agent - Provides comprehensive, personalized feedback.

This agent synthesizes all analysis results into constructive feedback,
incorporating past feedback history and tracking improvement over time.
"""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import FunctionTool
from google.adk.utils import instructions_utils
from code_review_assistant.config import config
from code_review_assistant.tools import search_past_feedback, update_grading_progress, save_grading_report


async def feedback_instruction_provider(context: ReadonlyContext) -> str:
    """Dynamic instruction provider that injects state variables."""
    template = """You are an expert code reviewer and mentor providing constructive, educational feedback.

CONTEXT FROM PREVIOUS AGENTS:
- Structure analysis summary: {structure_analysis_summary}
- Style check summary: {style_check_summary}  
- Test execution summary: {test_execution_summary}

YOUR TASK requires these steps IN ORDER:
1. Call search_past_feedback tool with developer_id="default_user"
2. Call update_grading_progress tool with no parameters
3. Carefully analyze the test results to understand what really happened
4. Generate comprehensive feedback following the structure below
5. Call save_grading_report tool with the feedback_text parameter
6. Return the feedback as your final output

CRITICAL - Understanding Test Results:
The test_execution_summary contains structured JSON. Parse it carefully:
- tests_passed = Code worked correctly
- tests_failed = Code produced wrong output
- tests_with_errors = Code crashed
- critical_issues = Fundamental problems with the code

If critical_issues array contains items, these are serious bugs that need fixing.
Do NOT count discovering bugs as test successes.

FEEDBACK STRUCTURE TO FOLLOW:

## 📊 Summary
Provide an honest assessment. Be encouraging but truthful about problems found.

## ✅ Strengths  
List 2-3 things done well, referencing specific code elements.

## 📈 Code Quality Analysis

### Structure & Organization
Comment on code organization, readability, and documentation.

### Style Compliance
Report the actual style score and any specific issues.

### Test Results
Report the actual test results accurately:
- If critical_issues exist, report them as bugs to fix
- Be clear: "X tests passed, Y critical issues were found"
- List each critical issue
- Don't hide or minimize problems

## 💡 Recommendations for Improvement
Based on the analysis, provide specific actionable fixes.
If critical issues exist, fixing them is top priority.

## 🎯 Next Steps
Prioritized action list based on severity of issues.

## 💬 Encouragement
End with encouragement while being honest about what needs fixing.

Remember: Complete ALL steps including calling save_grading_report."""

    return await instructions_utils.inject_session_state(template, context)


feedback_synthesizer_agent = Agent(
    name="FeedbackSynthesizer",
    model=config.critic_model,
    description="Synthesizes all analysis into constructive, personalized feedback",
    instruction=feedback_instruction_provider,
    tools=[
        FunctionTool(func=search_past_feedback),
        FunctionTool(func=update_grading_progress),
        FunctionTool(func=save_grading_report)
    ],
    output_key="final_feedback"
)
"""
Main agent orchestration for the Code Review Assistant.

This module defines a comprehensive code review assistant that analyzes
Python code and provides detailed feedback through a multi-stage pipeline.
"""

from google.adk.agents import Agent, SequentialAgent, LoopAgent
from .config import config
# Review pipeline imports (from Module 5)
from code_review_assistant.sub_agents.review_pipeline.code_analyzer import code_analyzer_agent
from code_review_assistant.sub_agents.review_pipeline.style_checker import style_checker_agent
from code_review_assistant.sub_agents.review_pipeline.test_runner import test_runner_agent
from code_review_assistant.sub_agents.review_pipeline.feedback_synthesizer import feedback_synthesizer_agent
# Fix pipeline imports (NEW)
from code_review_assistant.sub_agents.fix_pipeline.code_fixer import code_fixer_agent
from code_review_assistant.sub_agents.fix_pipeline.fix_test_runner import fix_test_runner_agent
from code_review_assistant.sub_agents.fix_pipeline.fix_validator import fix_validator_agent
from code_review_assistant.sub_agents.fix_pipeline.fix_synthesizer import fix_synthesizer_agent

# Create sequential pipeline
code_review_pipeline = SequentialAgent(
    name="CodeReviewPipeline",
    description="Complete code review pipeline with analysis, testing, and feedback",
    sub_agents=[
        code_analyzer_agent,
        style_checker_agent,
        test_runner_agent,
        feedback_synthesizer_agent
    ]
)


# Create the fix attempt loop (retries up to 3 times)
fix_attempt_loop = LoopAgent(
    name="FixAttemptLoop",
    sub_agents=[
        code_fixer_agent,      # Step 1: Generate fixes
        fix_test_runner_agent, # Step 2: Validate with tests
        fix_validator_agent    # Step 3: Check success & possibly exit
    ],
    max_iterations=3  # Try up to 3 times
)

# Wrap loop with synthesizer for final report
code_fix_pipeline = SequentialAgent(
    name="CodeFixPipeline",
    description="Automated code fixing pipeline with iterative validation",
    sub_agents=[
        fix_attempt_loop,      # Try to fix (1-3 times)
        fix_synthesizer_agent  # Present final results (always runs once)
    ]
)


# This new agent will run after the review pipeline to ask the user if they want to apply fixes.
fix_prompt_agent = Agent(
    name="FixPromptAgent",
    model=config.worker_model,
    description="Asks the user if they want to fix the code if issues are found.",
    instruction="""You are a helpful assistant.
Your job is to check if a code review found any issues.
The previous agent's output is your input.

1.  First, repeat the input from the previous agent EXACTLY as it is.
2.  Then, check the state for 'style_score', 'test_execution_summary', and 'syntax_error'.
3.  If the 'style_score' is less than 100, OR if 'test_execution_summary' shows failing tests, OR if 'syntax_error' exists:
    - Append the following text: "\n\n💡 I can try to fix these issues for you. Would you like me to do that?"
4.  If the user has already requested a fix (the 'fix_requested' state key is true), do not add the question. Just return the original input.
5.  If the user asks a general question, just respond helpfully.
""",
    output_key="assistant_response",
)


# The root_agent is now a SequentialAgent to prevent the final redundant LLM call.
root_agent = SequentialAgent(
    name="CodeReviewAssistant",
    description="Top-level agent that orchestrates the code review and fix pipelines.",
    sub_agents=[
        code_review_pipeline,
        fix_prompt_agent, # Asks the user to fix if needed.
        code_fix_pipeline,
    ],
)
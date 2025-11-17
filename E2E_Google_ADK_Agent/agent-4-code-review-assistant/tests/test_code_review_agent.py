"""
Integration tests for the Code Review Assistant using ADK evaluation framework.
"""

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.asyncio
async def test_add_function_review():
    """Test code review of simple add function."""
    await AgentEvaluator.evaluate(
        agent_module="code_review_assistant",
        eval_dataset_file_path_or_dir="tests/integration/test_add_function_review.test.json"
    )

@pytest.mark.asyncio
async def test_style_violations():
    """Test that style violations are properly detected."""
    await AgentEvaluator.evaluate(
        agent_module="code_review_assistant",
        eval_dataset_file_path_or_dir="tests/integration/style_violations.test.json"
    )

@pytest.mark.asyncio
async def test_all_integration_tests():
    """Run all test files in the integration directory."""
    await AgentEvaluator.evaluate(
        agent_module="code_review_assistant",
        eval_dataset_file_path_or_dir="tests/integration/"
    )

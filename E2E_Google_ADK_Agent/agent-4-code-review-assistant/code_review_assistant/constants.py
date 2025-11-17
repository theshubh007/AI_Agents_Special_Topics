"""
Centralized state key definitions for the Code Review Assistant.
This ensures consistency across all agents and tools when accessing state.
"""


class StateKeys:
    """State keys used throughout the code review pipeline."""

    # === Session-level keys (persist within a session) ===
    CODE_TO_REVIEW = "code_to_review"
    CODE_ANALYSIS = "code_analysis"
    CODE_LINE_COUNT = "code_line_count"
    STYLE_SCORE = "style_score"
    STYLE_ISSUES = "style_issues"
    STYLE_ISSUE_COUNT = "style_issue_count"

    # === Test-related keys ===
    TEST_EXECUTION_SUMMARY = "test_execution_summary"  # From test_runner_agent output_key

    # === Review pipeline state ===
    FINAL_GRADE = "final_grade"
    GRADING_ATTEMPTS = "grading_attempts"
    LAST_GRADING_TIME = "last_grading_time"
    SYNTAX_ERROR = "syntax_error"
    PAST_FEEDBACK = "past_feedback"
    FEEDBACK_PATTERNS = "feedback_patterns"
    SCORE_IMPROVEMENT = "score_improvement"

    # === Fix pipeline keys ===
    CODE_FIXES = "code_fixes"  # From code_fixer_agent output_key
    FIX_TEST_EXECUTION_SUMMARY = "fix_test_execution_summary"  # From fix_test_runner_agent output_key
    FIXED_STYLE_SCORE = "fixed_style_score"
    FIXED_STYLE_ISSUES = "fixed_style_issues"
    FIX_REPORT = "fix_report"
    FIX_STATUS = "fix_status"
    FINAL_FIX_REPORT = "final_fix_report"  # From fix_validator_agent output_key
    LAST_FIX_REPORT = "last_fix_report"
    FIX_REQUESTED = "fix_requested"

    # === Agent output keys (for reference) ===
    STRUCTURE_ANALYSIS_SUMMARY = "structure_analysis_summary"  # From code_analyzer_agent
    STYLE_CHECK_SUMMARY = "style_check_summary"  # From style_checker_agent
    FINAL_FEEDBACK = "final_feedback"  # From feedback_synthesizer_agent
    FIX_SUMMARY = "fix_summary"  # From fix_synthesizer_agent

    # === Temporary keys (cleared after each invocation) ===
    TEMP_TEST_CODE = "temp:test_code_to_execute"
    TEMP_ANALYSIS_TIMESTAMP = "temp:analysis_timestamp"
    TEMP_TEST_GENERATION_COMPLETE = "temp:test_generation_complete"
    TEMP_FUNCTIONS_TO_TEST = "temp:functions_to_test"
    TEMP_PROCESSING_TIMESTAMP = "temp:processing_timestamp"

    # === User-scoped keys (persist across sessions for a user) ===
    USER_ID = "user_id"
    USER_PREFERRED_STYLE = "user:preferred_style"
    USER_TOTAL_SUBMISSIONS = "user:total_submissions"
    USER_LAST_STYLE_SCORE = "user:last_style_score"
    USER_LAST_SUBMISSION_TIME = "user:last_submission_time"
    USER_LAST_TEST_PASS_RATE = "user:last_test_pass_rate"
    USER_PAST_FEEDBACK_CACHE = "user:past_feedback_cache"
    USER_LAST_GRADING_REPORT = "user:last_grading_report"

    # === App-scoped keys (shared across all users) ===
    APP_GRADING_VERSION = "app:grading_version"
    APP_STYLE_GUIDE_VERSION = "app:style_guide_version"

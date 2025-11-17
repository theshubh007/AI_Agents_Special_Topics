"""
Tools for the Code Review Assistant.

These tools provide safe code analysis, style checking, test generation,
and feedback management capabilities using ADK's built-in code executor.
"""

import ast
import asyncio
import hashlib
import json
import os
import pycodestyle
import tempfile
import logging
from datetime import datetime
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor

from google.genai import types
from google.adk.tools import ToolContext

from .constants import StateKeys

# Configure logging
logger = logging.getLogger(__name__)


async def analyze_code_structure(code: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Analyzes Python code structure using AST parsing.

    This tool parses Python code to extract structural information
    including functions, classes, imports, and complexity metrics.

    Args:
        code: Python source code to analyze
        tool_context: ADK tool context for state management

    Returns:
        Dictionary containing analysis results and status
    """
    logger.info("Tool: Analyzing code structure...")

    try:
        # Validate input
        if not code or not isinstance(code, str):
            return {
                "status": "error",
                "message": "No code provided or invalid input"
            }

        # Parse in thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            tree = await loop.run_in_executor(executor, ast.parse, code)

            # Extract comprehensive structural information
            analysis = await loop.run_in_executor(
                executor, _extract_code_structure, tree, code
            )

        # Store code and analysis for other agents to access
        tool_context.state[StateKeys.CODE_TO_REVIEW] = code
        tool_context.state[StateKeys.CODE_ANALYSIS] = analysis
        tool_context.state[StateKeys.CODE_LINE_COUNT] = len(code.splitlines())

        logger.info(f"Tool: Analysis complete - {analysis['metrics']['function_count']} functions, "
                    f"{analysis['metrics']['class_count']} classes")

        return {
            "status": "success",
            "analysis": analysis,
            "summary": f"Found {analysis['metrics']['function_count']} functions and "
                       f"{analysis['metrics']['class_count']} classes"
        }

    except SyntaxError as e:
        error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
        logger.error(f"Tool: {error_msg}")
        tool_context.state[StateKeys.CODE_TO_REVIEW] = code
        tool_context.state[StateKeys.SYNTAX_ERROR] = error_msg

        return {
            "status": "error",
            "error_type": "syntax",
            "message": error_msg,
            "line": e.lineno,
            "offset": e.offset
        }
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        logger.error(f"Tool: {error_msg}", exc_info=True)

        return {
            "status": "error",
            "error_type": "parse",
            "message": error_msg
        }


def _extract_code_structure(tree: ast.AST, code: str) -> Dict[str, Any]:
    """
    Helper function to extract structural information from AST.
    Runs in thread pool for CPU-bound work.
    """
    functions = []
    classes = []
    imports = []
    docstrings = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = {
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'lineno': node.lineno,
                'has_docstring': ast.get_docstring(node) is not None,
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'decorators': [d.id for d in node.decorator_list
                               if isinstance(d, ast.Name)]
            }
            functions.append(func_info)

            if func_info['has_docstring']:
                docstrings.append(f"{node.name}: {ast.get_docstring(node)[:50]}...")

        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)

            class_info = {
                'name': node.name,
                'lineno': node.lineno,
                'methods': methods,
                'has_docstring': ast.get_docstring(node) is not None,
                'base_classes': [base.id for base in node.bases
                                 if isinstance(base, ast.Name)]
            }
            classes.append(class_info)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'module': alias.name,
                    'alias': alias.asname,
                    'type': 'import'
                })
        elif isinstance(node, ast.ImportFrom):
            imports.append({
                'module': node.module or '',
                'names': [alias.name for alias in node.names],
                'type': 'from_import',
                'level': node.level
            })

    return {
        'functions': functions,
        'classes': classes,
        'imports': imports,
        'docstrings': docstrings,
        'metrics': {
            'line_count': len(code.splitlines()),
            'function_count': len(functions),
            'class_count': len(classes),
            'import_count': len(imports),
            'has_main': any(f['name'] == 'main' for f in functions),
            'has_if_main': '__main__' in code,
            'avg_function_length': _calculate_avg_function_length(tree)
        }
    }


def _calculate_avg_function_length(tree: ast.AST) -> float:
    """Calculate average function length in lines."""
    function_lengths = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                length = node.end_lineno - node.lineno + 1
                function_lengths.append(length)

    if function_lengths:
        return sum(function_lengths) / len(function_lengths)
    return 0.0


async def check_code_style(code: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Checks code style compliance using pycodestyle (PEP 8).

    Args:
        code: Python source code to check (or will retrieve from state)
        tool_context: ADK tool context

    Returns:
        Dictionary containing style score and issues
    """
    logger.info("Tool: Checking code style...")

    try:
        # Retrieve code from state if not provided
        if not code:
            code = tool_context.state.get(StateKeys.CODE_TO_REVIEW, '')
            if not code:
                return {
                    "status": "error",
                    "message": "No code provided or found in state"
                }

        # Run style check in thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, _perform_style_check, code
            )

        # Store results in state
        tool_context.state[StateKeys.STYLE_SCORE] = result['score']
        tool_context.state[StateKeys.STYLE_ISSUES] = result['issues']
        tool_context.state[StateKeys.STYLE_ISSUE_COUNT] = result['issue_count']

        logger.info(f"Tool: Style check complete - Score: {result['score']}/100, "
                    f"Issues: {result['issue_count']}")

        return result

    except Exception as e:
        error_msg = f"Style check failed: {str(e)}"
        logger.error(f"Tool: {error_msg}", exc_info=True)

        # Set default values on error
        tool_context.state[StateKeys.STYLE_SCORE] = 0
        tool_context.state[StateKeys.STYLE_ISSUES] = []

        return {
            "status": "error",
            "message": error_msg,
            "score": 0
        }


def _perform_style_check(code: str) -> Dict[str, Any]:
    """Helper to perform style check in thread pool."""
    import io
    import sys

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # Capture stdout to get pycodestyle output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        style_guide = pycodestyle.StyleGuide(
            quiet=False,  # We want output
            max_line_length=100,
            ignore=['E501', 'W503']
        )

        result = style_guide.check_files([tmp_path])

        # Restore stdout
        sys.stdout = old_stdout

        # Parse captured output
        output = captured_output.getvalue()
        issues = []

        for line in output.strip().split('\n'):
            if line and ':' in line:
                parts = line.split(':', 4)
                if len(parts) >= 4:
                    try:
                        issues.append({
                            'line': int(parts[1]),
                            'column': int(parts[2]),
                            'code': parts[3].split()[0] if len(parts) > 3 else 'E000',
                            'message': parts[3].strip() if len(parts) > 3 else 'Unknown error'
                        })
                    except (ValueError, IndexError):
                        pass

        # Add naming convention checks
        try:
            tree = ast.parse(code)
            naming_issues = _check_naming_conventions(tree)
            issues.extend(naming_issues)
        except SyntaxError:
            pass  # Syntax errors will be caught elsewhere

        # Calculate weighted score
        score = _calculate_style_score(issues)

        return {
            "status": "success",
            "score": score,
            "issue_count": len(issues),
            "issues": issues[:10],  # First 10 issues
            "summary": f"Style score: {score}/100 with {len(issues)} violations"
        }

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _check_naming_conventions(tree: ast.AST) -> List[Dict[str, Any]]:
    """Check PEP 8 naming conventions."""
    naming_issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip private/protected methods and __main__
            if not node.name.startswith('_') and node.name != node.name.lower():
                naming_issues.append({
                    'line': node.lineno,
                    'column': node.col_offset,
                    'code': 'N802',
                    'message': f"N802 function name '{node.name}' should be lowercase"
                })
        elif isinstance(node, ast.ClassDef):
            # Check if class name follows CapWords convention
            if not node.name[0].isupper() or '_' in node.name:
                naming_issues.append({
                    'line': node.lineno,
                    'column': node.col_offset,
                    'code': 'N801',
                    'message': f"N801 class name '{node.name}' should use CapWords convention"
                })

    return naming_issues


def _calculate_style_score(issues: List[Dict[str, Any]]) -> int:
    """Calculate weighted style score based on violation severity."""
    if not issues:
        return 100

    # Define weights by error type
    weights = {
        'E1': 10,  # Indentation errors
        'E2': 3,  # Whitespace errors
        'E3': 5,  # Blank line errors
        'E4': 8,  # Import errors
        'E5': 5,  # Line length
        'E7': 7,  # Statement errors
        'E9': 10,  # Syntax errors
        'W2': 2,  # Whitespace warnings
        'W3': 2,  # Blank line warnings
        'W5': 3,  # Line break warnings
        'N8': 7,  # Naming conventions
    }

    total_deduction = 0
    for issue in issues:
        code_prefix = issue['code'][:2] if len(issue['code']) >= 2 else 'E2'
        weight = weights.get(code_prefix, 3)
        total_deduction += weight

    # Cap at 100 points deduction
    return max(0, 100 - min(total_deduction, 100))


async def search_past_feedback(developer_id: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Search for past feedback in memory service.

    Args:
        developer_id: ID of the developer (defaults to "default_user")
        tool_context: ADK tool context with potential memory service access

    Returns:
        Dictionary containing feedback search results
    """
    logger.info(f"Tool: Searching for past feedback for developer {developer_id}...")

    try:
        # Default developer ID if not provided
        if not developer_id:
            developer_id = tool_context.state.get(StateKeys.USER_ID, 'default_user')

        # Check if memory service is available
        if hasattr(tool_context, 'search_memory'):
            try:
                # Perform structured searches
                queries = [
                    f"developer:{developer_id} code review feedback",
                    f"developer:{developer_id} common issues",
                    f"developer:{developer_id} improvements"
                ]

                all_feedback = []
                patterns = {
                    'common_issues': [],
                    'improvements': [],
                    'strengths': []
                }

                for query in queries:
                    search_result = await tool_context.search_memory(query)

                    if search_result and hasattr(search_result, 'memories'):
                        for memory in search_result.memories[:5]:
                            memory_text = memory.text if hasattr(memory, 'text') else str(memory)
                            all_feedback.append(memory_text)

                            # Extract patterns
                            if 'style' in memory_text.lower():
                                patterns['common_issues'].append('style compliance')
                            if 'improved' in memory_text.lower():
                                patterns['improvements'].append('showing improvement')
                            if 'excellent' in memory_text.lower():
                                patterns['strengths'].append('consistent quality')

                # Store in state
                tool_context.state[StateKeys.PAST_FEEDBACK] = all_feedback
                tool_context.state[StateKeys.FEEDBACK_PATTERNS] = patterns

                logger.info(f"Tool: Found {len(all_feedback)} past feedback items")

                return {
                    "status": "success",
                    "feedback_found": True,
                    "count": len(all_feedback),
                    "summary": " | ".join(all_feedback[:3]) if all_feedback else "No feedback",
                    "patterns": patterns
                }

            except Exception as e:
                logger.warning(f"Tool: Memory search error: {e}")

        # Fallback: Check state for cached feedback
        cached_feedback = tool_context.state.get(StateKeys.USER_PAST_FEEDBACK_CACHE, [])
        if cached_feedback:
            tool_context.state[StateKeys.PAST_FEEDBACK] = cached_feedback
            return {
                "status": "success",
                "feedback_found": True,
                "count": len(cached_feedback),
                "summary": "Using cached feedback",
                "patterns": {}
            }

        # No feedback found
        tool_context.state[StateKeys.PAST_FEEDBACK] = []
        logger.info("Tool: No past feedback found")

        return {
            "status": "success",
            "feedback_found": False,
            "message": "No past feedback available - this appears to be a first submission",
            "patterns": {}
        }

    except Exception as e:
        error_msg = f"Feedback search error: {str(e)}"
        logger.error(f"Tool: {error_msg}", exc_info=True)

        tool_context.state[StateKeys.PAST_FEEDBACK] = []

        return {
            "status": "error",
            "message": error_msg,
            "feedback_found": False
        }


async def update_grading_progress(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Updates grading progress counters and metrics in state.
    """
    logger.info("Tool: Updating grading progress...")

    try:
        current_time = datetime.now().isoformat()

        # Build all state changes
        state_updates = {}

        # Temporary (invocation-level) state
        state_updates[StateKeys.TEMP_PROCESSING_TIMESTAMP] = current_time

        # Session-level state
        attempts = tool_context.state.get(StateKeys.GRADING_ATTEMPTS, 0) + 1
        state_updates[StateKeys.GRADING_ATTEMPTS] = attempts
        state_updates[StateKeys.LAST_GRADING_TIME] = current_time

        # User-level persistent state
        lifetime_submissions = tool_context.state.get(StateKeys.USER_TOTAL_SUBMISSIONS, 0) + 1
        state_updates[StateKeys.USER_TOTAL_SUBMISSIONS] = lifetime_submissions
        state_updates[StateKeys.USER_LAST_SUBMISSION_TIME] = current_time

        # Calculate improvement metrics
        current_style_score = tool_context.state.get(StateKeys.STYLE_SCORE, 0)
        last_style_score = tool_context.state.get(StateKeys.USER_LAST_STYLE_SCORE, 0)
        score_improvement = current_style_score - last_style_score

        state_updates[StateKeys.USER_LAST_STYLE_SCORE] = current_style_score
        state_updates[StateKeys.SCORE_IMPROVEMENT] = score_improvement

        # Track test results if available
        test_results = tool_context.state.get(StateKeys.TEST_EXECUTION_SUMMARY, {})

        # Parse if it's a string
        if isinstance(test_results, str):
            try:
                test_results = json.loads(test_results)
            except:
                test_results = {}

        if test_results and test_results.get('test_summary', {}).get('total_tests_run', 0) > 0:
            summary = test_results['test_summary']
            total = summary.get('total_tests_run', 0)
            passed = summary.get('tests_passed', 0)
            if total > 0:
                pass_rate = (passed / total) * 100
                state_updates[StateKeys.USER_LAST_TEST_PASS_RATE] = pass_rate

        # Apply all updates atomically
        for key, value in state_updates.items():
            tool_context.state[key] = value

        logger.info(f"Tool: Progress updated - Attempt #{attempts}, "
                    f"Lifetime: {lifetime_submissions}")

        return {
            "status": "success",
            "session_attempts": attempts,
            "lifetime_submissions": lifetime_submissions,
            "timestamp": current_time,
            "improvement": {
                "style_score_change": score_improvement,
                "direction": "improved" if score_improvement > 0 else "declined"
            },
            "summary": f"Attempt #{attempts} recorded, {lifetime_submissions} total submissions"
        }

    except Exception as e:
        error_msg = f"Progress update error: {str(e)}"
        logger.error(f"Tool: {error_msg}", exc_info=True)

        return {
            "status": "error",
            "message": error_msg
        }


async def save_grading_report(feedback_text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Saves a detailed grading report as an artifact.

    Args:
        feedback_text: The feedback text to include in the report
        tool_context: ADK tool context for state management

    Returns:
        Dictionary containing save status and details
    """
    logger.info("Tool: Saving grading report...")

    try:
        # Gather all relevant data from state
        code = tool_context.state.get(StateKeys.CODE_TO_REVIEW, '')
        analysis = tool_context.state.get(StateKeys.CODE_ANALYSIS, {})
        style_score = tool_context.state.get(StateKeys.STYLE_SCORE, 0)
        style_issues = tool_context.state.get(StateKeys.STYLE_ISSUES, [])

        # Get test results
        test_results = tool_context.state.get(StateKeys.TEST_EXECUTION_SUMMARY, {})

        # Parse if it's a string
        if isinstance(test_results, str):
            try:
                test_results = json.loads(test_results)
            except:
                test_results = {}

        timestamp = datetime.now().isoformat()

        # Create comprehensive report dictionary
        report = {
            'timestamp': timestamp,
            'grading_attempt': tool_context.state.get(StateKeys.GRADING_ATTEMPTS, 1),
            'code': {
                'content': code,
                'line_count': len(code.splitlines()),
                'hash': hashlib.md5(code.encode()).hexdigest()
            },
            'analysis': analysis,
            'style': {
                'score': style_score,
                'issues': style_issues[:5]  # First 5 issues
            },
            'tests': test_results,
            'feedback': feedback_text,
            'improvements': {
                'score_change': tool_context.state.get(StateKeys.SCORE_IMPROVEMENT, 0),
                'from_last_score': tool_context.state.get(StateKeys.USER_LAST_STYLE_SCORE, 0)
            }
        }

        # Convert report to JSON string
        report_json = json.dumps(report, indent=2)
        report_part = types.Part.from_text(text=report_json)

        # Try to save as artifact if the service is available
        if hasattr(tool_context, 'save_artifact'):
            try:
                # Generate filename with timestamp (replace colons for filesystem compatibility)
                filename = f"grading_report_{timestamp.replace(':', '-')}.json"

                # Save the main report
                version = await tool_context.save_artifact(filename, report_part)

                # Also save a "latest" version for easy access
                await tool_context.save_artifact("latest_grading_report.json", report_part)

                logger.info(f"Tool: Report saved as {filename} (version {version})")

                # Store report in state as well for redundancy
                tool_context.state[StateKeys.USER_LAST_GRADING_REPORT] = report

                return {
                    "status": "success",
                    "artifact_saved": True,
                    "filename": filename,
                    "version": str(version),
                    "size": len(report_json),
                    "summary": f"Report saved as {filename}"
                }

            except Exception as artifact_error:
                logger.warning(f"Artifact service error: {artifact_error}, falling back to state storage")
                # Continue to fallback below

        # Fallback: Store in state if artifact service is not available or failed
        tool_context.state[StateKeys.USER_LAST_GRADING_REPORT] = report
        logger.info("Tool: Report saved to state (artifact service not available)")

        return {
            "status": "success",
            "artifact_saved": False,
            "message": "Report saved to state only",
            "size": len(report_json),
            "summary": "Report saved to session state"
        }

    except Exception as e:
        error_msg = f"Report save error: {str(e)}"
        logger.error(f"Tool: {error_msg}", exc_info=True)

        # Still try to save minimal data to state
        try:
            tool_context.state[StateKeys.USER_LAST_GRADING_REPORT] = {
                'error': error_msg,
                'feedback': feedback_text,
                'timestamp': datetime.now().isoformat()
            }
        except:
            pass

        return {
            "status": "error",
            "message": error_msg,
            "artifact_saved": False,
            "summary": f"Failed to save report: {error_msg}"
        }


async def validate_fixed_style(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Validates style compliance of the fixed code.

    Args:
        tool_context: ADK tool context containing fixed code in state

    Returns:
        Dictionary with style validation results
    """
    logger.info("Tool: Validating style of fixed code...")

    try:
        # Get the fixed code from state
        code_fixes = tool_context.state.get(StateKeys.CODE_FIXES, '')
       
        # Try to extract from markdown if present
        if '```python' in code_fixes:
            start = code_fixes.rfind('```python') + 9
            end = code_fixes.rfind('```')
            if start < end:
                code_fixes = code_fixes[start:end].strip()

        if not code_fixes:
            return {
                "status": "error",
                "message": "No fixed code found in state"
            }

        # Store the extracted fixed code
        tool_context.state[StateKeys.CODE_FIXES] = code_fixes

        # Run style check on fixed code
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            style_result = await loop.run_in_executor(
                executor, _perform_style_check, code_fixes
            )

        # Compare with original
        original_score = tool_context.state.get(StateKeys.STYLE_SCORE, 0)
        improvement = style_result['score'] - original_score

        # Store results
        tool_context.state[StateKeys.FIXED_STYLE_SCORE] = style_result['score']
        tool_context.state[StateKeys.FIXED_STYLE_ISSUES] = style_result['issues']

        logger.info(f"Tool: Fixed code style score: {style_result['score']}/100 "
                    f"(improvement: +{improvement})")

        return {
            "status": "success",
            "fixed_style_score": style_result['score'],
            "original_style_score": original_score,
            "improvement": improvement,
            "remaining_issues": style_result['issues'],
            "perfect_style": style_result['score'] == 100
        }

    except Exception as e:
        logger.error(f"Tool: Style validation failed: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }


async def compile_fix_report(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Compiles comprehensive report of the fix process.

    Args:
        tool_context: ADK tool context with all fix pipeline data

    Returns:
        Comprehensive fix report
    """
    logger.info("Tool: Compiling comprehensive fix report...")

    try:
        # Gather all data
        original_code = tool_context.state.get(StateKeys.CODE_TO_REVIEW, '')
        code_fixes = tool_context.state.get(StateKeys.CODE_FIXES, '')

        # Test results
        original_tests = tool_context.state.get(StateKeys.TEST_EXECUTION_SUMMARY, {})
        fixed_tests = tool_context.state.get(StateKeys.FIX_TEST_EXECUTION_SUMMARY, {})

        # Parse if strings
        if isinstance(original_tests, str):
            try:
                original_tests = json.loads(original_tests)
            except:
                original_tests = {}

        if isinstance(fixed_tests, str):
            try:
                fixed_tests = json.loads(fixed_tests)
            except:
                fixed_tests = {}

        # Extract pass rates
        original_pass_rate = 0
        if original_tests:
            if 'pass_rate' in original_tests:
                original_pass_rate = original_tests['pass_rate']
            elif 'test_summary' in original_tests:
                # Handle test_runner_agent's JSON structure
                summary = original_tests['test_summary']
                total = summary.get('total_tests_run', 0)
                passed = summary.get('tests_passed', 0)
                if total > 0:
                    original_pass_rate = (passed / total) * 100
            elif 'passed' in original_tests and 'total' in original_tests:
                if original_tests['total'] > 0:
                    original_pass_rate = (original_tests['passed'] / original_tests['total']) * 100

        fixed_pass_rate = 0
        all_tests_pass = False
        if fixed_tests:
            if 'pass_rate' in fixed_tests:
                fixed_pass_rate = fixed_tests['pass_rate']
                all_tests_pass = fixed_tests.get('failed', 1) == 0
            elif 'passed' in fixed_tests and 'total' in fixed_tests:
                if fixed_tests['total'] > 0:
                    fixed_pass_rate = (fixed_tests['passed'] / fixed_tests['total']) * 100
                all_tests_pass = fixed_tests.get('failed', 0) == 0

        # Style scores
        original_style = tool_context.state.get(StateKeys.STYLE_SCORE, 0)
        fixed_style = tool_context.state.get(StateKeys.FIXED_STYLE_SCORE, 0)

        # Calculate improvements
        test_improvement = {
            'original_pass_rate': original_pass_rate,
            'fixed_pass_rate': fixed_pass_rate,
            'improvement': fixed_pass_rate - original_pass_rate,
            'all_tests_pass': all_tests_pass
        }

        style_improvement = {
            'original_score': original_style,
            'fixed_score': fixed_style,
            'improvement': fixed_style - original_style,
            'perfect_style': fixed_style == 100
        }

        # Determine overall status
        if all_tests_pass and style_improvement['perfect_style']:
            fix_status = 'SUCCESSFUL'
            status_emoji = '✅'
        elif test_improvement['improvement'] > 0 or style_improvement['improvement'] > 0:
            fix_status = 'PARTIAL'
            status_emoji = '⚠️'
        else:
            fix_status = 'FAILED'
            status_emoji = '❌'

        # Build comprehensive report
        report = {
            'status': fix_status,
            'status_emoji': status_emoji,
            'timestamp': datetime.now().isoformat(),
            'original_code': original_code,
            'code_fixes': code_fixes,
            'improvements': {
                'tests': test_improvement,
                'style': style_improvement
            },
            'summary': f"{status_emoji} Fix Status: {fix_status}\n"
                      f"Tests: {original_pass_rate:.1f}% → {fixed_pass_rate:.1f}%\n"
                      f"Style: {original_style}/100 → {fixed_style}/100"
        }

        # Store report in state
        tool_context.state[StateKeys.FIX_REPORT] = report
        tool_context.state[StateKeys.FIX_STATUS] = fix_status

        logger.info(f"Tool: Fix report compiled - Status: {fix_status}")
        logger.info(f"Tool: Test improvement: {original_pass_rate:.1f}% → {fixed_pass_rate:.1f}%")
        logger.info(f"Tool: Style improvement: {original_style} → {fixed_style}")

        return {
            "status": "success",
            "fix_status": fix_status,
            "report": report
        }

    except Exception as e:
        logger.error(f"Tool: Failed to compile fix report: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }


def exit_fix_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Signal that fixing is complete and should exit the loop.
   
    Args:
        tool_context: ADK tool context
       
    Returns:
        Confirmation message
    """
    logger.info("Tool: Setting escalate flag to exit fix loop")
   
    # This is the critical line that exits the LoopAgent
    tool_context.actions.escalate = True
   
    return {
        "status": "success",
        "message": "Fix complete, exiting loop"
    }


async def save_fix_report(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Saves the fix report as an artifact.

    Args:
        tool_context: ADK tool context

    Returns:
        Save status
    """
    logger.info("Tool: Saving fix report...")

    try:
        # Get the report from state
        fix_report = tool_context.state.get(StateKeys.FIX_REPORT, {})

        if not fix_report:
            return {
                "status": "error",
                "message": "No fix report found in state"
            }

        # Convert to JSON
        report_json = json.dumps(fix_report, indent=2)
        report_part = types.Part.from_text(text=report_json)

        # Generate filename
        timestamp = datetime.now().isoformat().replace(':', '-')
        filename = f"fix_report_{timestamp}.json"

        # Try to save as artifact
        if hasattr(tool_context, 'save_artifact'):
            try:
                version = await tool_context.save_artifact(filename, report_part)
                await tool_context.save_artifact("latest_fix_report.json", report_part)

                logger.info(f"Tool: Fix report saved as {filename}")

                return {
                    "status": "success",
                    "filename": filename,
                    "version": str(version),
                    "size": len(report_json)
                }
            except Exception as e:
                logger.warning(f"Could not save as artifact: {e}")

        # Fallback: store in state
        tool_context.state[StateKeys.LAST_FIX_REPORT] = fix_report

        return {
            "status": "success",
            "message": "Fix report saved to state",
            "size": len(report_json)
        }

    except Exception as e:
        logger.error(f"Tool: Failed to save fix report: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }


# Module exports
__all__ = [
    'analyze_code_structure',
    'check_code_style',
    'search_past_feedback',
    'update_grading_progress',
    'save_grading_report',
    'validate_fixed_style',
    'compile_fix_report',
    'save_fix_report',
]
# 🤖 AI-Powered Code Review Assistant

**An intelligent multi-agent system for automated code review and fixing**

I built this production-ready code review assistant using Google's Agent Development Kit (ADK) and Gemini AI. The system analyzes Python code, identifies issues, and can automatically fix problems through an iterative refinement process.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![ADK](https://img.shields.io/badge/Google%20ADK-1.15%2B-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5-red)


## 📹 Video Demonstration
[Walkthrough YouTube Video](https://youtu.be/EuK-QJoGaCw)

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      ROOT AGENT                                  │
│                 (Orchestrates Everything)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌────────────────────┐          ┌────────────────────┐
│  REVIEW PIPELINE   │          │   FIX PIPELINE     │
│   (Sequential)     │          │   (Loop-based)     │
└────────────────────┘          └────────────────────┘
         │                               │
         │                               │
    ┌────┴────┐                     ┌────┴────┐
    │         │                     │         │
    ▼         ▼                     ▼         ▼
┌────────┐ ┌────────┐         ┌────────┐ ┌────────┐
│ Code   │ │ Style  │         │ Code   │ │  Fix   │
│Analyzer│→│Checker │         │ Fixer  │→│ Test   │
└────────┘ └────────┘         └────────┘ │ Runner │
    │         │                     ▲     └────────┘
    ▼         ▼                     │         │
┌────────┐ ┌────────┐              │         ▼
│  Test  │ │Feedback│         ┌────────┐ ┌────────┐
│ Runner │→│Synth.  │         │  Fix   │ │  Fix   │
└────────┘ └────────┘         │Valid.  │→│ Synth. │
                               └────────┘ └────────┘
                                    │
                                    └──(Loop max 3x)
```

## 🎯 What I Built

This project implements a sophisticated AI agent system with:

- **Dual Pipeline Architecture**: Separate review and fix workflows that work together
- **4 Specialized Review Agents**: Code analyzer, style checker, test runner, and feedback synthesizer
- **Iterative Fix Loop**: Automatically attempts to fix issues up to 3 times with validation
- **Custom Tools**: AST parsing, PEP 8 style checking, automated test execution
- **Stateful Processing**: Multi-tier state management for tracking code and feedback across agents
- **Production Deployment**: Ready for Google Cloud (Agent Engine or Cloud Run)

## 🔄 Complete Workflow (Step-by-Step)

Here's exactly what happens when you submit code for review:

```
USER SUBMITS CODE
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: REVIEW PIPELINE (Sequential Execution)             │
└──────────────────────────────────────────────────────────────┘
       │
       ├─► Step 1: CODE ANALYZER
       │   • Parses code using Python AST
       │   • Extracts functions, classes, parameters
       │   • Calculates cyclomatic complexity
       │   • Detects syntax errors
       │   • Output: "Syntax Error Detected" OR "Code Structure Analysis"
       │
       ├─► Step 2: STYLE CHECKER (runs in parallel with analyzer)
       │   • Validates against PEP 8 standards
       │   • Checks naming conventions
       │   • Identifies indentation issues
       │   • Output: "Style Score: X/100" + list of violations
       │
       ├─► Step 3: TEST RUNNER
       │   • Executes code in sandboxed environment
       │   • Catches runtime errors (AttributeError, KeyError, etc.)
       │   • Validates logic with test cases
       │   • Output: "Outcome: OK" OR error details
       │
       └─► Step 4: FEEDBACK SYNTHESIZER
           • Aggregates all findings from above agents
           • Searches past feedback for similar issues
           • Generates comprehensive report with:
             - Summary of strengths
             - Critical issues found
             - Specific recommendations
             - Priority-ordered fixes
           • Output: "📊 Summary" with detailed feedback
           • Asks: "💡 I can try to fix these issues for you. Would you like me to do that?"

       ▼
USER ACCEPTS FIX OFFER
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: FIX PIPELINE (Iterative Loop, Max 3 Attempts)      │
└──────────────────────────────────────────────────────────────┘
       │
       ├─► Iteration 1:
       │   ├─► CODE FIXER
       │   │   • Applies corrections based on review feedback
       │   │   • Fixes syntax, style, and logic issues
       │   │   • Output: Fixed code
       │   │
       │   ├─► FIX TEST RUNNER
       │   │   • Re-runs tests on fixed code
       │   │   • Output: Pass rate (e.g., "19/20 tests passed")
       │   │
       │   └─► FIX VALIDATOR
       │       • Checks if all issues resolved
       │       • If YES → Exit loop, go to Fix Synthesizer
       │       • If NO → Loop back to Code Fixer (max 3 times)
       │
       └─► FIX SYNTHESIZER (after loop exits)
           • Compares original vs fixed code
           • Generates final report:
             - "✅ SUCCESSFUL" or "⚠️ PARTIAL"
             - What was fixed
             - Test pass rate improvement
             - Style score improvement
             - Remaining issues (if any)
           • Output: Complete fix summary + final corrected code

       ▼
PROCESS COMPLETE
```

## 🏗️ How It Works (Technical Details)

**Review Pipeline (Sequential Flow)**
1. **Code Analyzer**: Parses Python code using AST to extract functions, classes, and complexity metrics
2. **Style Checker**: Validates code against PEP 8 standards and identifies style violations
3. **Test Runner**: Executes code in a sandboxed environment to catch runtime errors
4. **Feedback Synthesizer**: Aggregates all findings and generates comprehensive feedback

**Fix Pipeline (Iterative Loop)**
1. **Code Fixer**: Applies corrections based on review feedback
2. **Fix Test Runner**: Validates the fixed code still executes correctly
3. **Fix Validator**: Checks if all issues are resolved; exits loop if successful
4. **Fix Synthesizer**: Produces final report with before/after comparison

The system uses **state management** to pass code and feedback between agents, ensuring each agent has the context it needs.

## � Examkple Conversation Flow

**What you see in action:**

```
YOU: "Please analyze the following: def dfs_search_v1(graph, start, target): ..."

SYSTEM (Code Analyzer): 
"Syntax Error Detected: Line 2, offset 1 - expected an indented block"

SYSTEM (Style Checker):
"Style Score: 77/100
Total Issues: 6
- Line 2: E112 expected an indented block
- Line 8: W293 blank line contains whitespace"

SYSTEM (Test Runner):
"Test Results: 16 passed, 1 failed, 3 errors
Critical Issues Found: 2
- AttributeError: stack initialization bug
- KeyError: unsafe node access"

SYSTEM (Feedback Synthesizer):
"📊 Summary: Your DFS implementation has the right logic but critical bugs...
✅ Strengths: Correct algorithm foundation, efficient visited check
💡 Recommendations: Fix indentation, change stack = start to stack = [start]
💡 I can try to fix these issues for you. Would you like me to do that?"

YOU: "Yes, please fix it"

SYSTEM (Fix Pipeline - Iteration 1):
"Applying fixes... Testing... Pass rate: 95% (19/20 tests)
One test still failing, attempting refinement..."

SYSTEM (Fix Synthesizer):
"✅ SUCCESSFUL
Test Results: 80% → 100%
Style Score: 77/100 → 100/100
All critical issues resolved. Here's your corrected code..."
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/ayoisio/code-review-assistant.git
cd code-review-assistant
```

**2. Set up Python environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r code_review_assistant/requirements.txt
```

**4. Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_CLOUD_PROJECT
```

**5. Run the assistant:**
```bash
adk run code_review_assistant
```

## 📂 Project Structure

```
code-review-assistant/
├── code_review_assistant/
│   ├── agent.py                 # Root agent and pipeline orchestration
│   ├── config.py                # Configuration and environment setup
│   ├── constants.py             # State keys and shared constants
│   ├── tools.py                 # Custom tools (AST parser, style checker)
│   ├── services.py              # Business logic and utilities
│   └── sub_agents/
│       ├── review_pipeline/     # Review workflow agents
│       │   ├── code_analyzer.py
│       │   ├── style_checker.py
│       │   ├── test_runner.py
│       │   └── feedback_synthesizer.py
│       └── fix_pipeline/        # Fix workflow agents
│           ├── code_fixer.py
│           ├── fix_test_runner.py
│           ├── fix_validator.py
│           └── fix_synthesizer.py
├── tests/                       # Integration and unit tests
├── deploy.sh                    # Deployment script for GCP
├── Dockerfile                   # Container configuration
└── main.py                      # Entry point
```

## ✨ Key Features

**Intelligent Code Analysis**
- AST-based parsing for accurate code structure extraction
- Cyclomatic complexity calculation
- Function and class detection with parameter analysis

**Style Validation**
- PEP 8 compliance checking
- Naming convention validation
- Indentation and formatting rules

**Automated Testing**
- Sandboxed code execution
- Runtime error detection
- Output validation

**Self-Healing Fixes**
- Iterative refinement with up to 3 attempts
- Validation after each fix attempt
- Automatic loop exit when issues are resolved

**Production Ready**
- Containerized with Docker
- Deployable to Google Cloud Platform
- Observability with Cloud Trace
- Type-safe state management

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
pytest tests/

# Test specific components
pytest tests/test_code_analyzer.py
pytest tests/test_code_review_agent.py

# Test deployed agent
python tests/test_agent_engine.py
```

## � Deyployment

Deploy to Google Cloud using the included script:

```bash
# Deploy to Agent Engine
./deploy.sh agent-engine

# Deploy to Cloud Run
./deploy.sh cloud-run
```

The deployment script handles:
- Building Docker containers
- Pushing to Google Container Registry
- Configuring environment variables
- Setting up Cloud Trace for monitoring

## 🔧 Technical Implementation

**Multi-Agent Orchestration**
- Built using Google ADK's agent framework
- Sequential pipeline for review workflow
- Loop-based pipeline for fix workflow with max iterations
- State passed between agents using type-safe constants

**Custom Tools**
- `analyze_code_structure()`: AST parsing with async execution
- `check_code_style()`: PEP 8 validation with detailed reporting
- `exit_fix_loop()`: Conditional loop termination based on validation

**State Management**
- Three-tier state system (temporary, session, user)
- Type-safe keys defined in `constants.py`
- Prevents state key typos across multi-agent workflows

**Performance Optimization**
- Async/await for concurrent operations
- Thread pools for CPU-bound tasks
- Efficient state serialization

## 📸 Project Output

![Screenshot 1](ss1.png)

![Screenshot 2](ss2.png)

![Screenshot 3](ss3.png)

![Screenshot 4](ss4.png)

![Screenshot 5](ss5.png)

![Screenshot 6](ss6.png)


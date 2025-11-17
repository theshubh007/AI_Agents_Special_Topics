# Implementation Plan

- [x] 1. Initialize ADK project structure


  - Use agent-starter-pack to create the base project with FastAPI server and agent definition
  - Verify pyproject.toml includes all required ADK dependencies
  - Verify app/agent.py and app/server.py files are created
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Implement gemini_cli tool function


  - [x] 2.1 Create gemini_cli function with task and github_url parameters


    - Define function signature with proper type hints and docstring
    - Add function to app/agent.py
    - _Requirements: 2.1, 2.2_
  
  - [x] 2.2 Implement repository cloning logic

    - Extract repository name from GitHub URL
    - Check if /tmp/{repo_name} directory exists
    - Execute git clone command if directory doesn't exist
    - Handle git clone errors and return descriptive error messages
    - Implement 300-second timeout for git clone operations
    - _Requirements: 2.3, 2.8_
  
  - [x] 2.3 Implement Gemini CLI execution logic

    - Construct gemini command with -p flag and task prompt
    - Execute command with cwd set to cloned repository directory
    - Capture stdout and stderr from subprocess
    - Return stdout on success, stderr on failure
    - Implement 600-second timeout for Gemini CLI execution
    - _Requirements: 2.4, 2.5, 2.6, 2.7, 2.9_
  
  - [x] 2.4 Add error handling and exception management

    - Catch subprocess.TimeoutExpired for timeout scenarios
    - Catch general exceptions for unexpected errors
    - Return user-friendly error messages for all failure cases
    - _Requirements: 2.7_

- [x] 3. Configure ADK root agent


  - [x] 3.1 Define root agent with proper configuration

    - Set agent name to "root_agent"
    - Configure model as "gemini-2.5-pro"
    - Write agent instructions that identify it as a world-class Software Developer
    - Add explicit instruction to always use the Gemini CLI tool
    - Register gemini_cli function in tools list
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Create Dockerfile with all dependencies


  - [x] 4.1 Set up base image and system dependencies


    - Use python:3.11-slim as base image
    - Install curl, git via apt-get
    - Install Node.js 20.x using NodeSource setup script
    - Clean up apt cache to reduce image size
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [x] 4.2 Install Gemini CLI and Python tools

    - Install Gemini CLI globally using npm install -g @google/gemini-cli
    - Install uv package manager version 0.6.12
    - _Requirements: 4.4, 4.5_
  
  - [x] 4.3 Configure application and startup

    - Set WORKDIR to /code
    - Copy pyproject.toml, README.md, uv.lock, and app/ directory
    - Run uv sync --frozen to install Python dependencies
    - Add COMMIT_SHA build argument
    - Expose port 8080
    - Set CMD to start ADK web interface: adk web --host 0.0.0.0 --port 8080 .
    - _Requirements: 4.6, 4.7_

- [x] 5. Create Cloud Build configuration


  - [x] 5.1 Define Docker build step


    - Configure docker build command with COMMIT_SHA build arg
    - Tag image as us-central1-docker.pkg.dev/$PROJECT_ID/container/gemini-cli-adk:latest
    - _Requirements: 5.2_
  
  - [x] 5.2 Define image push step

    - Configure docker push command to Artifact Registry
    - Use us-central1 region
    - _Requirements: 5.3_
  
  - [x] 5.3 Define Cloud Run deployment step

    - Configure gcloud run deploy command
    - Set service name to gemini-cli-adk
    - Set region to us-central1
    - Reference latest image from Artifact Registry
    - _Requirements: 5.4, 5.5_

- [x] 6. Configure web interface and user interaction


  - [x] 6.1 Verify ADK web interface functionality


    - Ensure adk web command starts successfully
    - Verify web interface is accessible on port 8080
    - Test that interface accepts user input for task and GitHub URL
    - _Requirements: 6.1, 6.2_
  
  - [x] 6.2 Test agent request handling

    - Verify agent receives user requests correctly
    - Verify agent invokes gemini_cli tool with correct parameters
    - Verify agent presents tool results back to user
    - _Requirements: 6.3, 6.4_

- [x] 7. Configure Cloud Run deployment settings



  - [x] 7.1 Set up Cloud Run service configuration


    - Configure service to scale to zero when idle
    - Enable automatic scaling for traffic increases
    - Set request timeout to 3600 seconds (60 minutes)
    - Configure IAM-based authentication
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ]* 8. Create unit tests for gemini_cli function
  - Write test for successful repository clone and CLI execution
  - Write test for repository caching (no re-clone on second call)
  - Write test for git clone timeout handling
  - Write test for Gemini CLI timeout handling
  - Write test for invalid GitHub URL handling
  - Write test for subprocess error handling
  - Mock subprocess.run, os.path.exists, and os.environ
  - _Requirements: 2.1-2.9_

- [ ]* 9. Create integration tests
  - Write test for full agent workflow with tool invocation
  - Write test for agent handling tool response
  - Write test for end-to-end flow with test GitHub repository
  - Set up test environment with small test repository
  - _Requirements: 3.1-3.4, 6.1-6.4_

- [ ]* 10. Create container and deployment tests
  - Write test to verify all dependencies in Docker image
  - Write test to verify Gemini CLI is executable
  - Write test to verify ADK web server starts
  - Write test to verify port 8080 accessibility
  - Create deployment test for Cloud Run service
  - _Requirements: 4.1-4.7, 5.1-5.5, 7.1-7.4_

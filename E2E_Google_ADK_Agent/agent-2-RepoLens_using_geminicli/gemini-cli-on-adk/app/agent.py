# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import subprocess
import tempfile

import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App

# Set project configuration - prioritize environment variable, then auth default
if "GOOGLE_CLOUD_PROJECT" not in os.environ:
    try:
        _, project_id = google.auth.default()
        if project_id:
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        else:
            # Fallback to the actual project ID
            os.environ["GOOGLE_CLOUD_PROJECT"] = "gen-lang-client-0125998383"
    except Exception as e:
        print(f"Warning: Google Cloud credentials not found: {e}")
        print("Using fallback project ID.")
        os.environ["GOOGLE_CLOUD_PROJECT"] = "gen-lang-client-0125998383"

os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

print(f"Using Google Cloud Project: {os.environ.get('GOOGLE_CLOUD_PROJECT')}")


def gemini_cli(task: str, github_url: str) -> str:
    """Executes the Gemini CLI.
    
    Args:
        task: The task to pass to Gemini CLI, eg: explain this codebase, generate a test plan, etc.
        github_url: GitHub URL to clone and analyze.
    
    Returns:
        The response from the Gemini CLI.
    """
    try:
        # Extract repository name from GitHub URL to create local directory
        repo_name = github_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        
        # Use system temp directory (works on both Windows and Unix)
        temp_base = tempfile.gettempdir()
        codebaseDir = os.path.join(temp_base, repo_name)
        
        # Clone the repo if directory doesn't exist
        if not os.path.exists(codebaseDir):
            print(f"Directory {codebaseDir} doesn't exist. Cloning from {github_url}...")
            # Use shallow clone with depth=1 and configure git to use less memory
            git_env = os.environ.copy()
            # Limit git memory usage
            git_env['GIT_CONFIG_COUNT'] = '2'
            git_env['GIT_CONFIG_KEY_0'] = 'pack.windowMemory'
            git_env['GIT_CONFIG_VALUE_0'] = '10m'
            git_env['GIT_CONFIG_KEY_1'] = 'pack.packSizeLimit'
            git_env['GIT_CONFIG_VALUE_1'] = '20m'
            
            clone_command = ['git', 'clone', '--depth', '1', '--single-branch', github_url, codebaseDir]
            clone_result = subprocess.run(
                clone_command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout for git clone
                env=git_env,
            )
            
            if clone_result.returncode != 0:
                # Clean up partial clone if it exists
                if os.path.exists(codebaseDir):
                    try:
                        shutil.rmtree(codebaseDir)
                        print(f"Cleaned up partial clone at {codebaseDir}")
                    except Exception as e:
                        print(f"Warning: Could not clean up partial clone: {e}")
                
                error_msg = f"Error cloning repository:\nSTDERR: {clone_result.stderr}\nSTDOUT: {clone_result.stdout}\nReturn code: {clone_result.returncode}"
                print(error_msg)
                return error_msg
            
            print(f"Successfully cloned repository to {codebaseDir}")
        else:
            print(f"Repository already exists at {codebaseDir}, using cached version")
        
        # Construct the gemini command
        print(f"Executing Gemini CLI in {codebaseDir} with task: {task[:100]}...")
        # Use full path to gemini CLI on Windows
        gemini_path = 'gemini'
        if os.name == 'nt':  # Windows
            npm_prefix = os.path.expandvars(r'%APPDATA%\npm')
            gemini_cmd = os.path.join(npm_prefix, 'gemini.cmd')
            if os.path.exists(gemini_cmd):
                gemini_path = gemini_cmd
        
        # Use positional argument instead of deprecated -p flag
        command = [gemini_path, task]
        
        # Execute the command in the specified directory
        env = os.environ.copy()
        
        # Try to use GEMINI_API_KEY if available, otherwise fall back to Vertex AI
        if 'GEMINI_API_KEY' in os.environ:
            env['GEMINI_API_KEY'] = os.environ['GEMINI_API_KEY']
            print("Using Gemini API Key for authentication")
        else:
            # Ensure Gemini CLI uses Vertex AI authentication
            env['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
            env['GOOGLE_CLOUD_PROJECT'] = os.environ.get('GOOGLE_CLOUD_PROJECT', 'gen-lang-client-0125998383')
            env['GOOGLE_CLOUD_LOCATION'] = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')
            print("Using Vertex AI for authentication")
        
        # Increase Node.js memory limit for Gemini CLI
        env['NODE_OPTIONS'] = '--max-old-space-size=4096'
        
        # Also create settings file if it doesn't exist
        gemini_settings_dir = os.path.expanduser('~/.gemini')
        gemini_settings_file = os.path.join(gemini_settings_dir, 'settings.json')
        if not os.path.exists(gemini_settings_file):
            os.makedirs(gemini_settings_dir, exist_ok=True)
            import json
            settings = {
                "auth": "vertexai",
                "project": env['GOOGLE_CLOUD_PROJECT'],
                "location": env['GOOGLE_CLOUD_LOCATION']
            }
            with open(gemini_settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print(f"Created Gemini CLI settings at {gemini_settings_file}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes timeout for Gemini CLI execution
            cwd=codebaseDir,
            env=env,
        )
        
        # Return the stdout directly as the response
        if result.returncode == 0:
            print(f"Gemini CLI executed successfully")
            return result.stdout
        else:
            error_msg = f"Error executing Gemini CLI:\nSTDERR: {result.stderr}\nSTDOUT: {result.stdout}\nReturn code: {result.returncode}"
            print(error_msg)
            return error_msg
    
    except subprocess.TimeoutExpired:
        return "Gemini CLI command timed out after 600 seconds"
    except Exception as e:
        return f"Failed to execute Gemini CLI: {str(e)}"


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    instruction="""
    You are a world class Software Developer and you have a very powerful tool - Gemini CLI to help analyze code, generating test plan, generating unit tests, etc.
    
    The codebase is cloned from a GitHub repository and stored in the system's temporary directory. Always use the Gemini CLI tool to analyze the codebase and complete the user's request.
    """,
    tools=[gemini_cli],
)

app = App(root_agent=root_agent, name="app")

import requests
import json
import os
from dotenv import load_dotenv
from google.auth import default
from google.auth.transport.requests import Request

load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
agent_engine_id = os.getenv("AGENT_ENGINE_ID")

if not agent_engine_id:
    raise ValueError(
        "AGENT_ENGINE_ID is not set in your .env file. "
        "Please copy the ID from your deployment output and add it to the .env file."
    )
if not project_id or not location:
     raise ValueError(
        "GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in your .env file."
    )


# Get credentials for authentication
credentials, auth_project_id = default()
credentials.refresh(Request())
print(f"Authenticated with project: {auth_project_id}")


# Determine resource path
base_url = f"https://{location}-aiplatform.googleapis.com/v1"
resource_path = f"projects/{project_id}/locations/{location}/reasoningEngines/{agent_engine_id}"
print(f"Targeting Agent Engine: {resource_path}\n")

headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

# Create session
print("Creating new session...")
session_response = requests.post(
    f"{base_url}/{resource_path}:query",
    headers=headers,
    json={
        "class_method": "create_session",
        "input": {"user_id": "test_user"}
    }
)
session_response.raise_for_status() # Raise an exception for bad status codes

session_data = session_response.json()
session_id = session_data["output"]["id"]
print(f"Created session: {session_id}")


# --- Send query to the agent for processing ---
print("\nSending query to agent and streaming response:")

# Let's use one of the more complex LeetCode problems as our test message
message_to_agent = """
Please analyze ```

def dfs_search_v1(graph, start, target):
    visited = set()
    stack = start

    while stack:
        current = stack.pop()

        if current == target:
            return True

        if current not in visited:
            visited.add(current)

            for neighbor in graph[current]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return False
```
"""

query_response = requests.post(
    f"{base_url}/{resource_path}:streamQuery?alt=sse",
    headers=headers,
    stream=True,
    json={
        "class_method": "async_stream_query",
        "input": {
            "user_id": "test_user",
            "session_id": session_id,
            "message": message_to_agent
        }
    }
)
query_response.raise_for_status()

# Loop through the streaming response
for line in query_response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        print(line_str)

print("\n\nStream finished.")
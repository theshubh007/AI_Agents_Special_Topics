# main.py
import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Get credentials from environment variables
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "code-review-assistant-artifacts")

# Build the session URI if we have all database credentials
if all([DB_USER, DB_PASSWORD, DB_NAME, CLOUD_SQL_CONNECTION_NAME]):
    SESSION_SERVICE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
    print(f"Using Cloud SQL for session persistence")
else:
    SESSION_SERVICE_URI = ""  # Falls back to in-memory
    print("Using in-memory session service (no database credentials provided)")

# Create the FastAPI app with ADK
app = get_fast_api_app(
    agents_dir=os.path.dirname(os.path.abspath(__file__)),
    session_service_uri=SESSION_SERVICE_URI,
    artifact_service_uri=f"gs://{ARTIFACT_BUCKET}",
    allow_origins=["*"],
    web=True,
    trace_to_cloud=True
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

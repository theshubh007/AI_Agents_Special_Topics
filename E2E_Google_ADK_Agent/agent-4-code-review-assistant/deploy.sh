#!/bin/bash
# A unified script for deploying and running the Code Review Assistant.
# This is the single source of truth for all deployment and runtime configurations.

set -e

# --- Configuration ---
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT:-"your-gcp-project-id"}
GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION:-"us-central1"}
SERVICE_NAME="code-review-assistant"
DEFAULT_SQL_INSTANCE_NAME="${SERVICE_NAME}-db-instance"
DEFAULT_DB_NAME="sessions"
DEFAULT_DB_USER="adk-user"
DEFAULT_ARTIFACT_BUCKET="${SERVICE_NAME}-artifacts"
DEFAULT_STAGING_BUCKET="${SERVICE_NAME}-staging"

# --- Helper Functions ---

usage() {
    echo "Usage: $0 {local|cloud-run|agent-engine}"
    echo ""
    echo "Commands:"
    echo "  local         - 🚀 Run the agent locally with a purely in-memory database for quick testing."
    echo "  cloud-run     - ☁️  Deploy to Cloud Run with a user-managed Cloud SQL database for persistence."
    echo "  agent-engine  - 🧠 Deploy to Vertex AI Agent Engine for a fully managed, stateful agent endpoint."
}

validate_cloud_env() {
    if [ "$GOOGLE_CLOUD_PROJECT" == "your-gcp-project-id" ]; then
        echo "❌ Error: GOOGLE_CLOUD_PROJECT is not set. Please update your .env file or run 'gcloud config set project <id>'."
        exit 1
    fi
}

ensure_apis_enabled_for_cloud_run() {
    echo "🔧 Checking and enabling required Google Cloud APIs for Cloud Run..."

    REQUIRED_APIS=(
        "sqladmin.googleapis.com"
        "run.googleapis.com"
        "cloudbuild.googleapis.com"
        "artifactregistry.googleapis.com"
        "compute.googleapis.com"
        "aiplatform.googleapis.com"
        "storage.googleapis.com"
        "cloudtrace.googleapis.com"
    )

    for API in "${REQUIRED_APIS[@]}"; do
        if ! gcloud services list --enabled --filter="name:${API}" --format="value(name)" --project="${GOOGLE_CLOUD_PROJECT}" 2>/dev/null | grep -q "${API}"; then
            echo "   - Enabling ${API}..."
            if gcloud services enable "${API}" --project="${GOOGLE_CLOUD_PROJECT}"; then
                echo "   - ${API} enabled successfully. Waiting for propagation..."
                sleep 5  # Give the API a moment to fully activate
            else
                echo "   ⚠️  Warning: Failed to enable ${API}. You may need to enable it manually."
            fi
        else
            echo "   - ${API} is already enabled."
        fi
    done

    echo "   - All required APIs for Cloud Run are processed."
}

ensure_apis_enabled_for_agent_engine() {
    echo "🔧 Checking and enabling required Google Cloud APIs for Agent Engine..."

    REQUIRED_APIS=(
        "aiplatform.googleapis.com"
        "storage.googleapis.com"
        "cloudbuild.googleapis.com"
        "compute.googleapis.com"
        "cloudtrace.googleapis.com"
    )

    for API in "${REQUIRED_APIS[@]}"; do
        if ! gcloud services list --enabled --filter="name:${API}" --format="value(name)" --project="${GOOGLE_CLOUD_PROJECT}" 2>/dev/null | grep -q "${API}"; then
            echo "   - Enabling ${API}..."
            if gcloud services enable "${API}" --project="${GOOGLE_CLOUD_PROJECT}"; then
                echo "   - ${API} enabled successfully. Waiting for propagation..."
                sleep 5  # Give the API a moment to fully activate
            else
                echo "   ⚠️  Warning: Failed to enable ${API}. You may need to enable it manually."
            fi
        else
            echo "   - ${API} is already enabled."
        fi
    done

    echo "   - All required APIs for Agent Engine are processed."
}

ensure_bucket_exists() {
    local BUCKET_NAME=$1
    local PURPOSE=$2

    # Remove gs:// prefix if present
    BUCKET_NAME=${BUCKET_NAME#gs://}

    if ! gsutil ls -b "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
        echo "   - Creating ${PURPOSE} bucket: gs://${BUCKET_NAME}..."
        gsutil mb -p "$GOOGLE_CLOUD_PROJECT" -l "$GOOGLE_CLOUD_LOCATION" "gs://${BUCKET_NAME}"

        # Get the service account
        PROJECT_NUMBER=$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format="value(projectNumber)")
        SERVICE_ACCOUNT="$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

        # Set uniform bucket-level access (recommended)
        gsutil iam ch serviceAccount:${SERVICE_ACCOUNT}:objectAdmin "gs://${BUCKET_NAME}"
        echo "   - ${PURPOSE} bucket created and permissions set successfully."
    else
        echo "   - Using existing ${PURPOSE} bucket: gs://${BUCKET_NAME}"
    fi
}

ensure_staging_bucket_exists() {
    local BUCKET_NAME=$1

    # Remove gs:// prefix if present
    BUCKET_NAME=${BUCKET_NAME#gs://}

    if ! gsutil ls -b "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
        echo "   - Creating staging bucket: gs://${BUCKET_NAME}..."
        gsutil mb -p "$GOOGLE_CLOUD_PROJECT" -l "$GOOGLE_CLOUD_LOCATION" "gs://${BUCKET_NAME}"
        echo "   - Staging bucket created successfully."
    else
        echo "   - Using existing staging bucket: gs://${BUCKET_NAME}"
    fi
}

ensure_artifact_registry_exists() {
    local REPO_NAME=$1

    echo "🔍 Checking for Artifact Registry repository '$REPO_NAME'..."

    if ! gcloud artifacts repositories describe "$REPO_NAME" \
        --location="$GOOGLE_CLOUD_LOCATION" \
        --project="$GOOGLE_CLOUD_PROJECT" >/dev/null 2>&1; then

        echo "   - Creating Artifact Registry repository '$REPO_NAME'..."
        gcloud artifacts repositories create "$REPO_NAME" \
            --repository-format=docker \
            --location="$GOOGLE_CLOUD_LOCATION" \
            --project="$GOOGLE_CLOUD_PROJECT" \
            --description="Docker repository for $SERVICE_NAME"
        echo "   - Artifact Registry repository created successfully."
    else
        echo "   - Using existing Artifact Registry repository '$REPO_NAME'."
    fi
}

ensure_iam_permissions_for_cloud_run() {
    echo "🔐 Granting the Compute Engine default service account necessary permissions..."
    PROJECT_NUMBER=$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format="value(projectNumber)")
    SERVICE_ACCOUNT="$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

    # Cloud SQL Client permission
    echo "   - Granting Cloud SQL Client role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/cloudsql.client" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Cloud SQL Client role may already be assigned."

    # Storage Object Admin permission for artifacts
    echo "   - Granting Storage Object Admin role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/storage.objectAdmin" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Storage Object Admin role may already be assigned."

    # Artifact Registry Writer permission (includes read) for Docker images
    echo "   - Granting Artifact Registry Writer role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/artifactregistry.writer" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Artifact Registry Writer role may already be assigned."

    # Vertex AI User permission for model access
    echo "   - Granting Vertex AI User role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/aiplatform.user" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Vertex AI User role may already be assigned."

    # Cloud Trace Agent permission for trace data
    echo "   - Granting Cloud Trace Agent role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/cloudtrace.agent" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Cloud Trace Agent role may already be assigned."

    echo "   - IAM permissions configuration complete."
}

ensure_iam_permissions_for_agent_engine() {
    echo "🔐 Granting necessary permissions for Agent Engine..."
    PROJECT_NUMBER=$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format="value(projectNumber)")
    SERVICE_ACCOUNT="$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

    # Storage Object Admin permission for artifacts and staging
    echo "   - Granting Storage Object Admin role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/storage.objectAdmin" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Storage Object Admin role may already be assigned."

    # Vertex AI User permission
    echo "   - Granting Vertex AI User role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/aiplatform.user" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Vertex AI User role may already be assigned."

    # Cloud Trace Agent permission for trace data
    echo "   - Granting Cloud Trace Agent role..."
    gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/cloudtrace.agent" \
        --condition=None \
        --quiet 2>/dev/null || echo "   ⚠️  Cloud Trace Agent role may already be assigned."

    echo "   - IAM permissions configuration complete."
}

# --- Main Script Logic ---

if [ -z "$1" ]; then
    usage
    exit 1
fi

case "$1" in
    local)
        echo "🚀 Starting local development server (In-Memory Sessions and Artifacts)..."
        adk web --port 8080 --host 0.0.0.0 --session_service_uri "" --reload
        ;;

    cloud-run)
        validate_cloud_env
        echo "☁️  Deploying to Cloud Run with Cloud SQL Persistence..."

        # Enable required APIs first
        ensure_apis_enabled_for_cloud_run

        # Set up IAM permissions
        ensure_iam_permissions_for_cloud_run

        # Set up artifact bucket
        if [ -z "$ARTIFACT_BUCKET" ]; then
            ARTIFACT_BUCKET="$DEFAULT_ARTIFACT_BUCKET"
        fi
        ensure_bucket_exists "$ARTIFACT_BUCKET" "artifact storage"

        # Check for Cloud SQL instance
        if [ -z "$CLOUD_SQL_INSTANCE_NAME" ]; then
            echo "🔎 No Cloud SQL instance specified. Checking for default instance '$DEFAULT_SQL_INSTANCE_NAME'..."
            if ! gcloud sql instances describe "$DEFAULT_SQL_INSTANCE_NAME" --project="$GOOGLE_CLOUD_PROJECT" >/dev/null 2>&1; then
                echo "   - Default instance not found. Creating a new Cloud SQL for PostgreSQL instance..."
                echo "   - This will take about 10-15 minutes."

                # Generate secure password
                DB_PASSWORD=$(openssl rand -base64 16)

                # Create Cloud SQL instance
                if gcloud sql instances create "$DEFAULT_SQL_INSTANCE_NAME" \
                    --database-version=POSTGRES_15 \
                    --region="$GOOGLE_CLOUD_LOCATION" \
                    --root-password="$DB_PASSWORD" \
                    --tier=db-g1-small \
                    --project="$GOOGLE_CLOUD_PROJECT"; then

                    # Create database
                    gcloud sql databases create "$DEFAULT_DB_NAME" \
                        --instance="$DEFAULT_SQL_INSTANCE_NAME" \
                        --project="$GOOGLE_CLOUD_PROJECT"

                    # Create user
                    gcloud sql users create "$DEFAULT_DB_USER" \
                        --instance="$DEFAULT_SQL_INSTANCE_NAME" \
                        --password="$DB_PASSWORD" \
                        --project="$GOOGLE_CLOUD_PROJECT"

                    echo "✅ Successfully created Cloud SQL instance and database."
                    echo ""
                    echo "   ⚠️  PLEASE SAVE THESE CREDENTIALS IN A SECURE LOCATION (e.g., Secret Manager):"
                    echo "   ============================================================"
                    echo "   CLOUD_SQL_INSTANCE_NAME: $DEFAULT_SQL_INSTANCE_NAME"
                    echo "   DB_NAME:                 $DEFAULT_DB_NAME"
                    echo "   DB_USER:                 $DEFAULT_DB_USER"
                    echo "   DB_PASSWORD:             $DB_PASSWORD"
                    echo "   ============================================================"
                    echo ""
                    echo "   You can add these to your .env file for future deployments."
                    echo ""

                    export CLOUD_SQL_INSTANCE_NAME="$DEFAULT_SQL_INSTANCE_NAME"
                    export DB_NAME="$DEFAULT_DB_NAME"
                    export DB_USER="$DEFAULT_DB_USER"
                    export DB_PASSWORD="$DB_PASSWORD"
                else
                    echo "❌ Error: Failed to create Cloud SQL instance."
                    exit 1
                fi
            else
                echo "   - Found existing default instance. Using '$DEFAULT_SQL_INSTANCE_NAME'."
                echo "   ⚠️  Make sure you have the DB_USER and DB_PASSWORD set in your .env file."
                export CLOUD_SQL_INSTANCE_NAME="$DEFAULT_SQL_INSTANCE_NAME"

                # Check if credentials are provided
                if [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
                    echo "❌ Error: Found existing Cloud SQL instance but missing credentials."
                    echo "   Please set DB_USER, DB_PASSWORD, and DB_NAME in your .env file."
                    exit 1
                fi
            fi
        else
            echo "   - Using specified Cloud SQL instance: $CLOUD_SQL_INSTANCE_NAME"

            # Verify credentials are provided
            if [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
                echo "❌ Error: Cloud SQL instance specified but missing credentials."
                echo "   Please set DB_USER, DB_PASSWORD, and DB_NAME in your .env file."
                exit 1
            fi
        fi

        # Get Cloud SQL connection name
        CLOUD_SQL_CONNECTION_NAME=$(gcloud sql instances describe "$CLOUD_SQL_INSTANCE_NAME" \
            --format="value(connectionName)" \
            --project="$GOOGLE_CLOUD_PROJECT")

        if [ -z "$CLOUD_SQL_CONNECTION_NAME" ]; then
            echo "❌ Error: Could not retrieve Cloud SQL connection name."
            exit 1
        fi

        echo "📦 Deploying with ADK CLI..."
        echo "   - Project: $GOOGLE_CLOUD_PROJECT"
        echo "   - Region: $GOOGLE_CLOUD_LOCATION"
        echo "   - Service: $SERVICE_NAME"
        echo "   - Artifact service: GCS bucket gs://$ARTIFACT_BUCKET"
        echo ""
        echo "   Note: Session service URI will be configured via environment variables"
        echo "   to work around ADK CLI parsing issues."
        echo ""

        # Deploy with ADK CLI WITHOUT session_service_uri to avoid parsing bug
        if adk deploy cloud_run \
            --project="$GOOGLE_CLOUD_PROJECT" \
            --region="$GOOGLE_CLOUD_LOCATION" \
            --service_name="$SERVICE_NAME" \
            --app_name="code_review_assistant" \
            --port=8080 \
            --with_ui \
            --artifact_service_uri="gs://$ARTIFACT_BUCKET" \
            --trace_to_cloud \
            code_review_assistant; then

            echo ""
            echo "🔗 Updating Cloud Run service with Cloud SQL connection..."

            # Update the service to add Cloud SQL connection and database credentials
            if gcloud run services update "$SERVICE_NAME" \
                --add-cloudsql-instances="$CLOUD_SQL_CONNECTION_NAME" \
                --update-env-vars="DB_USER=$DB_USER,DB_PASSWORD=$DB_PASSWORD,DB_NAME=$DB_NAME,CLOUD_SQL_CONNECTION_NAME=$CLOUD_SQL_CONNECTION_NAME,ARTIFACT_BUCKET=$ARTIFACT_BUCKET" \
                --region="$GOOGLE_CLOUD_LOCATION" \
                --project="$GOOGLE_CLOUD_PROJECT"; then

                echo "✅ Cloud SQL connection configured successfully!"
            else
                echo "⚠️  Warning: Failed to add Cloud SQL connection. The service may use in-memory sessions."
            fi

            echo ""
            echo "✅ Deployment complete!"
            echo "   Your Code Review Assistant is now running on Cloud Run."

            # Trim any whitespace from project ID and get service URL
            PROJECT_TRIMMED=$(echo "$GOOGLE_CLOUD_PROJECT" | tr -d '[:space:]')
            SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
                --region="$GOOGLE_CLOUD_LOCATION" \
                --project="$PROJECT_TRIMMED" \
                --format="value(status.url)" 2>/dev/null)

            if [ -n "$SERVICE_URL" ]; then
                echo "   Service URL: $SERVICE_URL"
            fi
        else
            echo "❌ Error: Deployment failed. Please check the error messages above."
            exit 1
        fi
        ;;

    agent-engine)
        validate_cloud_env
        echo "🧠 Deploying to Vertex AI Agent Engine (Fully Managed Persistence)..."
        echo "   - Enabling Cloud Trace for observability."

        # Enable required APIs first
        ensure_apis_enabled_for_agent_engine

        # Set up IAM permissions
        ensure_iam_permissions_for_agent_engine

        # Set up staging bucket
        if [ -z "$STAGING_BUCKET" ]; then
            STAGING_BUCKET="gs://$DEFAULT_STAGING_BUCKET"
            echo "   - No staging bucket specified. Will use default: $STAGING_BUCKET"
        fi
        ensure_staging_bucket_exists "$STAGING_BUCKET"

        # Set up artifact bucket (Agent Engine also needs runtime artifact storage)
        if [ -z "$ARTIFACT_BUCKET" ]; then
            ARTIFACT_BUCKET="$DEFAULT_ARTIFACT_BUCKET"
        fi
        ensure_bucket_exists "$ARTIFACT_BUCKET" "artifact storage"

        # Note: Agent Engine handles environment variables differently
        # The ARTIFACT_BUCKET will be available to the agent code via os.environ
        export ARTIFACT_BUCKET="$ARTIFACT_BUCKET"

        echo "📦 Deploying with ADK CLI..."
        echo "   - Project: $GOOGLE_CLOUD_PROJECT"
        echo "   - Region: $GOOGLE_CLOUD_LOCATION"
        echo "   - Staging: $STAGING_BUCKET"
        echo ""

        if [ -n "$AGENT_ENGINE_ID" ]; then
            echo "   - Updating existing Agent Engine: $AGENT_ENGINE_ID"
            if adk deploy agent_engine \
                --project="$GOOGLE_CLOUD_PROJECT" \
                --region="$GOOGLE_CLOUD_LOCATION" \
                --staging_bucket="$STAGING_BUCKET" \
                --agent_engine_id="$AGENT_ENGINE_ID" \
                --trace_to_cloud \
                code_review_assistant; then

                echo ""
                echo "✅ Agent Engine updated successfully!"
            else
                echo "❌ Error: Agent Engine update failed."
                exit 1
            fi
        else
            echo "   - Creating new Agent Engine deployment."
            if adk deploy agent_engine \
                --project="$GOOGLE_CLOUD_PROJECT" \
                --region="$GOOGLE_CLOUD_LOCATION" \
                --staging_bucket="$STAGING_BUCKET" \
                --display_name="Code Review Assistant" \
                --trace_to_cloud \
                code_review_assistant; then

                echo ""
                echo "✅ Agent Engine created successfully!"
                echo "   ⚠️  IMPORTANT: Save the Agent Engine ID shown above in your .env file"
                echo "   for future updates (as AGENT_ENGINE_ID=<the-id>)."
            else
                echo "❌ Error: Agent Engine creation failed."
                echo "   Check the logs for details. Common issues:"
                echo "   - Missing requirements.txt file"
                echo "   - Import errors in the agent code"
                echo "   - API quota issues"
                exit 1
            fi
        fi
        ;;

    *)
        echo "❌ Error: Invalid command '$1'"
        usage
        exit 1
        ;;
esac
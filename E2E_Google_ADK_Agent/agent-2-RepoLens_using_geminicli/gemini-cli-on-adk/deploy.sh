#!/bin/bash

# Deployment script for Gemini CLI ADK Agent to Cloud Run

set -e

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}
REGION="us-central1"
SERVICE_NAME="gemini-cli-adk"
IMAGE_NAME="us-central1-docker.pkg.dev/${PROJECT_ID}/container/${SERVICE_NAME}:latest"

echo "Deploying ${SERVICE_NAME} to Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Image: ${IMAGE_NAME}"

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com \
  --project=${PROJECT_ID}

# Create Artifact Registry repository if it doesn't exist
echo "Creating Artifact Registry repository..."
gcloud artifacts repositories create container \
  --repository-format=docker \
  --location=${REGION} \
  --project=${PROJECT_ID} \
  2>/dev/null || echo "Repository already exists"

# Build and deploy using Cloud Build
echo "Building and deploying with Cloud Build..."
gcloud builds submit \
  --config=cloudbuild.yaml \
  --project=${PROJECT_ID}

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --region=${REGION} \
  --project=${PROJECT_ID} \
  --format='value(status.url)')

echo ""
echo "✅ Deployment complete!"
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "To test the agent, visit: ${SERVICE_URL}"

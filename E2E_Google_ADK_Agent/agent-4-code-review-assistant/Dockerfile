# Stage 1: The Builder
# This stage installs all dependencies, including those needed for specific deployments.
FROM python:3.11-slim as builder

WORKDIR /app

# Install poetry for dependency management
RUN pip install poetry

# Copy only the dependency files first to leverage Docker's layer caching.
# If these files don't change, this layer won't be rebuilt.
COPY pyproject.toml poetry.lock* ./

# Install project dependencies using poetry.
# We also install psycopg2-binary using pip, which is the required
# PostgreSQL driver for connecting to Cloud SQL.
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi && \
    pip install psycopg2-binary

# Copy the rest of the application code
COPY code_review_assistant/ ./code_review_assistant/

# ---
# Stage 2: The Final Production Image
# This stage creates a lean, secure image using the artifacts from the builder.
FROM python:3.11-slim

WORKDIR /app

# Copy the installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application code from the builder stage
COPY --from=builder /app /app

# Create a dedicated, non-root user for security best practices
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables. These can be overridden at runtime by Cloud Run or Docker.
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
# This provides a fallback for manual 'docker run' commands, but our deploy.sh script
# will always provide the correct URI for the target environment.
ENV SESSION_SERVICE_URI="sqlite:///./sessions.db"

# This is the command that will be run when the container starts.
# It's simple and flexible: it just runs the ADK API server and expects the
# session service URI to be provided as an environment variable.
CMD ["sh", "-c", "adk api_server code_review_assistant --port ${PORT:-8080} --host 0.0.0.0 --session_service_uri \"$SESSION_SERVICE_URI\" --artifact_service_uri \"$ARTIFACT_SERVICE_URI\""]
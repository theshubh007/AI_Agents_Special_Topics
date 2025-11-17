# Windows Run Script for Gemini CLI ADK Agent

Write-Host "Starting Gemini CLI ADK Agent..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Running setup..." -ForegroundColor Yellow
    & .\setup-windows.ps1
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if authenticated with Google Cloud
Write-Host "`nChecking Google Cloud authentication..." -ForegroundColor Yellow
try {
    $project = gcloud config get-value project 2>$null
    if ($project) {
        Write-Host "✓ Google Cloud project: $project" -ForegroundColor Green
    } else {
        Write-Host "⚠ No Google Cloud project set" -ForegroundColor Yellow
        Write-Host "Please run: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠ Google Cloud SDK not configured" -ForegroundColor Yellow
    Write-Host "Please run:" -ForegroundColor Cyan
    Write-Host "  gcloud auth login --update-adc" -ForegroundColor Cyan
    Write-Host "  gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Cyan
}

# Start the agent
Write-Host "`nStarting ADK web interface on http://localhost:8080..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m adk web --host 0.0.0.0 --port 8080 .

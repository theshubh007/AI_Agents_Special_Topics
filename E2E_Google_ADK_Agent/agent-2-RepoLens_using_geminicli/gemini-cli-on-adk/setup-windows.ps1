# Windows Setup Script for Gemini CLI ADK Agent

Write-Host "Setting up Gemini CLI ADK Agent on Windows..." -ForegroundColor Green

# Check if Python is installed
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10-3.12 from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "`nChecking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Cyan
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install -e .

# Install Gemini CLI
Write-Host "`nInstalling Gemini CLI..." -ForegroundColor Yellow
npm install -g @google/gemini-cli

# Check if gcloud is installed
Write-Host "`nChecking Google Cloud SDK..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud --version
    Write-Host "✓ Google Cloud SDK found" -ForegroundColor Green
    Write-Host "`nPlease authenticate with Google Cloud:" -ForegroundColor Yellow
    Write-Host "  gcloud auth login --update-adc" -ForegroundColor Cyan
    Write-Host "  gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Cyan
} catch {
    Write-Host "⚠ Google Cloud SDK not found" -ForegroundColor Yellow
    Write-Host "Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Cyan
}

Write-Host "`n✓ Setup complete!" -ForegroundColor Green
Write-Host "`nTo run the agent:" -ForegroundColor Yellow
Write-Host "  1. Activate the virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "  2. Run the agent: python -m adk web --host 0.0.0.0 --port 8080 ." -ForegroundColor Cyan
Write-Host "  3. Open browser: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""

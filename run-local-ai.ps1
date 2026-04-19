# PowerShell script to run Serinity AI API locally on Windows

$ErrorActionPreference = "Stop"

# Get the directory where this script is located
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $ProjectDir ".venv"
$Host_IP = "127.0.0.1"
$Port = 8001

Set-Location $ProjectDir

# Check if virtual environment exists
if (-not (Test-Path $VenvDir)) {
    Write-Host "Virtual environment not found at: $VenvDir" -ForegroundColor Red
    Write-Host "Create it first with:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv"
    Write-Host "  .venv\Scripts\Activate.ps1"
    Write-Host "  pip install -r requirements.txt"
    exit 1
}

# Activate the virtual environment
$ActivateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
& $ActivateScript

# Check if main.py exists
$MainPy = Join-Path $ProjectDir "app\main.py"
if (-not (Test-Path $MainPy)) {
    Write-Host "FastAPI entrypoint not found: $MainPy" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Serinity AI API on http://$($Host_IP):$Port" -ForegroundColor Green
uvicorn app.main:app --reload --host $Host_IP --port $Port

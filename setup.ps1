# PowerShell script to setup virtual environment and install requirements
# Usage: .\setup.ps1

param(
    [switch]$Force  # Force recreate virtual environment
)

# Set error action preference
$ErrorActionPreference = "Stop"

try {
    Write-Host "Checking for virtual environment..." -ForegroundColor Yellow

    # Check if we should force recreate or if .venv doesn't exist
    if ($Force -and (Test-Path ".venv")) {
        Write-Host "Force flag detected. Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force ".venv"
    }

    if (Test-Path ".venv") {
        Write-Host "Virtual environment found. Activating..." -ForegroundColor Green
        
        # Check if activation script exists
        if (Test-Path ".venv\Scripts\Activate.ps1") {
            & ".venv\Scripts\Activate.ps1"
        } else {
            Write-Error "Virtual environment exists but activation script not found"
        }
    } else {
        Write-Host "Virtual environment not found. Creating new one..." -ForegroundColor Yellow
        
        # Check if python is available
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
            Write-Error "Python is not installed or not in PATH"
        }
        
        python -m venv .venv
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to create virtual environment"
        }
        
        Write-Host "Virtual environment created successfully!" -ForegroundColor Green
        Write-Host "Activating new virtual environment..." -ForegroundColor Green
        & ".venv\Scripts\Activate.ps1"
    }

    # Upgrade pip first
    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip

    # Install requirements if file exists
    Write-Host "Checking for requirements.txt..." -ForegroundColor Yellow

    if (Test-Path "requirements.txt") {
        Write-Host "Installing requirements from requirements.txt..." -ForegroundColor Yellow
        pip install -r requirements.txt
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install requirements"
        }
        
        Write-Host "Requirements installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "No requirements.txt found. Skipping installation." -ForegroundColor Yellow
        Write-Host "You can create a requirements.txt file with your dependencies." -ForegroundColor Cyan
    }

    Write-Host "`nSetup completed successfully!" -ForegroundColor Green
    Write-Host "Virtual environment is ready and activated." -ForegroundColor Green
    Write-Host "`nTo activate manually in the future, run:" -ForegroundColor Cyan
    Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "`nTo deactivate, run:" -ForegroundColor Cyan
    Write-Host "  deactivate" -ForegroundColor White

} catch {
    Write-Host "`nError occurred: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Setup failed!" -ForegroundColor Red
    exit 1
}

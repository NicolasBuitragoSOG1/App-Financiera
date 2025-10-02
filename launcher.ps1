# Personal Finance Platform Launcher (PowerShell)
param(
    [switch]$Setup,
    [switch]$Docker,
    [switch]$Stop
)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = $ScriptDir

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Personal Finance Platform Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project Location: $ProjectRoot" -ForegroundColor Yellow
Write-Host ""

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to check if port is in use
function Test-Port($port) {
    $connection = Test-NetConnection -ComputerName localhost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
    return $connection
}

# Stop servers if requested
if ($Stop) {
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    Get-Process | Where-Object {$_.ProcessName -eq "node" -or $_.ProcessName -eq "python"} | Where-Object {$_.MainWindowTitle -like "*Finance*"} | Stop-Process -Force
    Write-Host "Servers stopped." -ForegroundColor Green
    exit
}

# Docker mode
if ($Docker) {
    Write-Host "Starting with Docker..." -ForegroundColor Yellow
    
    if (-not (Test-Command docker)) {
        Write-Host "Error: Docker is not installed or not in PATH!" -ForegroundColor Red
        exit 1
    }
    
    Set-Location $ProjectRoot
    
    if (-not (Test-Path "docker-compose.yml")) {
        Write-Host "Error: docker-compose.yml not found!" -ForegroundColor Red
        exit 1
    }
    
    # Check if OPENAI_API_KEY is set
    if (-not $env:OPENAI_API_KEY) {
        Write-Host "Warning: OPENAI_API_KEY environment variable not set." -ForegroundColor Yellow
        Write-Host "AI features will not work properly." -ForegroundColor Yellow
    }
    
    Write-Host "Starting Docker containers..." -ForegroundColor Green
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host " Docker containers started successfully!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host " Frontend:     http://localhost:3000" -ForegroundColor Cyan
        Write-Host " Backend API:  http://localhost:8000" -ForegroundColor Cyan
        Write-Host " API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Green
    }
    
    exit
}

# Verify project structure
$requiredFolders = @("backend", "frontend")
foreach ($folder in $requiredFolders) {
    if (-not (Test-Path (Join-Path $ProjectRoot $folder))) {
        Write-Host "Error: $folder folder not found!" -ForegroundColor Red
        Write-Host "Make sure this launcher is in the project root directory." -ForegroundColor Red
        exit 1
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

$pythonOk = Test-Command python
$nodeOk = Test-Command node
$npmOk = Test-Command npm

if (-not $pythonOk) {
    Write-Host "Error: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://python.org" -ForegroundColor Yellow
    exit 1
}

if (-not $nodeOk -or -not $npmOk) {
    Write-Host "Error: Node.js/npm is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Python found: $(python --version)" -ForegroundColor Green
Write-Host "✓ Node.js found: $(node --version)" -ForegroundColor Green
Write-Host "✓ npm found: $(npm --version)" -ForegroundColor Green

# Setup mode or check dependencies
if ($Setup -or -not (Test-Path (Join-Path $ProjectRoot "backend\requirements.txt"))) {
    Write-Host ""
    Write-Host "Setting up project..." -ForegroundColor Yellow
    
    # Install backend dependencies
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    Set-Location (Join-Path $ProjectRoot "backend")
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error installing Python dependencies!" -ForegroundColor Red
        exit 1
    }
    
    # Initialize database
    Write-Host "Initializing database..." -ForegroundColor Yellow
    python init_data.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error initializing database!" -ForegroundColor Red
        exit 1
    }
    
    # Install frontend dependencies
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    Set-Location (Join-Path $ProjectRoot "frontend")
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error installing Node.js dependencies!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Setup completed successfully!" -ForegroundColor Green
}

# Check if dependencies exist
$backendDeps = Test-Path (Join-Path $ProjectRoot "backend\Lib") -or (Test-Path (Join-Path $ProjectRoot "backend\venv"))
$frontendDeps = Test-Path (Join-Path $ProjectRoot "frontend\node_modules")

if (-not $backendDeps) {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    Set-Location (Join-Path $ProjectRoot "backend")
    pip install -r requirements.txt
}

if (-not $frontendDeps) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    Set-Location (Join-Path $ProjectRoot "frontend")
    npm install
}

# Check .env file
$envPath = Join-Path $ProjectRoot "backend\.env"
if (-not (Test-Path $envPath)) {
    Write-Host "Creating default .env file..." -ForegroundColor Yellow
    $envContent = @"
SECRET_KEY=your-secret-key-here-change-in-production-make-it-very-long-and-random
DATABASE_URL=sqlite:///./finance_app.db
OPENAI_API_KEY=your-openai-api-key-here
"@
    $envContent | Out-File -FilePath $envPath -Encoding UTF8
    Write-Host "⚠️  Please edit backend\.env and add your OpenAI API key!" -ForegroundColor Yellow
}

# Check if ports are available
Write-Host ""
Write-Host "Checking ports..." -ForegroundColor Yellow

if (Test-Port 8000) {
    Write-Host "Warning: Port 8000 is already in use!" -ForegroundColor Yellow
}

if (Test-Port 3000) {
    Write-Host "Warning: Port 3000 is already in use!" -ForegroundColor Yellow
}

# Start servers
Write-Host ""
Write-Host "Starting servers..." -ForegroundColor Green

# Start backend
Write-Host "Starting backend server..." -ForegroundColor Yellow
Set-Location (Join-Path $ProjectRoot "backend")
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Finance Backend Server' -ForegroundColor Green; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Wait for backend
Start-Sleep -Seconds 5

# Start frontend
Write-Host "Starting frontend server..." -ForegroundColor Yellow
Set-Location (Join-Path $ProjectRoot "frontend")
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Finance Frontend Server' -ForegroundColor Green; npm run dev"

# Wait for frontend
Start-Sleep -Seconds 3

# Success message
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Servers started successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host " Frontend:     http://localhost:3000" -ForegroundColor Cyan
Write-Host " Backend API:  http://localhost:8000" -ForegroundColor Cyan
Write-Host " API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Demo Credentials:" -ForegroundColor Yellow
Write-Host " Email:    user@test.com" -ForegroundColor White
Write-Host " Password: Test123" -ForegroundColor White
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host " .\launcher.ps1          - Start normally" -ForegroundColor White
Write-Host " .\launcher.ps1 -Setup   - Run setup first" -ForegroundColor White
Write-Host " .\launcher.ps1 -Docker  - Start with Docker" -ForegroundColor White
Write-Host " .\launcher.ps1 -Stop    - Stop all servers" -ForegroundColor White
Write-Host ""
Write-Host "Both servers are running in separate windows." -ForegroundColor Green
Write-Host "Close those windows to stop the servers." -ForegroundColor Green

@echo off
setlocal enabledelayedexpansion

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%"

echo ========================================
echo  Personal Finance Platform Launcher
echo ========================================
echo Project Location: %PROJECT_ROOT%
echo.

:: Check if we're in the correct directory
if not exist "%PROJECT_ROOT%backend" (
    echo Error: Backend folder not found!
    echo Make sure this launcher is in the project root directory.
    pause
    exit /b 1
)

if not exist "%PROJECT_ROOT%frontend" (
    echo Error: Frontend folder not found!
    echo Make sure this launcher is in the project root directory.
    pause
    exit /b 1
)

:: Check if dependencies are installed
echo Checking dependencies...

:: Check Python dependencies
if not exist "%PROJECT_ROOT%backend\venv" (
    if not exist "%PROJECT_ROOT%backend\requirements.txt" (
        echo Error: requirements.txt not found in backend folder!
        pause
        exit /b 1
    )
    echo Python dependencies not found. Installing...
    cd /d "%PROJECT_ROOT%backend"
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo Error installing Python dependencies!
        pause
        exit /b 1
    )
)

:: Check Node dependencies
if not exist "%PROJECT_ROOT%frontend\node_modules" (
    if not exist "%PROJECT_ROOT%frontend\package.json" (
        echo Error: package.json not found in frontend folder!
        pause
        exit /b 1
    )
    echo Node.js dependencies not found. Installing...
    cd /d "%PROJECT_ROOT%frontend"
    npm install
    if !errorlevel! neq 0 (
        echo Error installing Node.js dependencies!
        pause
        exit /b 1
    )
)

:: Initialize database if it doesn't exist
if not exist "%PROJECT_ROOT%backend\finance_app.db" (
    echo Initializing database...
    cd /d "%PROJECT_ROOT%backend"
    python init_data.py
    if !errorlevel! neq 0 (
        echo Error initializing database!
        pause
        exit /b 1
    )
)

:: Check if .env file exists
if not exist "%PROJECT_ROOT%backend\.env" (
    echo Warning: .env file not found in backend folder.
    echo Creating default .env file...
    cd /d "%PROJECT_ROOT%backend"
    echo SECRET_KEY=your-secret-key-here-change-in-production-make-it-very-long-and-random > .env
    echo DATABASE_URL=sqlite:///./finance_app.db >> .env
    echo OPENAI_API_KEY=your-openai-api-key-here >> .env
    echo.
    echo Please edit backend\.env and add your OpenAI API key for full functionality.
    echo.
)

echo.
echo Starting servers...
echo.

:: Start backend server
echo Starting backend server...
cd /d "%PROJECT_ROOT%backend"
start "Finance Backend Server" cmd /k "echo Backend Server Starting... && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Wait a moment for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Start frontend server
echo Starting frontend development server...
cd /d "%PROJECT_ROOT%frontend"
start "Finance Frontend Server" cmd /k "echo Frontend Server Starting... && npm run dev"

:: Wait a moment for frontend to start
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo  Servers are starting up!
echo ========================================
echo  Frontend:     http://localhost:3000
echo  Backend API:  http://localhost:8000
echo  API Docs:     http://localhost:8000/docs
echo ========================================
echo.
echo Demo Credentials:
echo  Email:    user@test.com
echo  Password: Test123
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo Press any key to exit this launcher...
pause > nul

endlocal

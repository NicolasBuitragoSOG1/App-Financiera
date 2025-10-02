@echo off
echo ========================================
echo  Personal Finance Management Platform
echo ========================================
echo.

echo Starting backend server...
cd backend
start "Backend Server" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting frontend development server...
cd ..\frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ========================================
echo  Servers are starting up!
echo ========================================
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit...
pause > nul

@echo off
echo ========================================
echo  Personal Finance Platform Setup
echo ========================================
echo.

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing backend dependencies!
    pause
    exit /b 1
)

echo.
echo Initializing database with sample data...
python init_data.py
if %errorlevel% neq 0 (
    echo Error initializing database!
    pause
    exit /b 1
)

echo.
echo Installing frontend dependencies...
cd ..\frontend
npm install
if %errorlevel% neq 0 (
    echo Error installing frontend dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Configure your OpenAI API key in backend/.env
echo 2. Run start.bat to launch the application
echo 3. Visit http://localhost:3000 to access the app
echo.
echo Demo credentials:
echo Email: user@test.com
echo Password: Test123
echo.
pause

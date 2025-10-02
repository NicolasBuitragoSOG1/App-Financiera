@echo off
:: Personal Finance Platform - Portable Launcher
:: This file can be copied anywhere and will find the project automatically

setlocal enabledelayedexpansion

:: Try to find the project directory
set "CURRENT_DIR=%~dp0"
set "PROJECT_DIR="

:: First, check if we're already in the project directory
if exist "%CURRENT_DIR%backend" if exist "%CURRENT_DIR%frontend" (
    set "PROJECT_DIR=%CURRENT_DIR%"
    goto :found
)

:: Check common locations
set "SEARCH_PATHS=%USERPROFILE%\Desktop\C# %USERPROFILE%\OneDrive\Escritorio\C# %USERPROFILE%\Documents\C# C:\Projects\C# C:\Dev\C#"

for %%P in (%SEARCH_PATHS%) do (
    if exist "%%P\backend" if exist "%%P\frontend" (
        set "PROJECT_DIR=%%P\"
        goto :found
    )
)

:: If not found, ask user
echo Finance Platform project not found automatically.
echo Please enter the full path to your project folder:
set /p "PROJECT_DIR="

if not exist "%PROJECT_DIR%\backend" (
    echo Error: Invalid project path. Backend folder not found.
    pause
    exit /b 1
)

:found
echo ========================================
echo  Personal Finance Platform
echo ========================================
echo Project found at: %PROJECT_DIR%
echo.

cd /d "%PROJECT_DIR%"

:: Check if launcher exists
if exist "launcher.bat" (
    call launcher.bat
) else (
    echo Error: launcher.bat not found in project directory.
    echo Please make sure you have the complete project files.
    pause
    exit /b 1
)

endlocal

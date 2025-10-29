@echo off
echo ====================================
echo FinanceApp - Test Runner
echo ====================================
echo.

:menu
echo Seleccione una opcion:
echo 1. Ejecutar todas las pruebas
echo 2. Ejecutar solo pruebas de backend
echo 3. Ejecutar solo pruebas de frontend
echo 4. Ejecutar pruebas con cobertura (backend)
echo 5. Ejecutar pruebas con cobertura (frontend)
echo 6. Abrir reporte de cobertura (backend)
echo 7. Abrir reporte de cobertura (frontend)
echo 8. Ejecutar pruebas de CI/CD localmente
echo 0. Salir
echo.

set /p option="Ingrese el numero de opcion: "

if "%option%"=="1" goto all_tests
if "%option%"=="2" goto backend_tests
if "%option%"=="3" goto frontend_tests
if "%option%"=="4" goto backend_coverage
if "%option%"=="5" goto frontend_coverage
if "%option%"=="6" goto open_backend_coverage
if "%option%"=="7" goto open_frontend_coverage
if "%option%"=="8" goto ci_tests
if "%option%"=="0" goto end

echo Opcion invalida
goto menu

:all_tests
echo.
echo Ejecutando pruebas de backend...
cd backend
call pytest
cd ..
echo.
echo Ejecutando pruebas de frontend...
cd frontend
call npm test
cd ..
goto menu

:backend_tests
echo.
echo Ejecutando pruebas de backend...
cd backend
call pytest
cd ..
goto menu

:frontend_tests
echo.
echo Ejecutando pruebas de frontend...
cd frontend
call npm test
cd ..
goto menu

:backend_coverage
echo.
echo Ejecutando pruebas de backend con cobertura...
cd backend
call pytest --cov=. --cov-report=html --cov-report=term
echo.
echo Reporte generado en: backend/htmlcov/index.html
cd ..
pause
goto menu

:frontend_coverage
echo.
echo Ejecutando pruebas de frontend con cobertura...
cd frontend
call npm run test:coverage
echo.
echo Reporte generado en: frontend/coverage/index.html
cd ..
pause
goto menu

:open_backend_coverage
echo.
echo Abriendo reporte de cobertura del backend...
start backend\htmlcov\index.html
goto menu

:open_frontend_coverage
echo.
echo Abriendo reporte de cobertura del frontend...
start frontend\coverage\index.html
goto menu

:ci_tests
echo.
echo Ejecutando pruebas como en CI/CD...
echo.
echo === BACKEND ===
cd backend
call pytest --cov=. --cov-report=xml --cov-report=term
cd ..
echo.
echo === FRONTEND ===
cd frontend
call npm run test:coverage
cd ..
echo.
echo Proceso completado!
pause
goto menu

:end
echo.
echo Gracias por usar el Test Runner!
pause

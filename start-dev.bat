@echo off
REM MediaCMS Windows Development Environment Startup Script
REM This script will automatically start all required services

echo ========================================
echo MediaCMS Development Environment
echo ========================================
echo.

REM Check Python virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Please run:
    echo python -m venv venv
    echo .\venv\Scripts\activate.bat
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if Redis is running
echo [CHECK] Checking Redis service...
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Redis is not running. Please start Redis first:
    echo Method 1 - WSL: wsl -e bash -c "sudo service redis-server start"
    echo Method 2 - Memurai: Start Memurai service in Windows Services
    pause
)

REM Check if PostgreSQL is running
echo [CHECK] Checking PostgreSQL service...
sc query postgresql-x64-* >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PostgreSQL may not be running
    echo Please check PostgreSQL service in Windows Services
)

echo.
echo [STARTUP] Starting all services...
echo.

REM Start first Celery Worker (short tasks) - Using solo pool for Windows compatibility
echo [STARTUP] Celery Worker (short tasks queue)...
start "Celery Short Tasks" cmd /k "venv\Scripts\activate.bat && celery -A cms worker --loglevel=info -Q short_tasks -n short@%%h --pool=solo"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start second Celery Worker (long tasks) - Using solo pool for Windows compatibility
echo [STARTUP] Celery Worker (long tasks queue)...
start "Celery Long Tasks" cmd /k "venv\Scripts\activate.bat && celery -A cms worker --loglevel=info -Q long_tasks -n long@%%h --pool=solo"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Celery Beat
echo [STARTUP] Celery Beat (task scheduler)...
start "Celery Beat" cmd /k "venv\Scripts\activate.bat && celery -A cms beat --loglevel=info"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Django backend service
echo [STARTUP] Django backend service...
start "Django Backend" cmd /k "venv\Scripts\activate.bat && python manage.py runserver localhost:8000"

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Start Vue frontend service (Client)
echo [STARTUP] Vue client frontend (user-facing)...
if exist "frontend-vue\package.json" (
    start "Vue Client Frontend" cmd /k "cd frontend-vue && npm run dev"
) else (
    echo [WARNING] Client frontend package.json not found
)

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Start Vue admin frontend
echo [STARTUP] Vue admin frontend (admin panel)...
if exist "admin-vue\package.json" (
    start "Vue Admin Frontend" cmd /k "cd admin-vue && npm run dev"
) else (
    echo [WARNING] Admin frontend package.json not found
)

echo.
echo ========================================
echo All services started successfully
echo ========================================
echo.
echo Access URLs:
echo   - Django Backend:  http://localhost:8000
echo   - Django Admin:    http://localhost:8000/admin
echo   - API Docs:        http://localhost:8000/api/v1/
echo   - Client Frontend: http://localhost:8088 (User-facing)
echo   - Admin Frontend:  http://localhost:5174 (Admin Panel)
echo.
echo Press any key to continue (keep this window open)...
pause >nul

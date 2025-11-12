@echo off
REM MediaCMS Minimal Development Environment (Without Celery)
REM For Windows - Core services only

echo ========================================
echo MediaCMS Minimal Development Mode
echo (Django + Vue only, no background tasks)
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

echo.
echo [STARTUP] Starting core services...
echo.

REM Start Django backend service
echo [STARTUP] Django backend service...
start "Django Backend" cmd /k "venv\Scripts\activate.bat && python manage.py runserver localhost:8000"

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Start Vue frontend service
echo [STARTUP] Vue frontend development server...
if exist "frontend-vue\package.json" (
    start "Vue Frontend" cmd /k "cd frontend-vue && npm run dev"
) else (
    echo [WARNING] Frontend package.json not found
)

echo.
echo ========================================
echo Core services started
echo ========================================
echo.
echo IMPORTANT: Background tasks (video encoding, etc) are DISABLED
echo For full functionality, use start-dev.bat instead
echo.
echo Access URLs:
echo   - Django Backend:  http://localhost:8000
echo   - Django Admin:    http://localhost:8000/admin
echo   - Vue Frontend:    http://localhost:8080
echo.
echo Press any key to continue (keep this window open)...
pause >nul


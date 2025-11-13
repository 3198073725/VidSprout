@echo off
chcp 936 >nul
REM MediaCMS Windows 开发环境启动脚本
REM 此脚本将自动启动所有必要的服务

echo ========================================
echo MediaCMS Windows 开发环境启动脚本
echo ========================================
echo.

REM 检查 Python 虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo [错误] 虚拟环境不存在，请先执行以下命令：
    echo python -m venv venv
    echo .\venv\Scripts\activate.bat
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM 检查 Redis 是否运行
echo [检查] 检查 Redis 服务...
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [警告] Redis 未运行，请先启动 Redis 服务
    echo 方式1 - WSL: wsl -e bash -c "sudo service redis-server start"
    echo 方式2 - Memurai: 在服务管理器中启动 Memurai 服务
    pause
)

REM 检查 PostgreSQL 是否运行
echo [检查] 检查 PostgreSQL 服务...
sc query postgresql-x64-* >nul 2>&1
if errorlevel 1 (
    echo [警告] PostgreSQL 服务未运行，请检查服务状态
    echo 请在 Windows 服务管理器中启动 PostgreSQL
)

echo.
echo [启动] 正在依次启动各服务...
echo.

REM 启动第一个 Celery Worker（短任务）
echo [启动] Celery Worker (短任务队列)...
start "Celery Short Tasks" cmd /k "venv\Scripts\activate.bat && celery -A cms worker --loglevel=info -Q short_tasks -n short@%%h --pool=solo"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

REM 启动第二个 Celery Worker（长任务）
echo [启动] Celery Worker (长任务队列)...
start "Celery Long Tasks" cmd /k "venv\Scripts\activate.bat && celery -A cms worker --loglevel=info -Q long_tasks -n long@%%h --pool=solo"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

REM 启动 Celery Beat
echo [启动] Celery Beat (定时任务调度器)...
start "Celery Beat" cmd /k "venv\Scripts\activate.bat && celery -A cms beat --loglevel=info"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

REM 启动 Django 后端服务
echo [启动] Django 后端服务...
start "Django Backend" cmd /k "venv\Scripts\activate.bat && python manage.py runserver localhost:8000"

REM 等待 3 秒
timeout /t 3 /nobreak >nul

REM 启动 Vue 客户端前端服务
echo [启动] Vue 客户端前端（用户端）...
if exist "frontend-vue\package.json" (
    start "Vue 客户端前端" cmd /k "cd frontend-vue && npm run dev"
) else (
    echo [警告] 找不到客户端前端项目的 package.json
)

REM 等待 3 秒
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 所有服务已启动完成
echo ========================================
echo.
echo 访问地址：
echo   - Django 后台:     http://localhost:8000
echo   - Django Admin:    http://localhost:8000/admin
echo   - API 文档:        http://localhost:8000/api/v1/
echo   - 客户端前端:      http://localhost:8088 （用户端）
echo.
echo 按任意键继续（保持此窗口打开）...
pause >nul


@echo off
REM MediaCMS Windows 环境检查脚本

echo ========================================
echo MediaCMS 环境检查工具
echo ========================================
echo.

echo [检查] Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python 未安装或未添加到 PATH
) else (
    python --version
    echo [√] Python 已安装
)
echo.

echo [检查] pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [X] pip 未安装
) else (
    pip --version
    echo [√] pip 已安装
)
echo.

echo [检查] Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [X] Node.js 未安装或未添加到 PATH
) else (
    node --version
    echo [√] Node.js 已安装
)
echo.

echo [检查] npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [X] npm 未安装
) else (
    npm --version
    echo [√] npm 已安装
)
echo.

echo [检查] Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [X] Git 未安装或未添加到 PATH
) else (
    git --version
    echo [√] Git 已安装
)
echo.

echo [检查] PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [X] PostgreSQL 客户端未安装或未添加到 PATH
) else (
    psql --version
    echo [√] PostgreSQL 客户端已安装
)
echo.

echo [检查] Redis...
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [X] Redis 未运行或未安装
) else (
    redis-cli ping
    echo [√] Redis 正在运行
)
echo.

echo [检查] FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [X] FFmpeg 未安装或未添加到 PATH
) else (
    ffmpeg -version | findstr "version"
    echo [√] FFmpeg 已安装
)
echo.

echo [检查] ImageMagick...
magick -version >nul 2>&1
if errorlevel 1 (
    echo [X] ImageMagick 未安装或未添加到 PATH
) else (
    magick -version | findstr "Version"
    echo [√] ImageMagick 已安装
)
echo.

echo [检查] Python 虚拟环境...
if exist "venv\Scripts\activate.bat" (
    echo [√] 虚拟环境已创建
) else (
    echo [X] 虚拟环境不存在，请运行: python -m venv venv
)
echo.

echo [检查] Python 依赖...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -c "import django" >nul 2>&1
    if errorlevel 1 (
        echo [X] Django 未安装，请运行: pip install -r requirements.txt
    ) else (
        echo [√] Python 依赖已安装
    )
    call venv\Scripts\deactivate.bat
)
echo.

echo [检查] 前端依赖...
if exist "frontend-vue\node_modules" (
    echo [√] 前端依赖已安装
) else (
    echo [X] 前端依赖未安装，请运行: cd frontend-vue ^&^& npm install
)
echo.

echo ========================================
echo 环境检查完成！
echo ========================================
echo.
pause


@echo off
REM MediaCMS Vue 前端构建脚本
REM 将 Vue 前端构建并复制到 Django static 目录

echo ========================================
echo MediaCMS Vue 前端构建脚本
echo ========================================
echo.

cd /d "%~dp0"
cd frontend-vue

echo [1/2] 正在构建 Vue 前端...
call npm run build

if errorlevel 1 (
    echo [错误] Vue 前端构建失败！
    pause
    exit /b 1
)

echo [成功] Vue 前端构建完成！
echo.

echo [2/2] 构建文件已输出到 ../static/vue/
echo.

echo [提示] 现在可以：
echo   1. 运行 Django 服务器：python manage.py runserver
echo   2. 访问 http://localhost:8000 查看 Vue 前端
echo.

echo ========================================
echo 完成！
echo ========================================
pause


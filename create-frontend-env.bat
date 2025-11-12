@echo off
REM MediaCMS 创建前端环境变量文件脚本
REM 如果 .env.development 不存在，则创建它

echo ========================================
echo MediaCMS 前端环境变量文件创建脚本
echo ========================================
echo.

cd /d "%~dp0"
cd frontend-vue

if exist ".env.development" (
    echo [信息] .env.development 文件已存在
    echo [信息] 如果需要重新创建，请先删除现有文件
    pause
    exit /b 0
)

echo [创建] 正在创建 .env.development 文件...

(
echo # MediaCMS Vue 前端开发环境配置
echo # 此文件会被 Vite 自动加载
echo.
echo # API 基础地址
echo VITE_API_BASE=http://localhost:8000/api
echo.
echo # 是否使用 CSRF（开发环境通常不需要）
echo VITE_USE_CSRF=false
echo.
echo # Token 相关配置
echo VITE_ACCESS_HEADER=Authorization
echo VITE_ACCESS_PREFIX=Bearer
echo.
echo # Token 刷新端点
echo VITE_REFRESH_ENDPOINT=http://localhost:8000/api/v1/auth/refresh
echo.
echo # 前端地址（用于生成完整 URL）
echo VITE_FRONTEND_URL=http://localhost:8080
echo.
echo # 后端地址（用于直接 API 调用）
echo VITE_BACKEND_URL=http://localhost:8000
) > .env.development

if exist ".env.development" (
    echo [成功] .env.development 文件已创建！
    echo [路径] %cd%\.env.development
) else (
    echo [错误] 文件创建失败，请手动创建
    pause
    exit /b 1
)

echo.
echo ========================================
echo 完成！
echo ========================================
pause


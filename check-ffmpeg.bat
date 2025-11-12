@echo off
REM 检查 FFmpeg 和 FFprobe 是否安装并可用

echo ========================================
echo MediaCMS FFmpeg 环境检查
echo ========================================
echo.

echo 检查 FFmpeg...
where ffmpeg >nul 2>&1
if %errorlevel% == 0 (
    echo [✓] FFmpeg 已安装
    ffmpeg -version | findstr "version"
) else (
    echo [✗] FFmpeg 未找到！
    echo     请安装 FFmpeg 并添加到 PATH
    echo     下载地址: https://www.gyan.dev/ffmpeg/builds/
)

echo.
echo 检查 FFprobe...
where ffprobe >nul 2>&1
if %errorlevel% == 0 (
    echo [✓] FFprobe 已安装
    ffprobe -version | findstr "version"
) else (
    echo [✗] FFprobe 未找到！
    echo     请安装 FFmpeg（包含 FFprobe）并添加到 PATH
)

echo.
echo ========================================
echo 提示：
echo 1. 如果 FFmpeg 未安装，请参考文档：docs/Windows_FFmpeg安装和配置指南.md
echo 2. 安装后需要重启命令行/Django 服务器才能生效
echo 3. 如果 FFmpeg 在非标准路径，可以在 cms/local_settings.py 中指定完整路径
echo ========================================
pause


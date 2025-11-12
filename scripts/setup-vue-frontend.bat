@echo off
REM MediaCMS Vue 3 前端快速安装脚本 (Windows)
REM 使用方法: scripts\setup-vue-frontend.bat

setlocal enabledelayedexpansion

echo ==========================================
echo   MediaCMS Vue 3 前端安装脚本 (Windows)
echo ==========================================
echo.

REM 检查 Node.js
echo [检查] Node.js 版本...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 Node.js，请先安装 Node.js ^>= 18
    pause
    exit /b 1
)

for /f "tokens=1 delims=." %%a in ('node -v') do set NODE_MAJOR=%%a
set NODE_MAJOR=%NODE_MAJOR:~1%
if %NODE_MAJOR% lss 18 (
    echo [错误] Node.js 版本过低，需要 ^>= 18
    pause
    exit /b 1
)

node -v
npm -v
echo.

REM 检查是否已存在目录
if exist "frontend-vue" (
    echo [警告] frontend-vue 目录已存在
    set /p confirm="是否删除并重新创建? (y/N): "
    if /i "!confirm!"=="y" (
        rmdir /s /q frontend-vue
    ) else (
        echo 安装取消
        pause
        exit /b 0
    )
)

REM 创建 Vue 项目
echo [1/5] 创建 Vue 3 + TypeScript 项目...
call npm create vite@latest frontend-vue -- --template vue-ts
echo.

cd frontend-vue

REM 安装核心依赖
echo [2/5] 安装核心依赖...
call npm install vue@^3.4.21 vue-router@^4.3.0 pinia@^2.1.7 pinia-plugin-persistedstate@^3.2.1 axios@^1.6.8
echo.

REM 安装 UI 和工具库
echo [3/5] 安装 UI 组件库和工具...
call npm install element-plus@^2.6.3 @element-plus/icons-vue@^2.3.1
call npm install @vueuse/core@^10.9.0 @vueuse/components@^10.9.0 dayjs@^1.11.10 lodash-es@^4.17.21
echo.

REM 安装功能库
echo [4/5] 安装功能库...
call npm install video.js@^8.10.0 @videojs/http-streaming@^3.12.0
call npm install @uppy/core@^3.9.3 @uppy/vue@^1.1.3 @uppy/tus@^3.5.4 @uppy/dashboard@^3.8.2 tus-js-client@^4.1.0
call npm install vue-i18n@^9.10.2 vee-validate@^4.12.6 yup@^1.4.0 clipboard@^2.0.11 qrcode@^1.5.3 viewerjs@^1.11.6 v-viewer@^3.0.11
echo.

REM 安装开发依赖
echo [5/5] 安装开发依赖...
call npm install -D @vitejs/plugin-vue@^5.0.4 vite@^5.1.6 typescript@^5.4.2 vue-tsc@^2.0.6
call npm install -D @types/node@^20.11.28 @types/video.js@^7.3.58 @types/lodash-es@^4.17.12
call npm install -D sass@^1.72.0 unplugin-auto-import@^0.17.5 unplugin-vue-components@^0.26.0
call npm install -D vite-plugin-compression@^0.5.1 rollup-plugin-visualizer@^5.12.0
call npm install -D eslint@^8.57.0 eslint-plugin-vue@^9.23.0 @typescript-eslint/eslint-plugin@^7.2.0 @typescript-eslint/parser@^7.2.0
call npm install -D prettier@^3.2.5 eslint-config-prettier@^9.1.0 eslint-plugin-prettier@^5.1.3
call npm install -D tailwindcss@^3.4.1 autoprefixer@^10.4.18 postcss@^8.4.38
echo.

REM 创建目录结构
echo [创建] 目录结构...
mkdir src\api src\assets\images src\assets\fonts src\assets\styles\themes 2>nul
mkdir src\components\layout src\components\media src\components\user src\components\common 2>nul
mkdir src\composables src\directives src\layouts src\locales src\plugins 2>nul
mkdir src\router src\stores src\types src\utils src\views 2>nul

REM 创建环境变量文件
echo [创建] 配置文件...
(
echo # 开发环境
echo NODE_ENV=development
echo VITE_API_URL=http://localhost:8000
echo VITE_WS_URL=ws://localhost:8000
echo VITE_UPLOAD_CHUNK_SIZE=5242880
echo VITE_ENABLE_MOCK=false
) > .env.development

(
echo # 生产环境
echo NODE_ENV=production
echo VITE_API_URL=https://api.mediacms.com
echo VITE_WS_URL=wss://api.mediacms.com
echo VITE_UPLOAD_CHUNK_SIZE=5242880
echo VITE_ENABLE_MOCK=false
) > .env.production

REM 创建 .prettierrc
(
echo {
echo   "semi": false,
echo   "singleQuote": true,
echo   "tabWidth": 2,
echo   "trailingComma": "es5",
echo   "printWidth": 100
echo }
) > .prettierrc

REM 初始化 Tailwind
echo [初始化] Tailwind CSS...
call npx tailwindcss init -p

REM 创建 VS Code 配置
mkdir .vscode 2>nul
(
echo {
echo   "editor.formatOnSave": true,
echo   "editor.defaultFormatter": "esbenp.prettier-vscode"
echo }
) > .vscode\settings.json

(
echo {
echo   "recommendations": [
echo     "vue.volar",
echo     "dbaeumer.vscode-eslint",
echo     "esbenp.prettier-vscode"
echo   ]
echo }
) > .vscode\extensions.json

REM 更新 scripts
call npm pkg set scripts.dev="vite"
call npm pkg set scripts.build="vue-tsc && vite build"
call npm pkg set scripts.lint="eslint . --ext .vue,.js,.ts --fix"
call npm pkg set scripts.format="prettier --write src/"

echo.
echo ==========================================
echo   [完成] 安装成功！
echo ==========================================
echo.
echo 下一步操作：
echo.
echo 1. 进入项目目录:
echo    cd frontend-vue
echo.
echo 2. 启动开发服务器:
echo    npm run dev
echo.
echo 3. 在另一个终端启动 Django:
echo    python manage.py runserver
echo.
echo 参考文档：
echo   - docs\vue3_frontend_migration_guide.md
echo   - docs\vue3_complete_dependencies.md
echo.
echo 开始构建您的 Vue 3 前端吧！
echo.
pause

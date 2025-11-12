#!/bin/bash

# MediaCMS Vue 3 前端快速安装脚本
# 使用方法: bash scripts/setup-vue-frontend.sh

set -e

echo "=========================================="
echo "  MediaCMS Vue 3 前端安装脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Node.js
echo -e "${YELLOW}检查 Node.js 版本...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: 未找到 Node.js，请先安装 Node.js >= 18${NC}"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}错误: Node.js 版本过低 (当前: $(node -v))，需要 >= 18${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js 版本: $(node -v)${NC}"
echo -e "${GREEN}✓ npm 版本: $(npm -v)${NC}"
echo ""

# 检查是否已存在 frontend-vue 目录
if [ -d "frontend-vue" ]; then
    echo -e "${YELLOW}警告: frontend-vue 目录已存在${NC}"
    read -p "是否删除并重新创建? (y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        rm -rf frontend-vue
    else
        echo "安装取消"
        exit 0
    fi
fi

# 创建 Vue 项目
echo -e "${YELLOW}1/5 创建 Vue 3 + TypeScript 项目...${NC}"
npm create vite@latest frontend-vue -- --template vue-ts
echo ""

cd frontend-vue

# 安装核心依赖
echo -e "${YELLOW}2/5 安装核心依赖...${NC}"
npm install vue@^3.4.21 vue-router@^4.3.0 pinia@^2.1.7 pinia-plugin-persistedstate@^3.2.1 axios@^1.6.8
echo ""

# 安装 UI 和工具库
echo -e "${YELLOW}3/5 安装 UI 组件库和工具...${NC}"
npm install element-plus@^2.6.3 @element-plus/icons-vue@^2.3.1
npm install @vueuse/core@^10.9.0 @vueuse/components@^10.9.0 dayjs@^1.11.10 lodash-es@^4.17.21
echo ""

# 安装功能库
echo -e "${YELLOW}4/5 安装功能库（视频播放、文件上传等）...${NC}"
npm install video.js@^8.10.0 @videojs/http-streaming@^3.12.0
npm install @uppy/core@^3.9.3 @uppy/vue@^1.1.3 @uppy/tus@^3.5.4 @uppy/dashboard@^3.8.2 tus-js-client@^4.1.0
npm install vue-i18n@^9.10.2 vee-validate@^4.12.6 yup@^1.4.0 clipboard@^2.0.11 qrcode@^1.5.3 viewerjs@^1.11.6 v-viewer@^3.0.11
echo ""

# 安装开发依赖
echo -e "${YELLOW}5/5 安装开发依赖...${NC}"
npm install -D @vitejs/plugin-vue@^5.0.4 vite@^5.1.6 typescript@^5.4.2 vue-tsc@^2.0.6
npm install -D @types/node@^20.11.28 @types/video.js@^7.3.58 @types/lodash-es@^4.17.12
npm install -D sass@^1.72.0 unplugin-auto-import@^0.17.5 unplugin-vue-components@^0.26.0
npm install -D vite-plugin-compression@^0.5.1 rollup-plugin-visualizer@^5.12.0
npm install -D eslint@^8.57.0 eslint-plugin-vue@^9.23.0 @typescript-eslint/eslint-plugin@^7.2.0 @typescript-eslint/parser@^7.2.0
npm install -D prettier@^3.2.5 eslint-config-prettier@^9.1.0 eslint-plugin-prettier@^5.1.3
npm install -D tailwindcss@^3.4.1 autoprefixer@^10.4.18 postcss@^8.4.38
echo ""

# 创建基础目录结构
echo -e "${YELLOW}创建目录结构...${NC}"
mkdir -p src/{api,assets/{images,fonts,styles},components/{layout,media,user,common},composables,directives,layouts,locales,plugins,router,stores,types,utils,views}
mkdir -p src/assets/styles/themes

# 创建环境变量文件
echo -e "${YELLOW}创建配置文件...${NC}"
cat > .env.development << 'EOF'
# 开发环境
NODE_ENV=development
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_UPLOAD_CHUNK_SIZE=5242880
VITE_ENABLE_MOCK=false
EOF

cat > .env.production << 'EOF'
# 生产环境
NODE_ENV=production
VITE_API_URL=https://api.mediacms.com
VITE_WS_URL=wss://api.mediacms.com
VITE_UPLOAD_CHUNK_SIZE=5242880
VITE_ENABLE_MOCK=false
EOF

# 创建 .eslintrc.cjs
cat > .eslintrc.cjs << 'EOF'
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: ['vue', '@typescript-eslint'],
  rules: {
    'vue/multi-word-component-names': 'off',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': 'warn',
    'vue/no-v-html': 'warn',
  },
}
EOF

# 创建 .prettierrc
cat > .prettierrc << 'EOF'
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always",
  "endOfLine": "lf"
}
EOF

# 初始化 Tailwind CSS
echo -e "${YELLOW}初始化 Tailwind CSS...${NC}"
npx tailwindcss init -p

# 创建 VS Code 配置
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
EOF

cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "vue.volar",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss"
  ]
}
EOF

# 更新 package.json scripts
echo -e "${YELLOW}更新 npm scripts...${NC}"
npm pkg set scripts.dev="vite"
npm pkg set scripts.build="vue-tsc && vite build"
npm pkg set scripts.preview="vite preview"
npm pkg set scripts.lint="eslint . --ext .vue,.js,.ts --fix"
npm pkg set scripts.format="prettier --write src/"
npm pkg set scripts.type-check="vue-tsc --noEmit"

echo ""
echo -e "${GREEN}=========================================="
echo -e "  ✓ 安装完成！"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}下一步操作：${NC}"
echo ""
echo "1. 进入项目目录:"
echo -e "   ${GREEN}cd frontend-vue${NC}"
echo ""
echo "2. 复制 Vite 配置（参考文档）:"
echo -e "   ${GREEN}# 参考 docs/vue3_complete_dependencies.md 中的 vite.config.ts${NC}"
echo ""
echo "3. 启动开发服务器:"
echo -e "   ${GREEN}npm run dev${NC}"
echo ""
echo "4. 在另一个终端启动 Django 后端:"
echo -e "   ${GREEN}cd .. && python manage.py runserver${NC}"
echo ""
echo -e "${YELLOW}参考文档：${NC}"
echo "  - docs/vue3_frontend_migration_guide.md   (迁移指南)"
echo "  - docs/vue3_complete_dependencies.md      (完整依赖清单)"
echo ""
echo -e "${GREEN}🎉 开始构建您的 Vue 3 前端吧！${NC}"

# Vue 3 前端完整依赖与配置指南

## 📦 完整依赖清单

### 1. 核心依赖 (package.json - dependencies)

```json
{
  "name": "mediacms-vue-frontend",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    // Vue 核心
    "vue": "^3.4.21",
    
    // 路由
    "vue-router": "^4.3.0",
    
    // 状态管理
    "pinia": "^2.1.7",
    "pinia-plugin-persistedstate": "^3.2.1",  // 持久化状态
    
    // HTTP 客户端
    "axios": "^1.6.8",
    
    // 视频播放器
    "video.js": "^8.10.0",
    "@videojs/http-streaming": "^3.12.0",
    "videojs-contrib-quality-levels": "^4.1.0",  // 清晰度切换
    "videojs-hls-quality-selector": "^2.0.0",    // HLS 质量选择
    
    // UI 组件库（选一个）
    "element-plus": "^2.6.3",                    // 推荐：组件丰富
    // 或 "naive-ui": "^2.38.1",                  // 备选：TypeScript 友好
    // 或 "ant-design-vue": "^4.1.2",             // 备选：Ant Design
    
    // 图标
    "@element-plus/icons-vue": "^2.3.1",         // Element Plus 图标
    // 或 "@vicons/ionicons5": "^0.12.0",        // Naive UI 图标
    
    // 工具库
    "@vueuse/core": "^10.9.0",                   // Vue 组合式工具集
    "@vueuse/components": "^10.9.0",             // 组件工具
    "dayjs": "^1.11.10",                         // 日期时间处理
    "lodash-es": "^4.17.21",                     // 工具函数
    
    // 文件上传
    "tus-js-client": "^4.1.0",                   // 断点续传
    "@uppy/core": "^3.9.3",                      // 文件上传核心
    "@uppy/vue": "^1.1.3",                       // Uppy Vue 集成
    "@uppy/tus": "^3.5.4",                       // Uppy TUS 插件
    "@uppy/dashboard": "^3.8.2",                 // 上传面板
    "@uppy/drag-drop": "^3.1.0",                 // 拖拽上传
    "@uppy/webcam": "^3.4.0",                    // 摄像头录制
    
    // Markdown 编辑器
    "@vueup/vue-quill": "^1.2.0",                // 富文本编辑器
    "markdown-it": "^14.1.0",                    // Markdown 解析
    
    // PDF 查看器
    "pdfjs-dist": "^3.11.174",
    "@react-pdf-viewer/core": "^3.12.0",         // PDF 预览
    
    // 图片查看器
    "viewerjs": "^1.11.6",
    "v-viewer": "^3.0.11",                       // Vue3 图片查看
    
    // 虚拟滚动（性能优化）
    "vue-virtual-scroller": "^2.0.0-beta.8",
    
    // 国际化
    "vue-i18n": "^9.10.2",
    
    // 表单验证
    "vee-validate": "^4.12.6",
    "yup": "^1.4.0",                             // 验证规则
    
    // 复制到剪贴板
    "clipboard": "^2.0.11",
    
    // 二维码生成
    "qrcode": "^1.5.3",
    "vue-qrcode-reader": "^5.5.1",               // 二维码扫描
    
    // 图表（可选）
    "echarts": "^5.5.0",
    "vue-echarts": "^6.7.0",
    
    // WebSocket（实时通知）
    "socket.io-client": "^4.7.4",
    
    // 响应式设计
    "tailwindcss": "^3.4.1",                     // CSS 框架
    
    // 动画
    "@vueuse/motion": "^2.1.0",                  // 动画库
    "animate.css": "^4.1.1"                      // CSS 动画
  },
  
  "devDependencies": {
    // Vite 构建工具
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.1.6",
    "vite-plugin-compression": "^0.5.1",         // Gzip 压缩
    "vite-plugin-html": "^3.2.2",                // HTML 模板
    "rollup-plugin-visualizer": "^5.12.0",       // 打包分析
    
    // TypeScript
    "typescript": "^5.4.2",
    "vue-tsc": "^2.0.6",                         // Vue TS 检查
    "@types/node": "^20.11.28",
    "@types/video.js": "^7.3.58",
    "@types/lodash-es": "^4.17.12",
    "@types/qrcode": "^1.5.5",
    
    // Sass/SCSS
    "sass": "^1.72.0",
    "sass-loader": "^14.1.1",
    
    // ESLint
    "eslint": "^8.57.0",
    "eslint-plugin-vue": "^9.23.0",
    "@typescript-eslint/eslint-plugin": "^7.2.0",
    "@typescript-eslint/parser": "^7.2.0",
    
    // Prettier
    "prettier": "^3.2.5",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-prettier": "^5.1.3",
    
    // 自动导入（性能优化）
    "unplugin-auto-import": "^0.17.5",           // 自动导入 API
    "unplugin-vue-components": "^0.26.0",        // 自动导入组件
    
    // PostCSS
    "postcss": "^8.4.38",
    "postcss-html": "^1.6.0",
    "autoprefixer": "^10.4.18"
  }
}
```

---

## 🛠️ 完整配置文件

### 1. Vite 配置 (vite.config.ts)

```typescript
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import viteCompression from 'vite-plugin-compression'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  
  return {
    plugins: [
      vue(),
      
      // 自动导入 Vue API
      AutoImport({
        imports: [
          'vue',
          'vue-router',
          'pinia',
          '@vueuse/core',
        ],
        resolvers: [ElementPlusResolver()],
        dts: 'src/auto-imports.d.ts',
      }),
      
      // 自动导入组件
      Components({
        resolvers: [ElementPlusResolver()],
        dts: 'src/components.d.ts',
      }),
      
      // Gzip 压缩
      viteCompression({
        verbose: true,
        disable: false,
        threshold: 10240,
        algorithm: 'gzip',
        ext: '.gz',
      }),
      
      // 打包分析
      visualizer({
        open: false,
        gzipSize: true,
        brotliSize: true,
      }),
    ],
    
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '~': path.resolve(__dirname, './src'),
        'components': path.resolve(__dirname, './src/components'),
        'views': path.resolve(__dirname, './src/views'),
        'stores': path.resolve(__dirname, './src/stores'),
        'api': path.resolve(__dirname, './src/api'),
        'utils': path.resolve(__dirname, './src/utils'),
        'types': path.resolve(__dirname, './src/types'),
      },
    },
    
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @use "@/assets/styles/variables.scss" as *;
            @use "@/assets/styles/mixins.scss" as *;
          `,
        },
      },
    },
    
    build: {
      outDir: '../static/vue',
      emptyOutDir: true,
      assetsDir: 'assets',
      
      // 生成 manifest.json 用于 Django 引用
      manifest: true,
      
      // 代码分割策略
      rollupOptions: {
        output: {
          manualChunks: {
            // Vue 核心库
            'vue-vendor': ['vue', 'vue-router', 'pinia'],
            
            // UI 库
            'element-plus': ['element-plus', '@element-plus/icons-vue'],
            
            // 视频播放器
            'video-player': [
              'video.js',
              '@videojs/http-streaming',
            ],
            
            // 工具库
            'utils': ['axios', 'dayjs', 'lodash-es', '@vueuse/core'],
            
            // 上传组件
            'uploader': [
              '@uppy/core',
              '@uppy/vue',
              '@uppy/tus',
              '@uppy/dashboard',
            ],
          },
          
          // 文件命名
          entryFileNames: 'js/[name].[hash].js',
          chunkFileNames: 'js/[name].[hash].js',
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.')
            const ext = info[info.length - 1]
            
            if (/\.(png|jpe?g|svg|gif|webp|ico)$/.test(assetInfo.name)) {
              return `assets/images/[name].[hash][extname]`
            } else if (/\.css$/.test(assetInfo.name)) {
              return `css/[name].[hash][extname]`
            } else if (/\.(woff2?|eot|ttf|otf)$/.test(assetInfo.name)) {
              return `assets/fonts/[name].[hash][extname]`
            }
            return `assets/[name].[hash][extname]`
          },
        },
      },
      
      // 性能优化
      chunkSizeWarningLimit: 1000,
      sourcemap: mode === 'development',
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: mode === 'production',
          drop_debugger: mode === 'production',
        },
      },
    },
    
    server: {
      port: 8088,
      host: '0.0.0.0',
      open: false,
      
      // 代理配置
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
        '/media': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
        '/accounts': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
        '/static': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
      },
      
      // 热更新
      hmr: {
        overlay: true,
      },
    },
    
    // 优化配置
    optimizeDeps: {
      include: [
        'vue',
        'vue-router',
        'pinia',
        'axios',
        'element-plus',
        '@vueuse/core',
        'dayjs',
      ],
    },
  }
})
```

---

### 2. TypeScript 配置 (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path Mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "~/*": ["src/*"],
      "components/*": ["src/components/*"],
      "views/*": ["src/views/*"],
      "stores/*": ["src/stores/*"],
      "api/*": ["src/api/*"],
      "utils/*": ["src/utils/*"],
      "types/*": ["src/types/*"]
    },

    /* Vue specific */
    "types": ["vite/client", "node", "video.js"]
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.d.ts",
    "src/**/*.tsx",
    "src/**/*.vue"
  ],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

### 3. 环境变量配置

**文件：`.env.development`**
```bash
# 开发环境
NODE_ENV=development
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_UPLOAD_CHUNK_SIZE=5242880
VITE_ENABLE_MOCK=false
```

**文件：`.env.production`**
```bash
# 生产环境
NODE_ENV=production
VITE_API_URL=https://api.mediacms.com
VITE_WS_URL=wss://api.mediacms.com
VITE_UPLOAD_CHUNK_SIZE=5242880
VITE_ENABLE_MOCK=false
```

**文件：`src/vite-env.d.ts`**
```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_WS_URL: string
  readonly VITE_UPLOAD_CHUNK_SIZE: number
  readonly VITE_ENABLE_MOCK: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Django 传递的全局变量
interface Window {
  __INITIAL_STATE__?: {
    portalName: string
    frontendHost: string
    useRoundedCorners: boolean
    loadFromCdn: boolean
    user: {
      id: number
      username: string
      email: string
      isStaff: boolean
      isSuperuser: boolean
    } | null
    csrfToken: string
  }
}
```

---

### 4. ESLint 配置 (.eslintrc.cjs)

```javascript
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
```

---

### 5. Prettier 配置 (.prettierrc)

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always",
  "endOfLine": "lf",
  "vueIndentScriptAndStyle": false
}
```

---

### 6. Tailwind CSS 配置 (tailwind.config.js)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
```

---

### 7. PostCSS 配置 (postcss.config.js)

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

---

## 📁 完整目录结构

```
frontend-vue/
├── public/
│   ├── favicon.ico
│   └── robots.txt
│
├── src/
│   ├── api/                      # API 调用层
│   │   ├── client.ts            # Axios 实例
│   │   ├── auth.ts              # 认证 API
│   │   ├── media.ts             # 媒体 API
│   │   ├── users.ts             # 用户 API
│   │   ├── playlists.ts         # 播放列表 API
│   │   ├── comments.ts          # 评论 API
│   │   └── categories.ts        # 分类 API
│   │
│   ├── assets/                   # 静态资源
│   │   ├── images/
│   │   ├── fonts/
│   │   └── styles/
│   │       ├── main.scss        # 主样式文件
│   │       ├── variables.scss   # SCSS 变量
│   │       ├── mixins.scss      # SCSS 混入
│   │       ├── reset.scss       # 样式重置
│   │       └── themes/
│   │           ├── light.scss
│   │           └── dark.scss
│   │
│   ├── components/               # 组件
│   │   ├── layout/
│   │   │   ├── DefaultLayout.vue
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   ├── Footer.vue
│   │   │   └── Breadcrumb.vue
│   │   │
│   │   ├── media/
│   │   │   ├── MediaCard.vue
│   │   │   ├── MediaGrid.vue
│   │   │   ├── MediaList.vue
│   │   │   ├── MediaPlayer.vue
│   │   │   ├── MediaUpload.vue
│   │   │   ├── MediaInfo.vue
│   │   │   ├── MediaActions.vue
│   │   │   └── VideoEditor.vue
│   │   │
│   │   ├── comments/
│   │   │   ├── CommentList.vue
│   │   │   ├── CommentItem.vue
│   │   │   └── CommentForm.vue
│   │   │
│   │   ├── user/
│   │   │   ├── UserCard.vue
│   │   │   ├── UserAvatar.vue
│   │   │   ├── UserProfile.vue
│   │   │   └── UserSettings.vue
│   │   │
│   │   └── common/
│   │       ├── Button.vue
│   │       ├── Input.vue
│   │       ├── Modal.vue
│   │       ├── Toast.vue
│   │       ├── Loading.vue
│   │       ├── Pagination.vue
│   │       ├── Dropdown.vue
│   │       ├── Tabs.vue
│   │       └── EmptyState.vue
│   │
│   ├── composables/              # 组合式函数
│   │   ├── useAuth.ts
│   │   ├── useMedia.ts
│   │   ├── useUpload.ts
│   │   ├── usePlayer.ts
│   │   ├── useComments.ts
│   │   ├── usePagination.ts
│   │   ├── useTheme.ts
│   │   └── useWebSocket.ts
│   │
│   ├── directives/               # 自定义指令
│   │   ├── lazy-load.ts
│   │   ├── permission.ts
│   │   └── infinite-scroll.ts
│   │
│   ├── layouts/                  # 布局组件
│   │   ├── DefaultLayout.vue
│   │   ├── EmptyLayout.vue
│   │   └── AdminLayout.vue
│   │
│   ├── locales/                  # 国际化
│   │   ├── index.ts
│   │   ├── en.json
│   │   ├── zh-CN.json
│   │   └── es.json
│   │
│   ├── plugins/                  # 插件
│   │   ├── element-plus.ts
│   │   ├── video-player.ts
│   │   └── i18n.ts
│   │
│   ├── router/                   # 路由
│   │   ├── index.ts
│   │   ├── routes.ts
│   │   └── guards.ts
│   │
│   ├── stores/                   # Pinia 状态管理
│   │   ├── auth.ts
│   │   ├── media.ts
│   │   ├── ui.ts
│   │   ├── user.ts
│   │   ├── playlists.ts
│   │   └── comments.ts
│   │
│   ├── types/                    # TypeScript 类型
│   │   ├── global.d.ts
│   │   ├── media.ts
│   │   ├── user.ts
│   │   ├── comment.ts
│   │   ├── playlist.ts
│   │   └── api.ts
│   │
│   ├── utils/                    # 工具函数
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   ├── storage.ts
│   │   └── request.ts
│   │
│   ├── views/                    # 页面视图
│   │   ├── Home.vue
│   │   ├── Featured.vue
│   │   ├── Latest.vue
│   │   ├── Recommended.vue
│   │   ├── MediaDetail.vue
│   │   ├── Upload.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Profile.vue
│   │   ├── Playlists.vue
│   │   ├── History.vue
│   │   ├── Liked.vue
│   │   ├── Search.vue
│   │   ├── Categories.vue
│   │   ├── NotFound.vue
│   │   └── admin/
│   │       ├── Dashboard.vue
│   │       ├── MediaManage.vue
│   │       ├── UserManage.vue
│   │       └── Settings.vue
│   │
│   ├── App.vue                   # 根组件
│   └── main.ts                   # 入口文件
│
├── .env.development              # 开发环境变量
├── .env.production               # 生产环境变量
├── .eslintrc.cjs                 # ESLint 配置
├── .prettierrc                   # Prettier 配置
├── index.html                    # HTML 入口
├── package.json                  # 依赖配置
├── postcss.config.js             # PostCSS 配置
├── tailwind.config.js            # Tailwind 配置
├── tsconfig.json                 # TypeScript 配置
├── tsconfig.node.json            # Node TypeScript 配置
└── vite.config.ts                # Vite 配置
```

---

## 🚀 安装步骤

### 1. 创建项目

```bash
cd mediacms
npm create vite@latest frontend-vue -- --template vue-ts
cd frontend-vue
```

### 2. 安装所有依赖

```bash
# 安装核心依赖
npm install vue@^3.4.21 \
  vue-router@^4.3.0 \
  pinia@^2.1.7 \
  pinia-plugin-persistedstate@^3.2.1 \
  axios@^1.6.8

# 安装视频播放器
npm install video.js@^8.10.0 \
  @videojs/http-streaming@^3.12.0 \
  videojs-contrib-quality-levels@^4.1.0 \
  videojs-hls-quality-selector@^2.0.0

# 安装 UI 库（选择 Element Plus）
npm install element-plus@^2.6.3 \
  @element-plus/icons-vue@^2.3.1

# 安装工具库
npm install @vueuse/core@^10.9.0 \
  @vueuse/components@^10.9.0 \
  dayjs@^1.11.10 \
  lodash-es@^4.17.21

# 安装文件上传
npm install tus-js-client@^4.1.0 \
  @uppy/core@^3.9.3 \
  @uppy/vue@^1.1.3 \
  @uppy/tus@^3.5.4 \
  @uppy/dashboard@^3.8.2 \
  @uppy/drag-drop@^3.1.0 \
  @uppy/webcam@^3.4.0

# 安装其他功能库
npm install vue-i18n@^9.10.2 \
  vee-validate@^4.12.6 \
  yup@^1.4.0 \
  clipboard@^2.0.11 \
  qrcode@^1.5.3 \
  viewerjs@^1.11.6 \
  v-viewer@^3.0.11 \
  socket.io-client@^4.7.4 \
  @vueuse/motion@^2.1.0 \
  animate.css@^4.1.1

# 安装开发依赖
npm install -D @vitejs/plugin-vue@^5.0.4 \
  vite@^5.1.6 \
  typescript@^5.4.2 \
  vue-tsc@^2.0.6 \
  @types/node@^20.11.28 \
  @types/video.js@^7.3.58 \
  @types/lodash-es@^4.17.12 \
  sass@^1.72.0 \
  unplugin-auto-import@^0.17.5 \
  unplugin-vue-components@^0.26.0 \
  vite-plugin-compression@^0.5.1 \
  rollup-plugin-visualizer@^5.12.0 \
  eslint@^8.57.0 \
  eslint-plugin-vue@^9.23.0 \
  @typescript-eslint/eslint-plugin@^7.2.0 \
  @typescript-eslint/parser@^7.2.0 \
  prettier@^3.2.5 \
  tailwindcss@^3.4.1 \
  autoprefixer@^10.4.18 \
  postcss@^8.4.38
```

### 3. 初始化配置文件

```bash
# 创建 Tailwind CSS 配置
npx tailwindcss init -p

# 创建 TypeScript 配置（已有则跳过）
# tsconfig.json 已由 Vite 创建

# 创建环境变量文件
touch .env.development .env.production

# 创建 ESLint 配置
touch .eslintrc.cjs

# 创建 Prettier 配置
touch .prettierrc
```

---

## 🎬 功能实现清单

### 核心功能

| 功能 | 依赖包 | 配置 |
|------|--------|------|
| **路由** | vue-router | `router/index.ts` |
| **状态管理** | pinia + persistedstate | `stores/*.ts` |
| **HTTP 请求** | axios | `api/client.ts` |
| **视频播放** | video.js + HLS | `composables/usePlayer.ts` |
| **文件上传** | @uppy/* + tus-js-client | `composables/useUpload.ts` |
| **UI 组件** | element-plus | 自动导入 |
| **国际化** | vue-i18n | `locales/index.ts` |
| **表单验证** | vee-validate + yup | 组件内使用 |
| **虚拟滚动** | vue-virtual-scroller | 长列表优化 |

### 高级功能

| 功能 | 依赖包 | 说明 |
|------|--------|------|
| **断点续传** | tus-js-client | 大文件上传 |
| **PDF 预览** | pdfjs-dist | PDF 文件查看 |
| **图片预览** | viewerjs + v-viewer | 图片放大查看 |
| **二维码** | qrcode | 分享链接生成 |
| **WebSocket** | socket.io-client | 实时通知 |
| **剪贴板** | clipboard | 复制分享链接 |
| **动画** | @vueuse/motion + animate.css | 页面过渡动画 |

---

## 🔧 开发工具配置

### VS Code 扩展推荐 (.vscode/extensions.json)

```json
{
  "recommendations": [
    "vue.volar",
    "vue.vscode-typescript-vue-plugin",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "lokalise.i18n-ally"
  ]
}
```

### VS Code 设置 (.vscode/settings.json)

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

---

## 📝 npm scripts (package.json)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore",
    "format": "prettier --write src/",
    "type-check": "vue-tsc --noEmit"
  }
}
```

---

## ✅ 完整安装验证清单

```bash
# 1. 检查 Node.js 版本（需要 >= 18）
node -v

# 2. 检查 npm 版本
npm -v

# 3. 安装依赖
npm install

# 4. 类型检查
npm run type-check

# 5. 代码格式化
npm run format

# 6. Lint 检查
npm run lint

# 7. 开发模式运行
npm run dev

# 8. 生产构建
npm run build
```

---

完成！🎉 现在您拥有一个功能完整的 Vue 3 前端配置。

# MediaCMS Vue 3 前端迁移指南

## 📋 目标
用 Vue 3 完全替换现有的 React 前端，保持后端 Django 代码不变，利用现有的 REST API。

---

## 🎯 核心策略

### ✅ **保持不变的部分**
- ✅ Django 后端完全不动
- ✅ 现有的 REST API 继续使用
- ✅ Django 模板仅保留单个入口文件
- ✅ Session 认证机制保持不变（django-allauth）
- ✅ 数据库、Celery、Redis 等基础设施不变

### 🔄 **需要替换的部分**
- 🔄 `frontend/` 目录下的 React 代码 → Vue 3
- 🔄 Django 模板中的 React 挂载点 → Vue 挂载点
- 🔄 前端路由从 React Router → Vue Router
- 🔄 状态管理从 Flux → Pinia

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    用户浏览器                                  │
└─────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────┐
│                 Django（后端 + 模板入口）                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  templates/root.html (唯一入口)                       │   │
│  │  <div id="app"></div>  ← Vue 3 挂载点                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Django REST API（已有，不修改）                       │   │
│  │  /api/v1/media/, /api/v1/users/, etc.               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Django Session Auth（已有，不修改）                   │   │
│  │  /accounts/login/, /accounts/logout/, etc.          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ⬇ 静态资源
┌─────────────────────────────────────────────────────────────┐
│              Vue 3 SPA（替换 React）                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  frontend-vue/                                        │   │
│  │  ├── src/                                             │   │
│  │  │   ├── App.vue                                      │   │
│  │  │   ├── router/        # Vue Router                  │   │
│  │  │   ├── stores/        # Pinia 状态管理              │   │
│  │  │   ├── api/           # API 调用                    │   │
│  │  │   ├── components/    # Vue 组件                    │   │
│  │  │   └── views/         # 页面视图                    │   │
│  │  └── dist/ → static/    # 编译输出                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 项目结构

### 新建 Vue 3 项目

```
mediacms/
├── frontend-vue/              # 新建：Vue 3 项目
│   ├── public/
│   │   └── index.html        # Vue 入口（不使用，改用 Django 模板）
│   ├── src/
│   │   ├── App.vue           # 根组件
│   │   ├── main.ts           # 入口文件
│   │   ├── router/
│   │   │   └── index.ts      # 路由配置
│   │   ├── stores/
│   │   │   ├── auth.ts       # 用户认证状态
│   │   │   ├── media.ts      # 媒体数据
│   │   │   └── ui.ts         # UI 状态
│   │   ├── api/
│   │   │   ├── client.ts     # Axios 客户端
│   │   │   ├── auth.ts       # 认证 API
│   │   │   ├── media.ts      # 媒体 API
│   │   │   └── users.ts      # 用户 API
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.vue
│   │   │   │   ├── Sidebar.vue
│   │   │   │   └── Footer.vue
│   │   │   ├── media/
│   │   │   │   ├── MediaCard.vue
│   │   │   │   ├── MediaPlayer.vue
│   │   │   │   ├── MediaUpload.vue
│   │   │   │   └── MediaList.vue
│   │   │   └── common/
│   │   │       ├── Button.vue
│   │   │       ├── Input.vue
│   │   │       └── Modal.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── MediaDetail.vue
│   │   │   ├── Upload.vue
│   │   │   ├── Profile.vue
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── composables/      # 组合式 API
│   │   │   ├── useAuth.ts
│   │   │   ├── useMedia.ts
│   │   │   └── useUpload.ts
│   │   ├── types/
│   │   │   ├── media.ts
│   │   │   └── user.ts
│   │   └── utils/
│   │       ├── constants.ts
│   │       └── helpers.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── frontend/                  # 原有 React 项目（可保留备份）
├── templates/
│   ├── root.html             # 修改：Vue 挂载点
│   └── ...                   # 其他 Django 模板保持不变
└── static/                   # Vue 编译输出到这里
    └── vue/
        ├── js/
        ├── css/
        └── assets/
```

---

## 🚀 实施步骤

### **第 1 步：创建 Vue 3 项目**

> 📖 **完整依赖清单**：请查看 [`vue3_complete_dependencies.md`](./vue3_complete_dependencies.md) 获取所有依赖、配置和目录结构的详细说明。

```bash
cd mediacms

# 创建 Vue 3 + TypeScript + Vite 项目
npm create vite@latest frontend-vue -- --template vue-ts

cd frontend-vue

# 安装核心依赖（完整列表见 vue3_complete_dependencies.md）
npm install

# 基础依赖
npm install vue-router@4 pinia pinia-plugin-persistedstate axios

# Vue 工具库
npm install @vueuse/core @vueuse/components dayjs lodash-es

# 视频播放器
npm install video.js@^8.10.0 @videojs/http-streaming videojs-contrib-quality-levels

# UI 组件库（推荐 Element Plus）
npm install element-plus @element-plus/icons-vue

# 文件上传（断点续传）
npm install @uppy/core @uppy/vue @uppy/tus @uppy/dashboard tus-js-client

# 其他功能库
npm install vue-i18n vee-validate yup clipboard qrcode viewerjs v-viewer

# 开发依赖
npm install -D @vitejs/plugin-vue vite typescript vue-tsc sass \
  unplugin-auto-import unplugin-vue-components \
  vite-plugin-compression eslint prettier tailwindcss

# 更多依赖详见完整文档
```

---

### **第 2 步：配置 Vite 构建**

**文件：`frontend-vue/vite.config.ts`**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  
  // 重要：构建配置
  build: {
    outDir: '../static/vue',  // 输出到 Django static 目录
    emptyOutDir: true,
    
    rollupOptions: {
      output: {
        // 生成稳定的文件名，便于 Django 引用
        entryFileNames: 'js/[name].[hash].js',
        chunkFileNames: 'js/[name].[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          const ext = info[info.length - 1];
          if (/\.(png|jpe?g|svg|gif|webp|ico)$/.test(assetInfo.name)) {
            return `assets/images/[name].[hash][extname]`;
          } else if (/\.css$/.test(assetInfo.name)) {
            return `css/[name].[hash][extname]`;
          }
          return `assets/[name].[hash][extname]`;
        },
      },
    },
    
    // 生成 manifest.json，用于 Django 引用
    manifest: true,
  },
  
  server: {
    port: 8088,
    proxy: {
      // 开发时代理到 Django 后端
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/accounts': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

---

### **第 3 步：修改 Django 模板入口**

**文件：`templates/root.html`**

```django
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{% block headtitle %}{{PORTAL_NAME}}{% endblock headtitle %}</title>
    
    {% include "common/head-meta.html" %}
    
    {% block headermeta %}
    <meta property="og:title" content="{{PORTAL_NAME}}">
    <meta property="og:type" content="website">
    {% endblock headermeta %}
    
    {# Vue 3 CSS - 由 Vite 生成 #}
    {% if DEBUG %}
        {# 开发模式：使用 Vite 开发服务器 #}
        <script type="module" src="http://localhost:8088/@vite/client"></script>
    {% else %}
        {# 生产模式：使用编译后的文件 #}
        <link rel="stylesheet" href="{% static 'vue/css/index.css' %}">
    {% endif %}
    
    {# 传递 Django 上下文到 Vue #}
    <script>
        window.__INITIAL_STATE__ = {
            portalName: "{{ PORTAL_NAME }}",
            frontendHost: "{{ FRONTEND_HOST }}",
            useRoundedCorners: {{ USE_ROUNDED_CORNERS|yesno:"true,false" }},
            loadFromCdn: {{ LOAD_FROM_CDN|yesno:"true,false" }},
            user: {% if user.is_authenticated %}{
                id: {{ user.id }},
                username: "{{ user.username }}",
                email: "{{ user.email }}",
                isStaff: {{ user.is_staff|yesno:"true,false" }},
                isSuperuser: {{ user.is_superuser|yesno:"true,false" }},
            }{% else %}null{% endif %},
            csrfToken: "{{ csrf_token }}",
        };
    </script>
</head>
<body>
    {# Vue 3 挂载点 #}
    <div id="app"></div>
    
    {# Django Messages（可选保留） #}
    {% include "messages.html" %}
    
    {# Vue 3 JS #}
    {% if DEBUG %}
        {# 开发模式 #}
        <script type="module" src="http://localhost:8088/src/main.ts"></script>
    {% else %}
        {# 生产模式 #}
        <script type="module" src="{% static 'vue/js/index.js' %}"></script>
    {% endif %}
</body>
</html>
```

---

### **第 4 步：Vue 3 入口文件**

**文件：`frontend-vue/src/main.ts`**

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 样式
import './assets/styles/main.scss'

// 创建 Vue 应用
const app = createApp(App)

// 使用 Pinia 状态管理
const pinia = createPinia()
app.use(pinia)

// 使用路由
app.use(router)

// 全局配置
app.config.globalProperties.$portalName = window.__INITIAL_STATE__?.portalName || 'MediaCMS'

// 挂载应用
app.mount('#app')
```

---

### **第 5 步：根组件**

**文件：`frontend-vue/src/App.vue`**

```vue
<template>
  <div id="mediacms-app" :class="{ 'dark-theme': isDark }">
    <!-- 全局加载指示器 -->
    <div v-if="isLoading" class="global-loading">
      <div class="spinner"></div>
    </div>

    <!-- 路由视图 -->
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'

const authStore = useAuthStore()
const uiStore = useUIStore()

const isLoading = computed(() => uiStore.isLoading)
const isDark = computed(() => uiStore.theme === 'dark')

onMounted(() => {
  // 初始化用户状态（从 Django 传递的数据）
  if (window.__INITIAL_STATE__?.user) {
    authStore.setUser(window.__INITIAL_STATE__.user)
  }
})
</script>

<style lang="scss">
// 全局样式
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#mediacms-app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 全局加载指示器
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  
  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
```

---

### **第 6 步：路由配置**

**文件：`frontend-vue/src/router/index.ts`**

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 布局组件
import DefaultLayout from '@/components/layout/DefaultLayout.vue'

// 页面组件
import Home from '@/views/Home.vue'
import MediaDetail from '@/views/MediaDetail.vue'
import Upload from '@/views/Upload.vue'
import Profile from '@/views/Profile.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: Home,
        meta: { title: 'Home' },
      },
      {
        path: '/featured',
        name: 'featured',
        component: () => import('@/views/Featured.vue'),
        meta: { title: 'Featured Media' },
      },
      {
        path: '/latest',
        name: 'latest',
        component: () => import('@/views/Latest.vue'),
        meta: { title: 'Latest Media' },
      },
      {
        path: '/recommended',
        name: 'recommended',
        component: () => import('@/views/Recommended.vue'),
        meta: { title: 'Recommended' },
      },
      {
        path: '/view/:friendlyToken',
        name: 'media-detail',
        component: MediaDetail,
        meta: { title: 'Media Detail' },
      },
      {
        path: '/upload',
        name: 'upload',
        component: Upload,
        meta: { 
          title: 'Upload Media',
          requiresAuth: true,  // 需要登录
        },
      },
      {
        path: '/user/:username',
        name: 'user-profile',
        component: Profile,
        meta: { title: 'User Profile' },
      },
      {
        path: '/playlists',
        name: 'playlists',
        component: () => import('@/views/Playlists.vue'),
        meta: { 
          title: 'My Playlists',
          requiresAuth: true,
        },
      },
      {
        path: '/history',
        name: 'history',
        component: () => import('@/views/History.vue'),
        meta: { 
          title: 'Watch History',
          requiresAuth: true,
        },
      },
      {
        path: '/liked',
        name: 'liked',
        component: () => import('@/views/Liked.vue'),
        meta: { 
          title: 'Liked Media',
          requiresAuth: true,
        },
      },
    ],
  },
  {
    // 登录页面（无布局）
    path: '/login',
    name: 'login',
    component: Login,
    meta: { title: 'Login', guest: true },
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { title: 'Register', guest: true },
  },
  {
    // 404 页面
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory('/'),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 更新页面标题
  document.title = to.meta.title 
    ? `${to.meta.title} - ${window.__INITIAL_STATE__?.portalName || 'MediaCMS'}`
    : window.__INITIAL_STATE__?.portalName || 'MediaCMS'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  }
  // 已登录用户访问登录/注册页，重定向到首页
  else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'home' })
  }
  else {
    next()
  }
})

export default router
```

---

### **第 7 步：Pinia 状态管理**

**文件：`frontend-vue/src/stores/auth.ts`**

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const csrfToken = ref<string>(window.__INITIAL_STATE__?.csrfToken || '')

  // 计算属性
  const isAuthenticated = computed(() => user.value !== null)
  const isStaff = computed(() => user.value?.isStaff || false)
  const isSuperuser = computed(() => user.value?.isSuperuser || false)

  // 方法
  function setUser(userData: User) {
    user.value = userData
  }

  function clearUser() {
    user.value = null
  }

  async function logout() {
    try {
      // 调用 Django logout（使用 Django 的 Session 认证）
      await fetch('/accounts/logout/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken.value,
        },
      })
      clearUser()
      window.location.href = '/login'  // 重定向到登录页
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  return {
    user,
    csrfToken,
    isAuthenticated,
    isStaff,
    isSuperuser,
    setUser,
    clearUser,
    logout,
  }
})
```

**文件：`frontend-vue/src/stores/media.ts`**

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Media } from '@/types/media'

export const useMediaStore = defineStore('media', () => {
  const mediaList = ref<Media[]>([])
  const currentMedia = ref<Media | null>(null)
  const isLoading = ref(false)

  function setMediaList(list: Media[]) {
    mediaList.value = list
  }

  function setCurrentMedia(media: Media) {
    currentMedia.value = media
  }

  return {
    mediaList,
    currentMedia,
    isLoading,
    setMediaList,
    setCurrentMedia,
  }
})
```

**文件：`frontend-vue/src/stores/ui.ts`**

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const isLoading = ref(false)
  const theme = ref<'light' | 'dark'>('light')
  const sidebarOpen = ref(false)

  function setLoading(loading: boolean) {
    isLoading.value = loading
  }

  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('theme', theme.value)
  }

  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  // 初始化主题
  const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
  if (savedTheme) {
    theme.value = savedTheme
  }

  return {
    isLoading,
    theme,
    sidebarOpen,
    setLoading,
    toggleTheme,
    toggleSidebar,
  }
})
```

---

### **第 8 步：API 客户端**

**文件：`frontend-vue/src/api/client.ts`**

```typescript
import axios from 'axios'
import type { AxiosInstance } from 'axios'
import { useAuthStore } from '@/stores/auth'

const apiClient: AxiosInstance = axios.create({
  baseURL: '/api/v1',  // Django API 基础路径
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // 重要：携带 Session Cookie
})

// 请求拦截器：添加 CSRF Token
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    
    // Django CSRF 保护
    if (config.method !== 'get') {
      config.headers['X-CSRFToken'] = authStore.csrfToken
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 未认证，跳转登录
      window.location.href = '/login'
    } else if (error.response?.status === 403) {
      // 无权限
      console.error('Permission denied')
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

---

### **第 9 步：媒体 API**

**文件：`frontend-vue/src/api/media.ts`**

```typescript
import apiClient from './client'
import type { Media, MediaListParams, MediaListResponse } from '@/types/media'

export const mediaApi = {
  // 获取媒体列表
  async getMediaList(params: MediaListParams = {}): Promise<MediaListResponse> {
    const { data } = await apiClient.get('/media/', { params })
    return data
  },

  // 获取媒体详情
  async getMediaDetail(friendlyToken: string): Promise<Media> {
    const { data } = await apiClient.get(`/media/${friendlyToken}/`)
    return data
  },

  // 上传媒体
  async uploadMedia(
    file: File,
    metadata: {
      title?: string
      description?: string
      category?: string
    },
    onProgress?: (percent: number) => void
  ): Promise<Media> {
    const formData = new FormData()
    formData.append('media_file', file)
    
    if (metadata.title) formData.append('title', metadata.title)
    if (metadata.description) formData.append('description', metadata.description)
    if (metadata.category) formData.append('category', metadata.category)

    const { data } = await apiClient.post('/media/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percent = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percent)
        }
      },
    })

    return data
  },

  // 点赞媒体
  async likeMedia(friendlyToken: string): Promise<void> {
    await apiClient.post(`/media/${friendlyToken}/like/`)
  },

  // 取消点赞
  async unlikeMedia(friendlyToken: string): Promise<void> {
    await apiClient.post(`/media/${friendlyToken}/dislike/`)
  },

  // 删除媒体
  async deleteMedia(friendlyToken: string): Promise<void> {
    await apiClient.delete(`/media/${friendlyToken}/`)
  },

  // 编辑媒体
  async updateMedia(
    friendlyToken: string,
    data: Partial<Media>
  ): Promise<Media> {
    const response = await apiClient.patch(`/media/${friendlyToken}/`, data)
    return response.data
  },
}

export default mediaApi
```

---

### **第 10 步：类型定义**

**文件：`frontend-vue/src/types/media.ts`**

```typescript
export interface Media {
  friendly_token: string
  title: string
  description: string
  thumbnail_url: string
  poster_url?: string
  preview_url?: string
  duration: number
  views: number
  likes: number
  dislikes: number
  media_type: 'video' | 'audio' | 'image' | 'pdf'
  state: 'public' | 'private' | 'unlisted'
  encoding_status: string
  user: string
  author_name: string
  author_profile: string
  author_thumbnail: string
  add_date: string
  edit_date?: string
  url: string
  api_url: string
  hls_info?: any
  encodings_info?: any[]
  categories_info?: any[]
  tags_info?: any[]
  subtitles_info?: any[]
}

export interface MediaListParams {
  page?: number
  author?: string
  show?: 'recommended' | 'featured' | 'latest'
  category?: string
  tag?: string
  search?: string
}

export interface MediaListResponse {
  count: number
  next: string | null
  previous: string | null
  results: Media[]
}
```

**文件：`frontend-vue/src/types/user.ts`**

```typescript
export interface User {
  id: number
  username: string
  email: string
  name?: string
  description?: string
  thumbnail?: string
  isStaff: boolean
  isSuperuser: boolean
}
```

---

### **第 11 步：核心组件示例**

**文件：`frontend-vue/src/components/layout/DefaultLayout.vue`**

```vue
<template>
  <div class="default-layout">
    <Header />
    <Sidebar />
    
    <main class="page-main">
      <div class="page-main-inner">
        <router-view />
      </div>
    </main>
    
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'
import Footer from './Footer.vue'
</script>

<style scoped lang="scss">
.default-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page-main {
  flex: 1;
  padding: 20px;
  margin-left: 250px;  // 侧边栏宽度
  
  @media (max-width: 768px) {
    margin-left: 0;
  }
}
</style>
```

**文件：`frontend-vue/src/components/media/MediaCard.vue`**

```vue
<template>
  <div class="media-card" @click="goToDetail">
    <div class="media-thumbnail">
      <img :src="media.thumbnail_url" :alt="media.title" />
      
      <div v-if="media.duration" class="duration">
        {{ formatDuration(media.duration) }}
      </div>
      
      <div v-if="media.encoding_status === 'running'" class="encoding-badge">
        Encoding...
      </div>
    </div>
    
    <div class="media-info">
      <h3 class="media-title">{{ media.title }}</h3>
      
      <div class="media-meta">
        <span class="author">{{ media.author_name }}</span>
        <span class="views">{{ media.views }} views</span>
        <span class="date">{{ formatDate(media.add_date) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Media } from '@/types/media'

interface Props {
  media: Media
}

const props = defineProps<Props>()
const router = useRouter()

function goToDetail() {
  router.push({
    name: 'media-detail',
    params: { friendlyToken: props.media.friendly_token },
  })
}

function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }
  return `${m}:${s.toString().padStart(2, '0')}`
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  if (days < 30) return `${Math.floor(days / 7)} weeks ago`
  if (days < 365) return `${Math.floor(days / 30)} months ago`
  return `${Math.floor(days / 365)} years ago`
}
</script>

<style scoped lang="scss">
.media-card {
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-4px);
  }
}

.media-thumbnail {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;  // 16:9 比例
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  
  img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .duration {
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 12px;
  }
  
  .encoding-badge {
    position: absolute;
    top: 8px;
    left: 8px;
    background: #ff9800;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
  }
}

.media-info {
  padding: 12px 0;
  
  .media-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  
  .media-meta {
    font-size: 14px;
    color: #666;
    display: flex;
    gap: 12px;
    
    span {
      &:not(:last-child)::after {
        content: '•';
        margin-left: 12px;
      }
    }
  }
}
</style>
```

---

### **第 12 步：视频播放器组件**

**文件：`frontend-vue/src/components/media/MediaPlayer.vue`**

```vue
<template>
  <div class="media-player">
    <video
      ref="videoRef"
      class="video-js vjs-default-skin"
      controls
      preload="auto"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import videojs from 'video.js'
import type Player from 'video.js/dist/types/player'
import 'video.js/dist/video-js.css'

interface Props {
  src: string
  poster?: string
  type?: string
}

const props = defineProps<Props>()

const videoRef = ref<HTMLVideoElement>()
let player: Player | null = null

onMounted(() => {
  if (videoRef.value) {
    player = videojs(videoRef.value, {
      controls: true,
      autoplay: false,
      preload: 'auto',
      poster: props.poster,
      fluid: true,
      responsive: true,
      sources: [
        {
          src: props.src,
          type: props.type || 'application/x-mpegURL',  // HLS
        },
      ],
    })
  }
})

onUnmounted(() => {
  if (player) {
    player.dispose()
  }
})

watch(() => props.src, (newSrc) => {
  if (player) {
    player.src({ src: newSrc, type: props.type || 'application/x-mpegURL' })
  }
})
</script>

<style scoped lang="scss">
.media-player {
  width: 100%;
  
  .video-js {
    width: 100%;
    height: auto;
  }
}
</style>
```

---

### **第 13 步：页面示例**

**文件：`frontend-vue/src/views/Home.vue`**

```vue
<template>
  <div class="home-page">
    <h1>{{ portalName }}</h1>
    
    <!-- 加载中 -->
    <div v-if="loading" class="loading">
      <p>Loading media...</p>
    </div>
    
    <!-- 媒体网格 -->
    <div v-else class="media-grid">
      <MediaCard
        v-for="media in mediaList"
        :key="media.friendly_token"
        :media="media"
      />
    </div>
    
    <!-- 分页 -->
    <div v-if="hasMore" class="load-more">
      <button @click="loadMore">Load More</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMediaStore } from '@/stores/media'
import { mediaApi } from '@/api/media'
import MediaCard from '@/components/media/MediaCard.vue'
import type { Media } from '@/types/media'

const mediaStore = useMediaStore()

const mediaList = ref<Media[]>([])
const loading = ref(false)
const currentPage = ref(1)
const hasMore = ref(true)

const portalName = computed(() => window.__INITIAL_STATE__?.portalName || 'MediaCMS')

async function loadMedia() {
  loading.value = true
  try {
    const response = await mediaApi.getMediaList({ page: currentPage.value })
    mediaList.value.push(...response.results)
    hasMore.value = !!response.next
  } catch (error) {
    console.error('Failed to load media:', error)
  } finally {
    loading.value = false
  }
}

function loadMore() {
  currentPage.value++
  loadMedia()
}

onMounted(() => {
  loadMedia()
})
</script>

<style scoped lang="scss">
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  
  h1 {
    font-size: 32px;
    margin-bottom: 30px;
  }
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.loading {
  text-align: center;
  padding: 40px;
}

.load-more {
  text-align: center;
  
  button {
    padding: 12px 32px;
    font-size: 16px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
      background: #2980b9;
    }
  }
}
</style>
```

---

## 🔧 构建与部署

### **开发模式**

```bash
# 启动 Django 后端
cd mediacms
python manage.py runserver

# 新终端：启动 Vue 前端
cd frontend-vue
npm run dev

# 访问 http://localhost:8088
```

### **生产构建**

```bash
# 构建 Vue 前端
cd frontend-vue
npm run build

# 输出到 ../static/vue/

# Django collectstatic（如需要）
cd ..
python manage.py collectstatic --noinput
```

### **更新 Makefile**

```makefile
# 在 Makefile 中添加
build-vue-frontend:
	cd frontend-vue && npm install && npm run build
	@echo "Vue frontend built successfully"

dev-vue:
	cd frontend-vue && npm run dev
```

---

## ✅ 迁移检查清单

### 准备阶段
- [ ] 创建 Vue 3 项目
- [ ] 安装依赖
- [ ] 配置 Vite 构建
- [ ] 修改 Django 模板入口

### 核心功能
- [ ] 实现路由系统
- [ ] 实现状态管理
- [ ] 实现 API 客户端
- [ ] 实现媒体列表
- [ ] 实现媒体详情
- [ ] 实现视频播放器
- [ ] 实现文件上传
- [ ] 实现用户认证（利用 Django Session）

### 样式与 UI
- [ ] 实现布局组件
- [ ] 实现响应式设计
- [ ] 实现深色主题
- [ ] 实现加载状态

### 测试与优化
- [ ] 功能测试
- [ ] 性能优化
- [ ] 代码分割
- [ ] 浏览器兼容性

---

## 🎯 关键优势

✅ **后端零改动**：完全使用现有 Django API  
✅ **认证无缝对接**：利用 Django Session，无需 JWT  
✅ **渐进式迁移**：可以逐页替换，新旧系统并存  
✅ **开发体验更好**：Vite 热更新，TypeScript 支持  
✅ **性能更优**：Vue 3 Composition API + Tree-shaking  

---

## 📚 参考资源

- [Vue 3 官方文档](https://vuejs.org/)
- [Vite 官方文档](https://vitejs.dev/)
- [Pinia 状态管理](https://pinia.vuejs.org/)
- [Video.js 文档](https://videojs.com/)

---

完成！🎉

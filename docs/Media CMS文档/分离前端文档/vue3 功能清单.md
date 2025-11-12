# Vue 3 前端功能实现完整清单

## 📋 功能对照表

以下列出了 MediaCMS 现有的所有功能，以及 Vue 3 前端需要实现的对应依赖和配置。

---

## 🎯 核心功能

### 1. 用户认证与授权

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **登录/登出** | Django Session | Axios + Cookie | `axios` | `api/auth.ts` |
| **注册** | django-allauth | Form + Validation | `vee-validate`, `yup` | `views/Register.vue` |
| **CSRF 保护** | Django CSRF Token | Axios 拦截器 | `axios` | `api/client.ts` |
| **权限管理** | Django Permissions | Pinia Store | `pinia` | `stores/auth.ts` |
| **RBAC** | Django RBAC | Route Guards | `vue-router` | `router/guards.ts` |
| **SAML 登录** | python3-saml | 重定向到 Django | 无需前端依赖 | - |

**实现要点：**
```typescript
// api/client.ts - CSRF Token
apiClient.interceptors.request.use((config) => {
  if (config.method !== 'get') {
    config.headers['X-CSRFToken'] = window.__INITIAL_STATE__.csrfToken
  }
  return config
})

// router/guards.ts - 路由权限
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})
```

---

### 2. 媒体播放

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **视频播放** | Video.js | Video.js Vue 组件 | `video.js@^8.10.0` | `components/media/MediaPlayer.vue` |
| **HLS 流媒体** | video.js HLS | HTTP Streaming Plugin | `@videojs/http-streaming@^3.12.0` | 同上 |
| **多清晰度切换** | - | Quality Selector | `videojs-contrib-quality-levels`, `videojs-hls-quality-selector` | 同上 |
| **音频播放** | Video.js | 同上 | 同上 | `components/media/AudioPlayer.vue` |
| **PDF 预览** | PDF.js | PDF.js Viewer | `pdfjs-dist@^3.11.174` | `components/media/PDFViewer.vue` |
| **图片预览** | - | Viewer.js | `viewerjs@^1.11.6`, `v-viewer@^3.0.11` | `components/media/ImageViewer.vue` |
| **播放速度控制** | Video.js | 内置 | - | MediaPlayer 配置 |
| **全屏播放** | Video.js | 内置 | - | - |
| **字幕支持** | Video.js | 内置 | - | MediaPlayer 配置 |

**实现要点：**
```vue
<!-- components/media/MediaPlayer.vue -->
<script setup lang="ts">
import videojs from 'video.js'
import 'videojs-contrib-quality-levels'
import 'videojs-hls-quality-selector'

const player = videojs(videoRef.value, {
  controls: true,
  fluid: true,
  sources: [{
    src: props.hlsUrl,
    type: 'application/x-mpegURL'
  }],
  plugins: {
    hlsQualitySelector: {
      displayCurrentQuality: true,
    }
  }
})
</script>
```

---

### 3. 文件上传

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **分块上传** | Fine Uploader | Uppy + TUS | `@uppy/core`, `@uppy/tus`, `tus-js-client` | `composables/useUpload.ts` |
| **断点续传** | Fine Uploader | TUS Protocol | `tus-js-client@^4.1.0` | 同上 |
| **拖拽上传** | Fine Uploader | Uppy Drag Drop | `@uppy/drag-drop@^3.1.0` | `components/media/MediaUpload.vue` |
| **摄像头录制** | - | Uppy Webcam | `@uppy/webcam@^3.4.0` | 同上 |
| **上传进度** | Fine Uploader | Uppy Dashboard | `@uppy/dashboard@^3.8.2` | 同上 |
| **文件类型验证** | Django | 前端验证 + 后端 | 自定义验证器 | `utils/validators.ts` |

**实现要点：**
```typescript
// composables/useUpload.ts
import Uppy from '@uppy/core'
import Tus from '@uppy/tus'
import Dashboard from '@uppy/dashboard'

export function useUpload() {
  const uppy = new Uppy({
    restrictions: {
      maxFileSize: 5 * 1024 * 1024 * 1000, // 5GB
      allowedFileTypes: ['video/*', 'audio/*', 'image/*', '.pdf'],
    },
  })
  .use(Tus, {
    endpoint: '/api/v1/media/upload/',
    chunkSize: import.meta.env.VITE_UPLOAD_CHUNK_SIZE,
    retryDelays: [0, 1000, 3000, 5000],
  })
  .use(Dashboard, {
    inline: true,
    target: '#upload-container',
    proudlyDisplayPoweredByUppy: false,
  })

  return { uppy }
}
```

---

### 4. 用户界面

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **UI 组件库** | 自定义 CSS | Element Plus | `element-plus@^2.6.3` | `plugins/element-plus.ts` |
| **图标** | Font Icons | Element Plus Icons | `@element-plus/icons-vue@^2.3.1` | 自动导入 |
| **响应式布局** | 自定义 CSS | Tailwind CSS | `tailwindcss@^3.4.1` | `tailwind.config.js` |
| **主题切换** | CSS 变量 | Pinia Store + CSS | `pinia` | `stores/ui.ts` |
| **国际化** | Django i18n | Vue I18n | `vue-i18n@^9.10.2` | `locales/index.ts` |
| **动画效果** | CSS Animations | VueUse Motion | `@vueuse/motion@^2.1.0`, `animate.css` | 组件内使用 |
| **无限滚动** | JavaScript | VueUse Directive | `@vueuse/core` | `directives/infinite-scroll.ts` |
| **虚拟滚动** | - | Vue Virtual Scroller | `vue-virtual-scroller@^2.0.0-beta.8` | 长列表组件 |

**实现要点：**
```typescript
// locales/index.ts
import { createI18n } from 'vue-i18n'
import en from './en.json'
import zh from './zh-CN.json'

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: { en, zh }
})

// stores/ui.ts
export const useUIStore = defineStore('ui', () => {
  const theme = ref<'light' | 'dark'>('light')
  
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    document.documentElement.setAttribute('data-theme', theme.value)
  }
  
  return { theme, toggleTheme }
})
```

---

### 5. 搜索与过滤

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **全文搜索** | PostgreSQL FTS | API 调用 | `axios` | `api/media.ts` |
| **实时搜索** | JavaScript | VueUse Debounce | `@vueuse/core` | `views/Search.vue` |
| **分类过滤** | Django Filter | Query Params | `vue-router` | 同上 |
| **标签过滤** | Django Filter | Query Params | `vue-router` | 同上 |
| **排序** | Django Order By | Query Params | `vue-router` | 同上 |

**实现要点：**
```vue
<!-- views/Search.vue -->
<script setup lang="ts">
import { useDebounceFn } from '@vueuse/core'

const searchQuery = ref('')
const searchResults = ref([])

const debouncedSearch = useDebounceFn(async (query: string) => {
  if (query.length < 2) return
  const results = await mediaApi.search({ q: query })
  searchResults.value = results
}, 500)

watch(searchQuery, (newQuery) => {
  debouncedSearch(newQuery)
})
</script>
```

---

### 6. 社交功能

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **评论系统** | Django Comments | API + 组件 | `axios` | `components/comments/` |
| **点赞/点踩** | Django Actions | API 调用 | `axios` | `composables/useLike.ts` |
| **分享** | JavaScript | Share API + Clipboard | `clipboard@^2.0.11` | `composables/useShare.ts` |
| **二维码分享** | - | QRCode Generator | `qrcode@^1.5.3` | `components/common/QRCode.vue` |
| **嵌入代码** | Django Template | Clipboard Copy | `clipboard` | `views/MediaDetail.vue` |
| **播放列表** | Django Models | API + Store | `axios`, `pinia` | `stores/playlists.ts` |

**实现要点：**
```typescript
// composables/useShare.ts
import Clipboard from 'clipboard'
import QRCode from 'qrcode'

export function useShare() {
  async function shareMedia(media: Media) {
    if (navigator.share) {
      await navigator.share({
        title: media.title,
        text: media.description,
        url: media.url,
      })
    } else {
      // 回退：复制到剪贴板
      const clipboard = new Clipboard('.share-btn')
      clipboard.on('success', () => {
        ElMessage.success('链接已复制')
      })
    }
  }
  
  async function generateQRCode(url: string) {
    return await QRCode.toDataURL(url)
  }
  
  return { shareMedia, generateQRCode }
}
```

---

### 7. 实时功能

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **实时通知** | - | WebSocket | `socket.io-client@^4.7.4` | `composables/useWebSocket.ts` |
| **编码进度** | Celery Tasks | WebSocket / Polling | `socket.io-client` | `composables/useEncodingStatus.ts` |
| **在线状态** | - | WebSocket | `socket.io-client` | 同上 |

**实现要点：**
```typescript
// composables/useWebSocket.ts
import { io } from 'socket.io-client'

export function useWebSocket() {
  const socket = io(import.meta.env.VITE_WS_URL, {
    auth: {
      token: authStore.csrfToken
    }
  })
  
  socket.on('encoding_progress', (data) => {
    // 更新编码进度
    mediaStore.updateEncodingProgress(data.mediaId, data.progress)
  })
  
  socket.on('notification', (notification) => {
    ElNotification({
      title: notification.title,
      message: notification.message,
    })
  })
  
  return { socket }
}
```

---

### 8. 数据管理

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **状态管理** | - | Pinia | `pinia@^2.1.7` | `stores/` |
| **状态持久化** | - | Pinia Plugin | `pinia-plugin-persistedstate@^3.2.1` | `main.ts` |
| **数据缓存** | Redis | LocalStorage + Pinia | 内置 | `stores/media.ts` |
| **分页** | Django Paginator | API + Component | `axios` | `composables/usePagination.ts` |

**实现要点：**
```typescript
// main.ts
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// stores/media.ts
export const useMediaStore = defineStore('media', () => {
  const cache = ref(new Map())
  
  async function getMedia(id: string) {
    // 先检查缓存
    if (cache.value.has(id)) {
      return cache.value.get(id)
    }
    
    // 从 API 获取
    const media = await mediaApi.getMediaDetail(id)
    cache.value.set(id, media)
    return media
  }
  
  return { getMedia }
}, {
  persist: {
    key: 'media-cache',
    storage: localStorage,
    paths: ['cache']
  }
})
```

---

### 9. 表单处理

| 功能 | 现有技术 | Vue 3 实现 | 依赖包 | 配置位置 |
|------|----------|-----------|--------|----------|
| **表单验证** | Django Forms | VeeValidate + Yup | `vee-validate@^4.12.6`, `yup@^1.4.0` | 表单组件 |
| **富文本编辑** | - | Quill Editor | `@vueup/vue-quill@^1.2.0` | `components/common/RichEditor.vue` |
| **Markdown** | - | Markdown-it | `markdown-it@^14.1.0` | `utils/markdown.ts` |

**实现要点：**
```vue
<!-- 表单验证示例 -->
<script setup lang="ts">
import { useForm } from 'vee-validate'
import * as yup from 'yup'

const schema = yup.object({
  title: yup.string().required('标题必填').min(3, '至少3个字符'),
  description: yup.string().max(500, '最多500字符'),
  category: yup.string().required('请选择分类'),
})

const { errors, handleSubmit } = useForm({
  validationSchema: schema,
})

const onSubmit = handleSubmit(async (values) => {
  await mediaApi.updateMedia(mediaId, values)
})
</script>

<template>
  <el-form @submit="onSubmit">
    <el-form-item label="标题" :error="errors.title">
      <el-input v-model="title" />
    </el-form-item>
  </el-form>
</template>
```

---

### 10. 性能优化

| 功能 | 技术方案 | 依赖包 | 配置位置 |
|------|----------|--------|----------|
| **懒加载路由** | Dynamic Import | `vue-router` | `router/index.ts` |
| **图片懒加载** | IntersectionObserver | `@vueuse/core` | `directives/lazy-load.ts` |
| **组件懒加载** | defineAsyncComponent | Vue 内置 | 组件使用处 |
| **代码分割** | Vite Rollup | `vite` | `vite.config.ts` |
| **Gzip 压缩** | Vite Plugin | `vite-plugin-compression` | `vite.config.ts` |
| **Tree Shaking** | Vite | `vite` | 自动 |
| **Bundle 分析** | Visualizer | `rollup-plugin-visualizer` | `vite.config.ts` |

---

## 📊 依赖总结

### 生产依赖 (18 个核心包)
```json
{
  "vue": "^3.4.21",
  "vue-router": "^4.3.0",
  "pinia": "^2.1.7",
  "pinia-plugin-persistedstate": "^3.2.1",
  "axios": "^1.6.8",
  "element-plus": "^2.6.3",
  "@element-plus/icons-vue": "^2.3.1",
  "@vueuse/core": "^10.9.0",
  "video.js": "^8.10.0",
  "@videojs/http-streaming": "^3.12.0",
  "@uppy/core": "^3.9.3",
  "@uppy/tus": "^3.5.4",
  "tus-js-client": "^4.1.0",
  "vue-i18n": "^9.10.2",
  "vee-validate": "^4.12.6",
  "dayjs": "^1.11.10",
  "lodash-es": "^4.17.21",
  "clipboard": "^2.0.11"
}
```

### 开发依赖 (15 个核心包)
```json
{
  "@vitejs/plugin-vue": "^5.0.4",
  "vite": "^5.1.6",
  "typescript": "^5.4.2",
  "vue-tsc": "^2.0.6",
  "sass": "^1.72.0",
  "tailwindcss": "^3.4.1",
  "unplugin-auto-import": "^0.17.5",
  "unplugin-vue-components": "^0.26.0",
  "vite-plugin-compression": "^0.5.1",
  "eslint": "^8.57.0",
  "eslint-plugin-vue": "^9.23.0",
  "@typescript-eslint/eslint-plugin": "^7.2.0",
  "prettier": "^3.2.5",
  "autoprefixer": "^10.4.18",
  "rollup-plugin-visualizer": "^5.12.0"
}
```

---

## ✅ 实施验证清单

### 阶段 1：基础设施 ✓
- [ ] Node.js >= 18
- [ ] npm / pnpm / yarn
- [ ] Vue 3 项目创建
- [ ] Vite 配置完成
- [ ] TypeScript 配置
- [ ] ESLint + Prettier

### 阶段 2：核心功能 ✓
- [ ] 路由系统
- [ ] 状态管理 (Pinia)
- [ ] API 客户端 (Axios + CSRF)
- [ ] 认证流程 (Session)
- [ ] UI 组件库 (Element Plus)

### 阶段 3：媒体功能 ✓
- [ ] 视频播放器 (Video.js + HLS)
- [ ] 文件上传 (Uppy + TUS)
- [ ] PDF 预览
- [ ] 图片查看器
- [ ] 音频播放

### 阶段 4：交互功能 ✓
- [ ] 评论系统
- [ ] 点赞/点踩
- [ ] 分享功能
- [ ] 播放列表
- [ ] 搜索与过滤

### 阶段 5：高级功能 ✓
- [ ] 国际化 (i18n)
- [ ] 主题切换
- [ ] WebSocket 实时通知
- [ ] 表单验证
- [ ] 性能优化

### 阶段 6：测试与优化 ✓
- [ ] 单元测试
- [ ] E2E 测试
- [ ] 性能测试
- [ ] 浏览器兼容性测试
- [ ] 移动端适配

---

## 🚀 快速开始

```bash
# 使用安装脚本（推荐）
bash scripts/setup-vue-frontend.sh     # Linux/Mac
scripts\setup-vue-frontend.bat         # Windows

# 手动安装
npm create vite@latest frontend-vue -- --template vue-ts
cd frontend-vue
# 参考 vue3_complete_dependencies.md 安装所有依赖
```

---

## 📚 相关文档

- [Vue 3 迁移指南](./vue3_frontend_migration_guide.md)
- [完整依赖清单](./vue3_complete_dependencies.md)
- [Vue 3 官方文档](https://vuejs.org/)
- [Element Plus 文档](https://element-plus.org/)
- [VueUse 文档](https://vueuse.org/)

---

完成！✅

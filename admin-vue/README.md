# MediaCMS 管理后台

> 基于 Vue 3 + TypeScript + Element Plus 的现代化管理后台系统

## 📋 项目简介

这是 MediaCMS 的独立管理后台应用，与主站前端完全分离，提供专业的后台管理功能。

### ✨ 特性

- 🚀 **Vue 3** - 使用 Composition API
- 💪 **TypeScript** - 类型安全
- ⚡️ **Vite** - 极速开发体验
- 🎨 **Element Plus** - 企业级 UI 组件库
- 📊 **ECharts** - 强大的数据可视化
- 🎯 **Vue Router** - 官方路由管理
- 📦 **Pinia** - 新一代状态管理
- 🌓 **暗色主题** - 支持亮色/暗色切换

## 📁 项目结构

```
admin-vue/
├── public/                # 静态资源
├── src/
│   ├── api/              # API 接口
│   │   ├── http.ts       # HTTP 客户端配置
│   │   ├── admin.ts      # 管理后台 API
│   │   └── types.ts      # TypeScript 类型定义
│   ├── assets/           # 资源文件
│   ├── layouts/          # 布局组件
│   │   ├── AdminLayout.vue    # 主布局
│   │   └── components/        # 布局子组件
│   │       ├── Sidebar.vue    # 侧边栏
│   │       └── Header.vue     # 顶栏
│   ├── router/           # 路由配置
│   │   └── index.ts
│   ├── stores/           # Pinia stores
│   │   ├── auth.ts       # 认证状态
│   │   └── app.ts        # 应用状态
│   ├── styles/           # 全局样式
│   │   ├── index.scss
│   │   └── variables.scss
│   ├── views/            # 页面组件
│   │   ├── Dashboard/    # 仪表板
│   │   ├── Media/        # 媒体管理
│   │   ├── User/         # 用户管理
│   │   ├── Content/      # 内容管理
│   │   ├── System/       # 系统管理
│   │   ├── Login.vue     # 登录页
│   │   └── 404.vue       # 404 页面
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🚀 快速开始

### 前置要求

- Node.js >= 16
- npm >= 8

### 安装依赖

```bash
cd admin-vue
npm install
```

### 开发环境运行

```bash
npm run dev
```

浏览器访问: `http://localhost:5174/admin/`

### 生产环境构建

```bash
npm run build
```

构建产物会输出到 `../static/admin/` 目录

## 🔧 配置说明

### Vite 配置 (`vite.config.ts`)

```typescript
export default defineConfig({
  server: {
    port: 5174,              // 开发服务器端口
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Django 后端地址
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../static/admin',  // 构建输出目录
  },
})
```

### 环境变量

可以创建 `.env` 文件配置环境变量：

```bash
# API 基础路径
VITE_API_BASE_URL=/api

# 应用标题
VITE_APP_TITLE=MediaCMS 管理后台
```

## 📊 功能模块

### 1. 仪表板

- ✅ 数据统计卡片（媒体、用户、观看量、待审核）
- ✅ 系统状态监控（CPU、内存、磁盘）
- ✅ 快捷操作入口
- ⏳ 数据图表（开发中）

### 2. 媒体管理

- ✅ 媒体列表展示
- ✅ 搜索和筛选功能
- ✅ 状态标签显示
- ⏳ 批量操作（开发中）
- ⏳ 媒体编辑（开发中）

### 3. 用户管理

- ⏳ 用户列表（开发中）
- ⏳ 用户详情（开发中）
- ⏳ 权限管理（开发中）

### 4. 内容管理

- ⏳ 评论管理（开发中）
- ⏳ 举报处理（开发中）
- ⏳ 内容审核（开发中）

### 5. 系统管理

- ⏳ 系统设置（开发中）
- ⏳ 系统监控（开发中）
- ⏳ 日志查看（开发中）

## 🔐 权限控制

### 路由守卫

所有路由默认需要登录，登录后会检查用户是否有管理员权限：

```typescript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth && !authStore.token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})
```

### API 拦截器

自动在请求头添加 Token：

```typescript
http.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Token ${authStore.token}`
  }
  return config
})
```

## 🎨 主题定制

### 切换主题

点击顶栏的主题切换按钮，或调用：

```typescript
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
appStore.toggleTheme()  // 切换主题
```

### 自定义主题色

修改 `src/styles/variables.scss`：

```scss
$primary-color: #409eff;  // 主题色
$success-color: #67c23a;  // 成功色
$warning-color: #e6a23c;  // 警告色
$danger-color: #f56c6c;   // 危险色
```

## 📡 API 调用示例

```typescript
import { getManageMedia } from '@/api/admin'

// 获取媒体列表
const loadMedia = async () => {
  try {
    const response = await getManageMedia({
      page: 1,
      search: '关键词',
      state: 'public',
      featured: true
    })
    console.log(response.results)
  } catch (error) {
    console.error('加载失败:', error)
  }
}
```

## 🔌 与 Django 集成

### Django URL 配置

在 `cms/urls.py` 添加：

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ... 其他路由
    
    # 管理后台 SPA 入口
    re_path(r'^admin/.*', TemplateView.as_view(
        template_name='admin/index.html'
    ), name='admin_spa'),
]
```

### 模板文件

将构建产物复制到 Django 的 `static/admin/` 目录，然后创建模板文件。

## 📝 开发规范

### 组件命名

- 使用 PascalCase: `UserList.vue`
- 布局组件: `AdminLayout.vue`
- 页面组件: 放在 `views/` 目录

### API 命名

- 列表接口: `getXxxList`
- 详情接口: `getXxxDetail`
- 创建接口: `createXxx`
- 更新接口: `updateXxx`
- 删除接口: `deleteXxx`

### 状态管理

- 使用 Pinia 进行状态管理
- 按功能模块划分 store
- 使用 Composition API 风格

## 🐛 常见问题

### Q1: 启动后无法访问？

**A:** 检查端口是否被占用，可以修改 `vite.config.ts` 中的端口号。

### Q2: API 请求失败？

**A:** 检查 `vite.config.ts` 中的 proxy 配置，确保 Django 后端正在运行。

### Q3: 登录后提示无权限？

**A:** 确保登录用户具有 `is_staff` 或 `is_superuser` 权限。

### Q4: 构建后样式丢失？

**A:** 检查 Django 静态文件配置，确保正确收集静态文件。

## 📚 技术文档

- [Vue 3 文档](https://cn.vuejs.org/)
- [TypeScript 文档](https://www.typescriptlang.org/zh/)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [Vite 文档](https://cn.vitejs.dev/)
- [Pinia 文档](https://pinia.vuejs.org/zh/)

## 📄 License

MIT License

## 👥 贡献指南

欢迎提交 Issue 和 Pull Request！

---

**MediaCMS Admin v1.0** - 让管理更简单 ✨


# MediaCMS 前后端 API 端点对照表

## 📋 API 端点分类

### 1. REST API 端点（使用 `/api/v1/` 前缀）

这些端点使用 `http` 实例（`baseURL: '/api'`）：

| 前端调用 | 实际 URL | 说明 |
|---------|---------|------|
| `http.get('/v1/media')` | `/api/v1/media` | 获取媒体列表 |
| `http.get('/v1/users')` | `/api/v1/users` | 获取用户列表 |
| `http.get('/v1/categories')` | `/api/v1/categories` | 获取分类列表 |
| `http.get('/v1/tags')` | `/api/v1/tags` | 获取标签列表 |
| `http.get('/v1/comments')` | `/api/v1/comments` | 获取评论列表 |
| `http.get('/v1/playlists')` | `/api/v1/playlists` | 获取播放列表 |
| `http.post('/v1/login')` | `/api/v1/login` | REST API 登录（如果存在） |

**使用方式：**
```typescript
import http from '../services/http'
const BASE = '/v1'
const data = await http.get(`${BASE}/media`)
```

---

### 2. Django allauth 端点（**不使用** `/api` 前缀）

这些端点**直接使用根路径**，需要使用 `axios` 并指定完整的后端 URL：

| 前端调用 | 实际 URL | 说明 |
|---------|---------|------|
| `axios.post('/accounts/signup/', ...)` | `/accounts/signup/` | 用户注册 |
| `axios.post('/accounts/login/', ...)` | `/accounts/login/` | Session 登录 |
| `axios.post('/accounts/logout/', ...)` | `/accounts/logout/` | Session 登出 |

**使用方式：**
```typescript
import axios from 'axios'
const backendURL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
await axios.post('/accounts/signup/', formData, {
  baseURL: backendURL, // 重要：不使用 /api 前缀
  withCredentials: true
})
```

---

### 3. 其他端点

| 端点 | 说明 |
|------|------|
| `/admin/` | Django Admin（不使用 /api 前缀） |
| `/static/` | 静态文件（不使用 /api 前缀） |
| `/media/` | 媒体文件（不使用 /api 前缀） |

---

## 🔧 配置说明

### 环境变量（`frontend-vue/.env.development`）

```bash
# REST API 基础地址（用于 http 实例）
VITE_API_BASE=http://localhost:8000/api

# 后端完整 URL（用于 allauth 端点）
VITE_BACKEND_URL=http://localhost:8000

# 前端地址
VITE_FRONTEND_URL=http://localhost:8080
```

---

## ⚠️ 常见错误

### ❌ 错误示例

```typescript
// 错误：Django allauth 端点不应使用 /api 前缀
const baseURL = import.meta.env.VITE_API_BASE || '/api'
await axios.post('/accounts/signup/', formData, {
  baseURL  // 这会变成 /api/accounts/signup/，导致 404
})
```

### ✅ 正确示例

```typescript
// 正确：使用完整的后端 URL
const backendURL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
await axios.post('/accounts/signup/', formData, {
  baseURL: backendURL  // 这会变成 http://localhost:8000/accounts/signup/
})
```

---

## 📝 修复清单

- ✅ `createUser()` - 已修复，使用 `VITE_BACKEND_URL` 而不是 `VITE_API_BASE`
- ✅ `login()` - 已修复，回退到 Session 认证时使用 `VITE_BACKEND_URL`
- ⚠️ 需要检查其他使用 `/accounts/` 的地方（如 logout）

---

## 🎯 总结

1. **REST API**：使用 `http` 实例，`baseURL: '/api'`，路径为 `/v1/xxx`
2. **Django allauth**：使用 `axios` 直接调用，`baseURL: 'http://localhost:8000'`，路径为 `/accounts/xxx`
3. **静态文件**：直接使用相对路径，如 `/static/`、`/media/`


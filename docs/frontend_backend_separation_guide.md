# MediaCMS 前后端分离实施指南

## 📌 目标
将 MediaCMS 改造为完全前后端分离的架构，后端提供纯 REST API，前端独立部署为 SPA 应用。

---

## 🏗️ 架构设计

### 分离后的系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                   前端应用（独立）                              │
│  技术栈: React 18 + TypeScript + Vite/Next.js                │
│  部署: Vercel/Netlify/独立 Nginx 服务器                       │
│  域名: https://app.mediacms.com                              │
└─────────────────────────────────────────────────────────────┘
                            ⬇ HTTPS + CORS
┌─────────────────────────────────────────────────────────────┐
│                   后端 API（独立）                              │
│  技术栈: Django 5 + DRF + Celery                             │
│  部署: Docker/uWSGI + Nginx                                 │
│  域名: https://api.mediacms.com                              │
└─────────────────────────────────────────────────────────────┘
                    ⬇                    ⬇
         ┌──────────────────┐   ┌──────────────────┐
         │  PostgreSQL 15   │   │   Redis 7.x      │
         └──────────────────┘   └──────────────────┘
                            ⬇
         ┌──────────────────────────────────────────┐
         │     媒体存储 (S3/OSS/MinIO)                │
         │     https://media.mediacms.com            │
         └──────────────────────────────────────────┘
```

---

## 🔧 后端改造方案

### 1. 认证系统改造（JWT）

#### 当前问题
- 依赖 Django Session（需要 Cookie）
- 使用 django-allauth（绑定模板）
- CSRF 令牌验证（不适合前后端分离）

#### 解决方案：引入 JWT 认证

**安装依赖：**
```bash
pip install djangorestframework-simplejwt
pip install django-cors-headers
```

**新增配置文件：`cms/settings_api.py`**

```python
# 继承原有配置
from .settings import *

# CORS 配置
INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 移除 CSRF 中间件（JWT 不需要）
    # 'django.middleware.csrf.CsrfViewMiddleware',
] + [m for m in MIDDLEWARE if 'csrf' not in m.lower()]

# CORS 设置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # 开发环境
    "https://app.mediacms.com",   # 生产环境
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# JWT 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 可选：保留 Session 用于 Django Admin
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# 移除 CSRF 验证
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# 允许跨域文件上传
FILE_UPLOAD_MAX_MEMORY_SIZE = 800 * 1024 * 1000 * 5  # 4GB
DATA_UPLOAD_MAX_MEMORY_SIZE = FILE_UPLOAD_MAX_MEMORY_SIZE
```

---

### 2. 创建统一 API 路由

**新建文件：`api/__init__.py`**

```python
# API 模块初始化
```

**新建文件：`api/urls.py`**

```python
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# API 文档
schema_view = get_schema_view(
    openapi.Info(
        title="MediaCMS API",
        default_version='v1',
        description="MediaCMS REST API 文档",
        contact=openapi.Contact(email="api@mediacms.io"),
        license=openapi.License(name="AGPL v3"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # JWT 认证端点
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 用户认证（自定义）
    path('auth/', include('api.v1.auth.urls')),
    
    # 核心 API
    path('media/', include('files.urls')),        # 媒体相关
    path('users/', include('users.urls')),        # 用户管理
    path('playlists/', include('api.v1.playlists.urls')),
    
    # API 文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

---

### 3. 用户认证 API

**新建文件：`api/v1/auth/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
]
```

**新建文件：`api/v1/auth/views.py`**

```python
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import User
from users.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(APIView):
    """用户注册"""
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response('用户创建成功', UserSerializer),
            400: '验证失败',
        },
        tags=['认证'],
    )
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')
        
        # 验证
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': '用户名已存在'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': '邮箱已被注册'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
        )
        
        # 生成 JWT Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """用户登录"""
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={
            200: '登录成功',
            401: '认证失败',
        },
        tags=['认证'],
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class ProfileView(APIView):
    """获取当前用户信息"""
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        responses={200: UserSerializer},
        tags=['用户'],
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """更新用户信息"""
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """用户登出（Token 黑名单）"""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': '成功登出'})
        except Exception:
            return Response(
                {'error': '无效的 token'},
                status=status.HTTP_400_BAD_REQUEST
            )
```

---

### 4. 文件上传 API 改造

**修改文件：`files/views/media.py`**

在 `MediaList.post()` 方法中确保支持 multipart/form-data：

```python

class MediaList(APIView):
    """Media listings views"""
    
    permission_classes = (IsAuthorizedToAdd,)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="media_file", 
                in_=openapi.IN_FORM, 
                type=openapi.TYPE_FILE, 
                required=True, 
                description="媒体文件（视频/音频/图片/PDF）"
            ),
            openapi.Parameter(
                name="title", 
                in_=openapi.IN_FORM, 
                type=openapi.TYPE_STRING, 
                required=False
            ),
            openapi.Parameter(
                name="description", 
                in_=openapi.IN_FORM, 
                type=openapi.TYPE_STRING, 
                required=False
            ),
            openapi.Parameter(
                name="category", 
                in_=openapi.IN_FORM, 
                type=openapi.TYPE_STRING, 
                required=False
            ),
        ],
        tags=['媒体管理'],
        operation_summary='上传媒体文件',
        responses={
            201: MediaSerializer,
            400: '请求错误',
            401: '未认证',
        },
    )
    def post(self, request, format=None):
        """上传新媒体（支持大文件分块上传）"""
        
        # 验证文件
        if 'media_file' not in request.data:
            return Response(
                {'error': '缺少 media_file 字段'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = MediaSerializer(
            data=request.data, 
            context={"request": request}
        )
        
        if serializer.is_valid():
            media_file = request.data["media_file"]
            media = serializer.save(
                user=request.user, 
                media_file=media_file
            )
            
            return Response(
                MediaSerializer(media, context={"request": request}).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
```

---

### 5. 媒体文件访问权限控制

**新建文件：`api/v1/media/permissions.py`**

```python
from rest_framework import permissions
from files.models import Media, MediaPermission
from django.conf import settings


class CanAccessMedia(permissions.BasePermission):
    """检查用户是否有权访问媒体"""
    
    def has_object_permission(self, request, view, obj):
        # 公开媒体
        if obj.state == 'public' and obj.is_reviewed:
            return True
        
        # 媒体所有者
        if obj.user == request.user:
            return True
        
        # 编辑者权限
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # 检查直接权限
        if MediaPermission.objects.filter(
            media=obj, 
            user=request.user
        ).exists():
            return True
        
        # 检查 RBAC 权限
        if getattr(settings, 'USE_RBAC', False):
            if obj.category:
                rbac_categories = request.user.get_rbac_categories_as_member()
                if obj.category in rbac_categories:
                    return True
        
        return False
```

---

## 🎨 前端改造方案

### 1. 创建独立前端项目

**选项 A：使用 Vite + React（推荐）**

```bash
# 创建新项目
npm create vite@latest mediacms-frontend -- --template react-ts

cd mediacms-frontend
npm install

# 安装核心依赖
npm install axios react-router-dom
npm install @tanstack/react-query  # 数据获取
npm install zustand                 # 状态管理
npm install video.js                # 视频播放器
npm install @headlessui/react       # UI 组件
npm install tailwindcss             # 样式框架
```

**选项 B：使用 Next.js（SEO 优化）**

```bash
npx create-next-app@latest mediacms-frontend --typescript --tailwind --app
```

---

### 2. 前端目录结构

```
mediacms-frontend/
├── src/
│   ├── api/                    # API 调用
│   │   ├── client.ts          # Axios 实例
│   │   ├── auth.ts            # 认证 API
│   │   ├── media.ts           # 媒体 API
│   │   └── users.ts           # 用户 API
│   ├── components/            # 组件
│   │   ├── common/           # 通用组件
│   │   ├── media/            # 媒体组件
│   │   └── layout/           # 布局组件
│   ├── pages/                # 页面
│   │   ├── Home.tsx
│   │   ├── MediaDetail.tsx
│   │   ├── Login.tsx
│   │   └── Upload.tsx
│   ├── hooks/                # 自定义 Hooks
│   ├── store/                # 状态管理
│   ├── types/                # TypeScript 类型
│   └── utils/                # 工具函数
├── public/
├── package.json
└── vite.config.ts
```

---

### 3. API 客户端配置

**文件：`src/api/client.ts`**

```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：添加 JWT Token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：处理 Token 过期
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Token 过期，尝试刷新
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // 刷新失败，跳转登录
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

---

### 4. 认证 API

**文件：`src/api/auth.ts`**

```typescript
import apiClient from './client';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  name?: string;
}

export interface AuthResponse {
  user: {
    id: number;
    username: string;
    email: string;
    name: string;
  };
  tokens: {
    access: string;
    refresh: string;
  };
}

export const authApi = {
  // 登录
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const { data } = await apiClient.post('/auth/login/', credentials);
    
    // 保存 Token
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  // 注册
  register: async (userData: RegisterData): Promise<AuthResponse> => {
    const { data } = await apiClient.post('/auth/register/', userData);
    
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  // 登出
  logout: async (): Promise<void> => {
    const refreshToken = localStorage.getItem('refresh_token');
    try {
      await apiClient.post('/auth/logout/', { refresh_token: refreshToken });
    } finally {
      localStorage.clear();
    }
  },

  // 获取当前用户
  getCurrentUser: async () => {
    const { data } = await apiClient.get('/auth/profile/');
    return data;
  },
};
```

---

### 5. 媒体 API

**文件：`src/api/media.ts`**

```typescript
import apiClient from './client';

export interface Media {
  friendly_token: string;
  title: string;
  description: string;
  thumbnail_url: string;
  duration: number;
  views: number;
  likes: number;
  media_type: 'video' | 'audio' | 'image' | 'pdf';
  state: 'public' | 'private' | 'unlisted';
  user: string;
  add_date: string;
}

export const mediaApi = {
  // 获取媒体列表
  getMediaList: async (params?: {
    page?: number;
    author?: string;
    show?: 'recommended' | 'featured' | 'latest';
  }) => {
    const { data } = await apiClient.get('/media/', { params });
    return data;
  },

  // 获取媒体详情
  getMediaDetail: async (friendlyToken: string) => {
    const { data } = await apiClient.get(`/media/${friendlyToken}/`);
    return data;
  },

  // 上传媒体
  uploadMedia: async (file: File, metadata: {
    title?: string;
    description?: string;
    category?: string;
  }) => {
    const formData = new FormData();
    formData.append('media_file', file);
    
    if (metadata.title) formData.append('title', metadata.title);
    if (metadata.description) formData.append('description', metadata.description);
    if (metadata.category) formData.append('category', metadata.category);

    const { data } = await apiClient.post('/media/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / (progressEvent.total || 1)
        );
        console.log(`Upload Progress: ${percentCompleted}%`);
      },
    });

    return data;
  },

  // 删除媒体
  deleteMedia: async (friendlyToken: string) => {
    await apiClient.delete(`/media/${friendlyToken}/`);
  },

  // 点赞
  likeMedia: async (friendlyToken: string) => {
    const { data } = await apiClient.post(`/media/${friendlyToken}/like/`);
    return data;
  },
};
```

---

## 🚀 部署方案

### 后端部署

**Dockerfile（后端）**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# 复制代码
COPY . .

# 收集静态文件（仅用于 Admin）
RUN python manage.py collectstatic --noinput --settings=cms.settings_api

EXPOSE 8000

CMD ["gunicorn", "cms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

---

### 前端部署

**Dockerfile（前端）**

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 生产环境
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf（前端）**

```nginx
server {
    listen 80;
    server_name app.mediacms.com;

    root /usr/share/nginx/html;
    index index.html;

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理（可选，用于开发）
    location /api {
        proxy_pass http://api.mediacms.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## ✅ 迁移检查清单

### 后端
- [ ] 安装并配置 `djangorestframework-simplejwt`
- [ ] 配置 CORS 允许前端域名
- [ ] 创建 JWT 认证端点
- [ ] 改造所有 API 移除 CSRF 依赖
- [ ] 确保文件上传支持 multipart
- [ ] 配置媒体文件 CORS 头
- [ ] 部署到独立域名

### 前端
- [ ] 创建独立 React 项目
- [ ] 实现 Axios 拦截器（Token 管理）
- [ ] 实现登录/注册页面
- [ ] 实现媒体列表/详情页
- [ ] 实现文件上传组件
- [ ] 配置环境变量（API_URL）
- [ ] 部署到 CDN/静态托管

---

## 📚 参考资源

- [Django REST Framework JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
- [React Query](https://tanstack.com/query/latest)
- [Vite 官方文档](https://vitejs.dev/)

---

## 🎯 总结

完全分离后的优势：
1. **独立开发**：前后端团队可并行开发
2. **灵活部署**：前端可部署到 CDN，提升访问速度
3. **技术栈自由**：前端可轻松切换框架（React/Vue/Angular）
4. **扩展性强**：可开发多个客户端（Web、移动端、桌面端）
5. **安全性高**：JWT 无状态认证，减少 CSRF 攻击面

主要挑战：
1. **CORS 配置**：需要正确配置跨域
2. **认证复杂**：从 Session 迁移到 JWT
3. **文件上传**：大文件上传需要优化
4. **SEO 问题**：SPA 需要 SSR 或预渲染

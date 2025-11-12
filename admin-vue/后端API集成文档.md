# 后端 API 集成文档

## 概述

本文档说明管理后台与后端 API 的集成情况，包括新增的 API 接口和现有接口的使用。

## 新增 API 接口

所有新增的管理员专用 API 都以 `/api/v1/admin/` 为前缀。

### 1. 仪表板统计

**端点**: `GET /api/v1/admin/dashboard/stats`

**权限**: 需要编辑者（editor）或更高权限

**响应示例**:
```json
{
  "overview": {
    "total_media": 1250,
    "total_users": 350,
    "total_comments": 4200,
    "total_views": 125000,
    "total_likes": 8500,
    "today_media": 12,
    "today_users": 5,
    "media_trend": 15.5,
    "users_trend": 8.3
  },
  "media_by_type": [
    { "media_type": "video", "count": 850, "total_views": 98000 },
    { "media_type": "image", "count": 280, "total_views": 18000 },
    { "media_type": "audio", "count": 85, "total_views": 7000 },
    { "media_type": "pdf", "count": 35, "total_views": 2000 }
  ],
  "encoding_stats": [
    { "encoding_status": "success", "count": 1180 },
    { "encoding_status": "pending", "count": 45 },
    { "encoding_status": "running", "count": 15 },
    { "encoding_status": "fail", "count": 10 }
  ],
  "daily_stats": [
    { "date": "2025-11-01", "media": 28, "views": 3500 },
    { "date": "2025-11-02", "media": 32, "views": 4200 }
  ],
  "pending": {
    "pending_media": 15,
    "reported_media": 3
  },
  "active_users": 185
}
```

### 2. 批量用户操作

**端点**: `POST /api/v1/admin/users/batch`

**权限**: 需要管理员（manager）或更高权限

**请求体**:
```json
{
  "action": "block",  // delete, block, unblock, set_editor, set_manager, remove_role
  "user_ids": ["user1", "user2", "user3"]
}
```

**响应示例**:
```json
{
  "success": 3,
  "failed": 0,
  "message": "成功封禁 3 个用户"
}
```

**支持的操作**:
- `delete`: 批量删除用户
- `block`: 批量封禁用户
- `unblock`: 批量解封用户
- `set_editor`: 批量设置为编辑者
- `set_manager`: 批量设置为管理员
- `remove_role`: 批量移除角色

### 3. 批量媒体操作

**端点**: `POST /api/v1/admin/media/batch`

**权限**: 需要编辑者（editor）或更高权限

**请求体**:
```json
{
  "action": "feature",
  "media_ids": ["token1", "token2", "token3"],
  "category": "新闻"  // 仅用于 set_category 操作
}
```

**响应示例**:
```json
{
  "success": 3,
  "failed": 0,
  "message": "成功设置 3 个精选媒体"
}
```

**支持的操作**:
- `delete`: 批量删除媒体
- `approve`: 批量审核通过
- `reject`: 批量审核拒绝
- `feature`: 批量设置为精选
- `unfeature`: 批量取消精选
- `set_public`: 批量设置为公开
- `set_private`: 批量设置为私有
- `set_unlisted`: 批量设置为不公开
- `set_category`: 批量设置分类（需要提供 category 参数）

### 4. 系统监控

**端点**: `GET /api/v1/admin/system/monitoring`

**权限**: 需要管理员（manager）或更高权限

**响应示例**:
```json
{
  "cpu": {
    "percent": 45.2,
    "count": 8,
    "load_avg": [1.5, 1.3, 1.2]
  },
  "memory": {
    "total": 16.0,
    "used": 8.5,
    "percent": 53.1
  },
  "disk": {
    "total": 500.0,
    "used": 320.5,
    "percent": 64.1
  },
  "network": {
    "bytes_sent": 15420.5,
    "bytes_recv": 48320.2
  },
  "database": {
    "queries": 0
  }
}
```

### 5. 热门分类

**端点**: `GET /api/v1/admin/categories/popular`

**权限**: 需要编辑者（editor）或更高权限

**响应示例**:
```json
[
  {
    "title": "新闻",
    "media_count": 350,
    "description": "新闻类媒体"
  },
  {
    "title": "教育",
    "media_count": 280,
    "description": "教育类内容"
  }
]
```

### 6. 活跃用户

**端点**: `GET /api/v1/admin/users/active`

**权限**: 需要编辑者（editor）或更高权限

**响应示例**:
```json
[
  {
    "username": "user1",
    "name": "张三",
    "email": "user1@example.com",
    "media_count": 45,
    ...
  }
]
```

## 现有 API 接口

以下是管理后台使用的现有 API 接口：

### 1. 媒体管理

**端点**: `GET /api/v1/manage_media`

**查询参数**:
- `page`: 页码
- `sort_by`: 排序字段（title, add_date, edit_date, views, likes, reported_times）
- `ordering`: 排序方向（asc, desc）
- `state`: 媒体状态（public, private, unlisted）
- `encoding_status`: 编码状态（pending, running, success, fail）
- `featured`: 是否精选（true, false, all）
- `is_reviewed`: 是否已审核（true, false, all）
- `category`: 分类标题
- `media_type`: 媒体类型（video, image, audio, pdf）

**删除媒体**: `DELETE /api/v1/manage_media?tokens=token1,token2`

### 2. 用户管理

**端点**: `GET /api/v1/manage_users`

**查询参数**:
- `page`: 页码
- `sort_by`: 排序字段（name, date_added）
- `ordering`: 排序方向（asc, desc）
- `role`: 用户角色（all, manager, editor）
- `is_approved`: 是否已批准（true, false）

**删除用户**: `DELETE /api/v1/manage_users?tokens=user1,user2`

### 3. 评论管理

**端点**: `GET /api/v1/manage_comments`

**查询参数**:
- `page`: 页码
- `sort_by`: 排序字段（text, add_date）
- `ordering`: 排序方向（asc, desc）

**删除评论**: `DELETE /api/v1/manage_comments?comment_ids=id1,id2`

## 权限说明

### 权限级别

1. **普通用户 (User)**: 无管理权限
2. **编辑者 (Editor)**: 可以管理媒体和评论
3. **管理员 (Manager)**: 可以管理媒体、评论和用户
4. **超级管理员 (Superuser)**: 拥有所有权限

### 权限类

- `IsMediacmsEditor`: 要求编辑者或更高权限
- `IsMediacmsManager`: 要求管理员或更高权限

## 前端 API 调用

所有 API 调用都通过 `admin-vue/src/api/admin.ts` 进行封装：

```typescript
import { getDashboardStats } from '@/api/admin'

// 获取仪表板统计
const stats = await getDashboardStats()

// 批量删除媒体
await batchDeleteMedia(['token1', 'token2'])

// 批量封禁用户
await batchBlockUsers(['user1', 'user2'])
```

## 依赖要求

后端需要安装以下 Python 包：

```txt
psutil==6.1.1  # 用于系统监控
```

安装命令：
```bash
pip install psutil==6.1.1
```

## 错误处理

所有 API 在遇到错误时会返回适当的 HTTP 状态码和错误信息：

- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未登录
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

前端会通过 Axios 拦截器统一处理这些错误，并显示相应的提示信息。

## 测试建议

1. 使用超级管理员账户测试所有功能
2. 测试不同权限级别用户的访问控制
3. 测试批量操作的边界情况（空列表、超大列表等）
4. 测试系统监控在不同操作系统上的兼容性
5. 进行性能测试，确保大数据量下的响应速度

## 未来改进

1. 添加更细粒度的权限控制
2. 实现数据导出功能
3. 添加操作日志记录
4. 实现实时通知系统
5. 优化批量操作的性能


# 密码重置功能修复说明

## 问题描述

前端请求 `/api/v1/auth/password/reset` 接口时返回 404 错误，因为该 API 端点不存在。

## 修复内容

### 1. 添加密码重置 API 视图

在 `users/views.py` 中添加了 `PasswordResetView` 类：
- 支持 POST 请求发送密码重置邮件
- 验证邮箱格式
- 使用 Django 内置的密码重置功能
- 返回统一的成功消息（安全考虑）

### 2. 配置 URL 路由

在 `users/urls.py` 中添加了新的路由：
```python
path('api/v1/auth/password/reset', views.PasswordResetView.as_view(), name='password-reset'),
```

### 3. 创建邮件模板

创建了密码重置邮件模板：
- `templates/registration/password_reset_email.html` - 邮件内容模板
- `templates/registration/password_reset_subject.txt` - 邮件主题模板

### 4. 更新邮件配置

修改了 `cms/settings.py` 中的邮件配置：
- 支持环境变量配置邮件服务器
- 移除了硬编码的邮件设置
- 更新了 `.env.example` 文件

## 使用说明

### 1. 配置邮件服务

在 `.env` 文件中配置邮件设置：

```bash
# 开发环境 - 在控制台显示邮件内容
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# 生产环境 - 使用 SMTP 发送邮件
# EMAIL_BACKEND=djcelery_email.backends.CeleryEmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# EMAIL_USE_TLS=True
# DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 2. API 使用方法

**请求地址**: `POST /api/v1/auth/password/reset`

**请求参数**:
```json
{
  "email": "user@example.com"
}
```

**成功响应**:
```json
{
  "message": "如果该邮箱地址存在于我们的系统中，您将收到密码重置邮件"
}
```

**错误响应**:
```json
{
  "detail": "请输入有效的邮箱地址"
}
```

### 3. 前端集成

前端代码已经正确配置，发送请求到 `/api/v1/auth/password/reset`。

### 4. 测试

可以使用提供的测试脚本：
```bash
python test_password_reset.py
```

## 安全特性

1. **邮箱验证**: 验证邮箱格式的有效性
2. **统一响应**: 无论用户是否存在都返回相同消息，防止邮箱枚举攻击
3. **链接有效期**: 密码重置链接默认24小时内有效
4. **一次性使用**: 每个重置链接只能使用一次

## 邮件发送流程

1. 用户在前端输入邮箱地址
2. 前端发送 POST 请求到 `/api/v1/auth/password/reset`
3. 后端验证邮箱格式和用户存在性
4. 生成密码重置令牌和链接
5. 发送包含重置链接的邮件
6. 用户点击邮件中的链接完成密码重置

## 注意事项

1. **邮件配置**: 确保邮件服务器配置正确
2. **HTTPS**: 生产环境建议使用 HTTPS 确保重置链接安全
3. **邮件模板**: 可以根据需要自定义邮件模板的样式和内容
4. **日志记录**: 建议添加密码重置请求的日志记录

## 故障排除

### 邮件发送失败
1. 检查邮件服务器配置
2. 确认邮箱密码或应用密码正确
3. 检查防火墙和网络连接

### API 404 错误
1. 确认 URL 路由配置正确
2. 重启 Django 服务器
3. 检查 URL 路径是否正确

### 邮件模板错误
1. 确认模板文件路径正确
2. 检查模板语法
3. 确认 Django 能找到模板目录

---

**修复完成时间**: 2025年11月12日  
**修复版本**: v1.1  
**相关文件**: 
- `users/views.py`
- `users/urls.py`
- `cms/settings.py`
- `templates/registration/password_reset_email.html`
- `templates/registration/password_reset_subject.txt`

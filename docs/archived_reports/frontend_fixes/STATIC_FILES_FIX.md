# 静态文件 404 错误修复

## 🎯 问题描述

Django 管理界面和前端页面出现静态文件 404 错误：
- `/static/css/_commons.css`
- `/static/js/_commons.js`
- `/static/lib/gfonts/gfonts.css`
- 等其他静态文件

## 🔧 修复方案

### 1. 添加开发模式静态文件服务

在 `cms/urls.py` 中添加了开发模式下的静态文件服务配置：

```python
# Add debug toolbar URLs in development
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            re_path(r"^__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
    
    # Serve static and media files in development
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 2. 验证配置

- ✅ DEBUG 模式已启用
- ✅ STATIC_ROOT 目录存在
- ✅ 所有静态文件都已收集
- ✅ URL 配置已更新

## 🚀 解决步骤

1. **重启 Django 服务器**：
   ```bash
   Ctrl+C  # 停止当前服务器
   python manage.py runserver localhost:8000  # 重新启动
   ```

2. **访问管理界面**：
   ```
   http://localhost:8000/admin/
   ```

3. **检查静态文件**：
   - CSS 样式应该正常加载
   - JavaScript 功能应该正常工作
   - 图标和字体应该正常显示

## 📋 预期结果

重启服务器后，应该不再看到以下 404 错误：
- `GET /static/css/_commons.css`
- `GET /static/js/_commons.js`
- `GET /static/lib/gfonts/gfonts.css`
- `GET /static/lib/material-icons/material-icons.css`
- 等其他静态文件

## 🔍 故障排除

如果问题仍然存在：

1. **重新收集静态文件**：
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **检查 .env 文件**：
   确保 `DJANGO_DEBUG=True`

3. **清除浏览器缓存**：
   按 Ctrl+F5 强制刷新

## 📝 技术说明

在 Django 开发模式下，静态文件需要通过 `django.conf.urls.static.static()` 函数来服务。这个配置只在 `DEBUG=True` 时生效，生产环境应该使用 Nginx 或 Apache 来服务静态文件。

---

**修复完成时间**: 2025年11月12日  
**相关文件**: `cms/urls.py`, `check_static_config.py`

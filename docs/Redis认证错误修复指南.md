# Redis 认证错误修复指南

## 🔍 问题分析

错误信息：`redis.exceptions.AuthenticationError: Authentication required.`

**原因：**
1. Redis 服务器设置了密码（例如：`root`）
2. Celery 的 `BROKER_URL` 和 `CELERY_RESULT_BACKEND` 没有包含密码
3. Celery 不使用 Django `CACHES` 配置中的 `PASSWORD` 选项，而是直接从 URL 中读取密码

## ✅ 解决方案

### 方案 1：在 Redis URL 中包含密码（推荐）

修改 `cms/local_settings.py`：

```python
# 如果 Redis 有密码
REDIS_PASSWORD = "root"  # 改为你的 Redis 密码
REDIS_LOCATION = f"redis://:{REDIS_PASSWORD}@127.0.0.1:6379/1"

# 如果 Redis 没有密码
# REDIS_PASSWORD = None
# REDIS_LOCATION = "redis://127.0.0.1:6379/1"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD if REDIS_PASSWORD else None,
        },
    }
}

BROKER_URL = REDIS_LOCATION
CELERY_RESULT_BACKEND = REDIS_LOCATION
```

**重要：** `BROKER_URL` 和 `CELERY_RESULT_BACKEND` 必须包含密码（如果 Redis 设置了密码）。

### 方案 2：移除 Redis 密码（开发环境）

如果你使用的是本地 Redis 服务器，可以在开发环境中移除密码：

1. **编辑 Redis 配置文件**（通常在 `redis.conf` 或 `redis.windows.conf`）：
   ```conf
   # 注释掉或移除这行
   # requirepass root
   ```

2. **重启 Redis 服务器**

3. **修改 `cms/local_settings.py`**：
   ```python
   REDIS_LOCATION = "redis://127.0.0.1:6379/1"  # 不包含密码
   ```

## 🔧 验证修复

修复后，重启 Django 开发服务器和 Celery worker：

```powershell
# 停止当前服务器（Ctrl+C）

# 重启 Django 服务器
python manage.py runserver

# 重启 Celery worker（如果正在运行）
celery -A cms worker -l info
```

## ⚠️ 注意事项

1. **URL 格式**：
   - 有密码：`redis://:password@host:port/db`
   - 无密码：`redis://host:port/db`

2. **密码中的特殊字符**：
   - 如果密码包含特殊字符（如 `@`、`:`），需要进行 URL 编码：
     ```python
     import urllib.parse
     encoded_password = urllib.parse.quote("your@password")
     REDIS_LOCATION = f"redis://:{encoded_password}@127.0.0.1:6379/1"
     ```

3. **Celery 配置**：
   - `BROKER_URL` 和 `CELERY_RESULT_BACKEND` 必须相同
   - 如果 Redis 有密码，两者都必须在 URL 中包含密码

## 📝 检查清单

- ✅ `REDIS_LOCATION` 包含密码（如果 Redis 设置了密码）
- ✅ `BROKER_URL = REDIS_LOCATION`
- ✅ `CELERY_RESULT_BACKEND = REDIS_LOCATION`
- ✅ `CACHES` 配置中的 `PASSWORD` 与 Redis 密码匹配
- ✅ Redis 服务器正在运行
- ✅ Django 和 Celery worker 已重启

## 🎯 快速修复

如果 Redis 密码是 `root`，直接修改 `cms/local_settings.py`：

```python
REDIS_LOCATION = "redis://:root@127.0.0.1:6379/1"
BROKER_URL = REDIS_LOCATION
CELERY_RESULT_BACKEND = REDIS_LOCATION
```

然后重启 Django 服务器即可！

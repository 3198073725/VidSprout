"""
从环境变量加载配置的辅助模块
用于替代硬编码的敏感信息
"""
import os
from pathlib import Path


def get_env(key: str, default=None, required=False):
    """
    从环境变量获取配置值
    
    Args:
        key: 环境变量名
        default: 默认值
        required: 是否必需（如果为True且未设置，则抛出异常）
    
    Returns:
        环境变量的值或默认值
    """
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def get_bool_env(key: str, default=False):
    """
    从环境变量获取布尔值
    
    支持的真值: true, True, TRUE, 1, yes, Yes, YES
    其他所有值都视为 False
    """
    value = os.environ.get(key, str(default))
    return value.lower() in ('true', '1', 'yes')


def get_int_env(key: str, default=0):
    """
    从环境变量获取整数值
    """
    value = os.environ.get(key, str(default))
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def get_list_env(key: str, default=None, separator=','):
    """
    从环境变量获取列表值
    
    例如: ALLOWED_HOSTS=localhost,127.0.0.1,example.com
    返回: ['localhost', '127.0.0.1', 'example.com']
    """
    if default is None:
        default = []
    value = os.environ.get(key)
    if not value:
        return default
    return [item.strip() for item in value.split(separator) if item.strip()]


# 数据库配置
def get_database_config():
    """获取数据库配置"""
    return {
        'ENGINE': get_env('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': get_env('DB_NAME', 'mediacms'),
        'USER': get_env('DB_USER', 'mediacms'),
        'PASSWORD': get_env('DB_PASSWORD', 'mediacms'),
        'HOST': get_env('DB_HOST', '127.0.0.1'),
        'PORT': get_env('DB_PORT', '5432'),
        'OPTIONS': {'pool': True},
    }


# Redis 配置
def get_redis_location():
    """
    获取 Redis 连接字符串
    
    格式: redis://[:password@]host:port/db
    """
    host = get_env('REDIS_HOST', '127.0.0.1')
    port = get_env('REDIS_PORT', '6379')
    password = get_env('REDIS_PASSWORD', '')
    db = get_env('REDIS_DB', '1')
    
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    else:
        return f"redis://{host}:{port}/{db}"


# 邮件配置
def get_email_config():
    """获取邮件配置"""
    return {
        'EMAIL_BACKEND': get_env('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'),
        'EMAIL_HOST': get_env('EMAIL_HOST', 'localhost'),
        'EMAIL_PORT': get_int_env('EMAIL_PORT', 587),
        'EMAIL_HOST_USER': get_env('EMAIL_HOST_USER', ''),
        'EMAIL_HOST_PASSWORD': get_env('EMAIL_HOST_PASSWORD', ''),
        'EMAIL_USE_TLS': get_bool_env('EMAIL_USE_TLS', True),
        'DEFAULT_FROM_EMAIL': get_env('DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
    }


# 示例使用:
# from cms.env_settings import get_env, get_database_config
# 
# SECRET_KEY = get_env('DJANGO_SECRET_KEY', required=True)
# DEBUG = get_bool_env('DJANGO_DEBUG', default=False)
# DATABASES = {'default': get_database_config()}


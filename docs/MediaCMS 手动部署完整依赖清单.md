# MediaCMS 手动部署完整依赖清单

## 一、系统基础要求

### 操作系统

- **推荐系统**: Ubuntu 20.04/22.04/24.04 或 Debian 10/11/12（Buster/Bullseye/Bookworm）
- **可选系统**: RHEL 8/9 或 CentOS Stream 8/9
- **架构**: x86_64（AMD64）

### 硬件要求

| 部署规模 | CPU 核心 | 内存       | 磁盘空间 | 网络带宽 |
| -------- | -------- | ---------- | -------- | -------- |
| 小型部署 | 2-4 核   | 4GB RAM    | 100GB+   | 100Mbps  |
| 中型部署 | 4-8 核   | 8-16GB RAM | 500GB+   | 1Gbps    |
| 大型部署 | 8+ 核    | 16GB+ RAM  | 1TB+     | 10Gbps   |

### 权限要求

- **用户权限**: 需要 root 或 sudo 权限进行安装
- **磁盘空间说明**: 原始视频文件需要 3 倍空间（原始 + 转码 + 临时文件）

------

## 二、核心编程环境

### Python 环境

- **Python 版本**: Python 3.8+（推荐 Python 3.11 或 3.13）
- **包管理工具**:
  - `pip`: Python 包管理器
  - `virtualenv`: 虚拟环境管理
  - `uv`（可选）: 更快的 Python 包管理器

### Node.js 环境（前端编译）

- **Node.js**: 版本 >= 14.17.0（推荐 LTS 版本）
- **npm**: Node.js 包管理器
- **构建工具**: Webpack 5.x, Babel 7.x

------

## 三、数据库系统

### PostgreSQL

- **版本**: PostgreSQL 13+（推荐 PostgreSQL 15 或 16）

- **配置要求**:

  ```
  -- 创建数据库和用户
  CREATE DATABASE mediacms;
  CREATE USER mediacms WITH PASSWORD 'mediacms';
  GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;
  ```

- **认证方式**: scram-sha-256

- **性能优化**: 建议根据硬件配置调整 `shared_buffers`, `work_mem`等参数

### Redis

- **用途**:
  - Celery 消息代理和结果后端
  - Django 缓存存储
  - Session 存储
- **版本**: Redis 6.0+
- **默认端口**: 6379
- **内存配置**: 建议分配 1GB+ 内存

------

## 四、Web 服务器

### Nginx

- **版本**: Nginx 1.18+
- **主要功能**:
  - 反向代理和负载均衡
  - 静态文件服务
  - SSL/TLS 终止
  - Gzip 压缩
- **配置文件位置**: `/etc/nginx/`
- **关键配置文件**:
  - `nginx.conf`: 主配置文件
  - `sites-available/mediacms`: 站点配置
  - `uwsgi_params`: uWSGI 参数

### uWSGI 应用服务器

- **版本**: uWSGI 2.0.28+

- **配置参数**:

  ```
  [uwsgi]
  socket = 127.0.0.1:9000
  processes = 2
  threads = 2
  buffer-size = 65535
  ```

- **进程管理**: 支持优雅重启和日志轮转

------

## 五、视频处理工具

### FFmpeg（核心依赖）

- **版本**: 最新静态编译版本（推荐）
- **下载地址**: https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
- **包含组件**:
  - `ffmpeg`: 视频转码和处理
  - `ffprobe`: 媒体文件分析
  - `ffplay`: 媒体播放测试
  - `qt-faststart`: MP4 文件优化
- **支持编码格式**:
  - 视频: H.264, H.265/HEVC, VP9, AV1
  - 音频: AAC, MP3, Opus, Vorbis
- **转码分辨率**: 144p, 240p, 360p, 480p, 720p, 1080p, 4K

### Bento4

- **版本**: 1.6.0-637+
- **下载地址**: http://zebulon.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-637.x86_64-unknown-linux.zip
- **核心工具**: `mp4hls`, `mp4fragment`, `mp4dash`
- **主要功能**:
  - MP4 文件分片和分段
  - HLS（HTTP Live Streaming）生成
  - DASH（Dynamic Adaptive Streaming）支持
  - DRM 加密支持

------

## 六、图像处理工具

### ImageMagick

- **版本**: ImageMagick 6.9+ 或 7.x

- **主要功能**:

  - 图片格式转换和优化
  - 缩略图生成
  - 视频预览图（sprite）创建
  - 图片水印处理

- **重要配置**（`/etc/ImageMagick-6/policy.xml`）:

  ```
  <!-- 允许处理大文件 -->
  <policy domain="resource" name="memory" value="2GiB"/>
  <policy domain="resource" name="width" value="32KP"/>
  <policy domain="resource" name="height" value="32KP"/>
  ```

------

## 七、系统依赖包

### Ubuntu/Debian 系统包

```
# 基础系统工具
sudo apt-get install -y build-essential pkg-config gcc g++ git
sudo apt-get install -y vim nano unzip wget curl xz-utils

# Python 开发环境
sudo apt-get install -y python3-dev python3-venv python3-pip virtualenv

# 数据库和缓存客户端
sudo apt-get install -y libpq-dev zlib1g-dev

# XML 处理（SAML 认证需要）
sudo apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl

# 进程管理
sudo apt-get install -y supervisor procps

# 图像处理依赖
sudo apt-get install -y libmagickwand-dev libjpeg-dev libpng-dev
```

### RHEL/CentOS 系统包

```
# 基础工具
sudo yum install -y gcc gcc-c++ make git vim nano unzip wget curl
sudo yum install -y python3-devel python3-pip libpq-devel zlib-devel
sudo yum install -y libxml2-devel xmlsec1-devel xmlsec1-openssl-devel
sudo yum install -y supervisor procps-ng
```

------

## 八、Python 包依赖

### 核心依赖（requirements.txt）

```
# Web 框架
Django==5.2.6
djangorestframework==3.16.1
drf-yasg==1.21.8

# 数据库
psycopg[binary,pool]==3.2.4

# 缓存和会话
django-redis==5.4.0
redis==5.0.1

# 任务队列
celery==5.4.0
django-celery-email==3.0.0

# 认证和授权
python3-saml==1.16.0
django-allauth==65.4.1

# 应用服务器
uwsgi==2.0.28

# 图像处理
Pillow==11.1.0
django-imagekit==5.0.0

# 实用工具
markdown==3.7
django-filter==24.3
filetype==1.2.0
django-mptt==0.16.0
crispy-bootstrap5==2024.10
requests==2.32.3
m3u8==6.0.0
pysubs2==1.8.0

# 管理界面
django-jazzmin==3.0.1
django-tinymce==4.1.0

# 开发工具
django-debug-toolbar==5.0.1
pre-commit==4.1.0

# 监控
sentry-sdk[django]==2.23.1
```

### 扩展功能依赖（requirements-full.txt）

```
# AI 字幕转录
openai-whisper==20250625
setuptools-rust

# 机器学习扩展
torch>=2.0.0
torchaudio>=2.0.0

# 其他媒体处理
moviepy==1.0.3
opencv-python==4.10.0.84
```

------

## 九、前端依赖（package.json）

### 核心框架

```
{
  "react": "^17.0.2",
  "react-dom": "^17.0.2",
  "react-router-dom": "^5.3.4"
}
```

### 构建工具

```
{
  "webpack": "^5.98.0",
  "babel-core": "^7.26.0",
  "typescript": "^5.8.2",
  "sass": "^1.85.1",
  "postcss": "^8.5.2"
}
```

### 功能库

```
{
  "axios": "^1.8.2",
  "flux": "^4.0.4",
  "video.js": "^8.15.1",
  "pdfjs-dist": "^3.4.120",
  "sortablejs": "^1.13.0",
  "moment": "^2.29.4"
}
```

### 开发依赖

```
{
  "webpack-cli": "^5.1.4",
  "babel-loader": "^9.2.1",
  "css-loader": "^7.1.2",
  "style-loader": "^4.0.0"
}
```

------

## 十、异步任务系统（Celery）

### Celery 工作进程配置

| 服务名称     | Worker 数量 | 并发数 | 任务超时 | 队列类型 |
| ------------ | ----------- | ------ | -------- | -------- |
| celery_short | 2           | 10     | 300秒    | 短任务   |
| celery_long  | 1           | 2      | 无限制   | 长任务   |
| celery_beat  | 1           | 1      | -        | 定时任务 |

### 任务类型分类

- **短任务队列**（celery_short）:
  - 缩略图生成
  - 邮件发送
  - 文件清理
  - 用户通知
- **长任务队列**（celery_long）:
  - 视频转码
  - HLS 切片
  - AI 字幕转录
  - 批量处理

### 消息队列配置

```
# Broker 配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# 队列路由
CELERY_TASK_ROUTES = {
    'mediacms.tasks.encode_video': {'queue': 'long'},
    'mediacms.tasks.generate_thumbnails': {'queue': 'short'},
}
```

------

## 十一、SSL/TLS 安全配置

### Certbot（Let's Encrypt）

```
# 安装 Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d yourdomain.com

# 自动续期测试
sudo certbot renew --dry-run
```

### OpenSSL 配置

```
# 生成 DH 参数（增强安全性）
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096

# 生成自签名证书（测试环境）
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt
```

### 安全头配置

```
# 安全头部配置
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
```

------

## 十二、进程管理服务（systemd）

### 服务文件配置

**1. mediacms.service**（主应用服务）

```
[Unit]
Description=MediaCMS uWSGI Application
After=network.target postgresql.service redis-server.service

[Service]
User=mediacms
Group=mediacms
WorkingDirectory=/home/mediacms.io/mediacms
Environment=PATH=/home/mediacms.io/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/mediacms.io/bin/uwsgi --ini uwsgi.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

**2. celery_short.service**（短任务队列）

```
[Unit]
Description=MediaCMS Celery Short Tasks Worker
After=network.target redis-server.service

[Service]
User=mediacms
Group=mediacms
WorkingDirectory=/home/mediacms.io/mediacms
Environment=PATH=/home/mediacms.io/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/mediacms.io/bin/celery -A mediacms worker --loglevel=info -Q short -c 10 -n short.%%h
Restart=always

[Install]
WantedBy=multi-user.target
```

**3. celery_long.service**（长任务队列）

```
[Unit]
Description=MediaCMS Celery Long Tasks Worker
After=network.target redis-server.service

[Service]
User=mediacms
Group=mediacms
WorkingDirectory=/home/mediacms.io/mediacms
Environment=PATH=/home/mediacms.io/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/mediacms.io/bin/celery -A mediacms worker --loglevel=info -Q long -c 2 -n long.%%h
Restart=always

[Install]
WantedBy=multi-user.target
```

**4. celery_beat.service**（定时任务调度器）

```
[Unit]
Description=MediaCMS Celery Beat Scheduler
After=network.target redis-server.service

[Service]
User=mediacms
Group=mediacms
WorkingDirectory=/home/mediacms.io/mediacms
Environment=PATH=/home/mediacms.io/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/mediacms.io/bin/celery -A mediacms beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
Restart=always

[Install]
WantedBy=multi-user.target
```

------

## 十三、目录结构规范

```
/home/mediacms.io/
├── bin/                    # Python 虚拟环境
├── mediacms/              # 项目主目录
│   ├── media_files/       # 媒体文件存储
│   │   ├── original/      # 原始上传文件
│   │   ├── encoded/       # 转码后文件
│   │   ├── hls/           # HLS 流文件
│   │   └── thumbnails/    # 缩略图文件
│   ├── static/            # 静态文件（CSS, JS, 图片）
│   ├── media/             # 用户上传的静态文件
│   ├── logs/              # 应用日志
│   │   ├── uwsgi.log
│   │   ├── celery.log
│   │   └── nginx/
│   └── pids/              # PID 文件
├── bento4/                # Bento4 工具集
│   ├── bin/
│   └── lib/
├── ffmpeg/                # FFmpeg 静态二进制文件
└── backups/               # 数据库备份
```

### 目录权限设置

```
# 创建 mediacms 用户
sudo useradd -r -s /bin/bash -d /home/mediacms.io mediacms

# 设置目录权限
sudo chown -R mediacms:mediacms /home/mediacms.io
sudo chmod 755 /home/mediacms.io
sudo chmod -R 755 /home/mediacms.io/mediacms/media_files/
```

------

## 十四、网络端口配置

### 必需开放端口

| 端口 | 协议 | 服务           | 访问控制 |
| ---- | ---- | -------------- | -------- |
| 80   | TCP  | HTTP（Nginx）  | 公网访问 |
| 443  | TCP  | HTTPS（Nginx） | 公网访问 |
| 9000 | TCP  | uWSGI（内部）  | 本地访问 |
| 5432 | TCP  | PostgreSQL     | 本地访问 |
| 6379 | TCP  | Redis          | 本地访问 |

### 防火墙配置示例

```
# UFW（Ubuntu）
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# firewalld（RHEL/CentOS）
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

------

## 十五、环境变量配置

### 核心配置（cms/local_settings.py）

```
import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_HOST = os.getenv('FRONTEND_HOST', 'https://yourdomain.com')
PORTAL_NAME = os.getenv('PORTAL_NAME', 'MediaCMS Portal')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'mediacms'),
        'USER': os.getenv('DB_USER', 'mediacms'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mediacms'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Redis 配置
REDIS_LOCATION = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery 配置
CELERY_BROKER_URL = REDIS_LOCATION
CELERY_RESULT_BACKEND = REDIS_LOCATION

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 邮件配置（可选）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
```

### 环境变量文件（.env）

```
# 应用配置
FRONTEND_HOST=https://yourdomain.com
PORTAL_NAME="My Media Portal"
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# 数据库
DB_NAME=mediacms
DB_USER=mediacms
DB_PASSWORD=strong-password-here
DB_HOST=127.0.0.1
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# 邮件服务
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

------

## 十六、可选功能依赖

### SAML 单点登录

```
# 系统依赖
sudo apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl

# Python 包
python3-saml==1.16.0
```

### AI 字幕转录（Whisper）

```
# 系统依赖（语音处理）
sudo apt-get install -y ffmpeg sox

# Python 包（需要较多磁盘空间）
openai-whisper>=20250625
setuptools-rust
torch>=2.0.0
```

### 监控和日志

```
# 系统监控
sudo apt-get install -y htop iotop nethogs

# 日志管理
sudo apt-get install -y logrotate
```

### 备份工具

```
# 数据库备份
sudo apt-get install -y postgresql-client bzip2

# 文件同步
sudo apt-get install -y rsync
```

------

## 十七、安装步骤摘要

### 完整安装脚本

```
#!/bin/bash
set -e

echo "开始安装 MediaCMS..."

# 1. 系统更新和基础包
apt-get update && apt-get upgrade -y
apt-get install -y curl wget gnupg lsb-release

# 2. 安装系统依赖
apt-get install -y build-essential pkg-config gcc g++ git vim nano \
    unzip wget curl xz-utils python3-dev python3-venv python3-pip \
    virtualenv libpq-dev zlib1g-dev libxml2-dev libxmlsec1-dev \
    libxmlsec1-openssl supervisor procps libmagickwand-dev \
    libjpeg-dev libpng-dev

# 3. 安装 PostgreSQL
apt-get install -y postgresql postgresql-contrib
systemctl enable postgresql --now

# 4. 安装 Redis
apt-get install -y redis-server
systemctl enable redis-server --now

# 5. 安装 Nginx
apt-get install -y nginx
systemctl enable nginx --now

# 6. 安装 FFmpeg
cd /tmp
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xf ffmpeg-release-amd64-static.tar.xz
cp ffmpeg-*-static/ffmpeg /usr/local/bin/
cp ffmpeg-*-static/ffprobe /usr/local/bin/
chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe

# 7. 安装 Bento4
wget http://zebulon.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-637.x86_64-unknown-linux.zip
unzip Bento4-SDK-1-6-0-637.x86_64-unknown-linux.zip -d /home/mediacms.io/bento4
ln -s /home/mediacms.io/bento4/bin/* /usr/local/bin/

# 8. 创建系统用户和目录
useradd -r -s /bin/bash -d /home/mediacms.io mediacms
mkdir -p /home/mediacms.io/{mediacms,backups,logs}
chown -R mediacms:mediacms /home/mediacms.io

# 9. 配置 PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE mediacms;
CREATE USER mediacms WITH PASSWORD 'mediacms';
GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;
ALTER USER mediacms CREATEDB;
EOF

# 10. 创建 Python 虚拟环境
sudo -u mediacms python3 -m venv /home/mediacms.io/venv

# 11. 安装 Python 依赖
sudo -u mediacms /home/mediacms.io/venv/bin/pip install -U pip
sudo -u mediacms /home/mediacms.io/venv/bin/pip install -r /path/to/requirements.txt

# 12. 安装 Node.js（如需要前端编译）
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# 13. 克隆 MediaCMS 代码
sudo -u mediacms git clone https://github.com/mediacms-io/mediacms.git /home/mediacms.io/mediacms

# 14. 应用配置和数据库迁移
cd /home/mediacms.io/mediacms
sudo -u mediacms /home/mediacms.io/venv/bin/python manage.py migrate
sudo -u mediacms /home/mediacms.io/venv/bin/python manage.py loaddata fixtures/encoding_profiles.json
sudo -u mediacms /home/mediacms.io/venv/bin/python manage.py loaddata fixtures/categories.json
sudo -u mediacms /home/mediacms.io/venv/bin/python manage.py collectstatic --noinput

# 15. 配置 systemd 服务
cp deploy/local_install/*.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable mediacms celery_short celery_long celery_beat

# 16. 配置 Nginx
cp deploy/local_install/nginx.conf /etc/nginx/sites-available/mediacms
ln -s /etc/nginx/sites-available/mediacms /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 17. 启动所有服务
systemctl start mediacms celery_short celery_long celery_beat

echo "MediaCMS 安装完成！"
```

### 安装后检查清单

-  PostgreSQL 数据库连接正常
-  Redis 服务运行正常
-  Nginx 配置语法正确
-  uWSGI 应用服务启动
-  Celery Worker 进程运行
-  静态文件收集完成
-  媒体文件目录权限正确
-  SSL 证书配置（如使用 HTTPS）

------

## 总结

手动部署 MediaCMS 是一个复杂但可控的过程，主要包含以下组件：

### 🏗️ 架构组件

- **7个核心服务**：PostgreSQL, Redis, Nginx, uWSGI, 3个Celery Worker
- **2个媒体工具**：FFmpeg（视频处理）, Bento4（流媒体）
- **1个图像工具**：ImageMagick

### 📦 软件依赖

- **25+ Python 包**：Django 生态和媒体处理库
- **40+ Node.js 包**：React 前端框架和构建工具
- **15+ 系统依赖包**：开发工具和系统库

### 🔧 配置复杂度

- **高**：需要手动配置多个服务和组件
- **建议**：初次部署推荐使用 Docker 简化流程
- **优势**：手动部署提供更好的性能调优和自定义能力

### ⚡ 性能优化建议

1. 根据硬件配置调整 PostgreSQL 和 Redis 参数
2. 配置合适的 Celery Worker 数量和并发数
3. 使用 CDN 加速静态文件和媒体流
4. 启用 Nginx 缓存和 Gzip 压缩
5. 定期清理临时文件和日志

此清单为生产环境部署提供了完整的参考，实际部署时请根据具体需求和环境进行调整。
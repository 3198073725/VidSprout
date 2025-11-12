# MediaCMS Windows 本地开发环境搭建计划

## 📋 总体目标
在 Windows 电脑上搭建完整的开发环境，进行前后端联调，然后准备部署到服务器。

---

## 🎯 阶段一：环境准备（预计时间：1-2小时）

### 1.1 安装必要软件

#### ✅ Python 环境
- **下载安装**：Python 3.11+ 或 3.13
  - 下载地址：https://www.python.org/downloads/
  - ✅ 勾选 "Add Python to PATH"
  - ✅ 验证安装：`python --version` 和 `pip --version`

#### ✅ Node.js 环境
- **下载安装**：Node.js 20.19.0+ 或 22.12.0+
  - 下载地址：https://nodejs.org/
  - ✅ 选择 LTS 版本
  - ✅ 验证安装：`node --version` 和 `npm --version`

#### ✅ Git
- **下载安装**：Git for Windows
  - 下载地址：https://git-scm.com/download/win
  - ✅ 验证安装：`git --version`

#### ✅ PostgreSQL 数据库
- **下载安装**：PostgreSQL 15+ 或 17
  - 下载地址：https://www.postgresql.org/download/windows/
  - ✅ 记住设置的 postgres 用户密码
  - ✅ 默认端口：5432
  - ✅ 安装 PostgreSQL 客户端工具（pgAdmin）

#### ✅ Redis
- **方式一（推荐）**：使用 WSL2 安装 Redis
  ```bash
  wsl --install
  # 在 WSL 中安装 Redis
  sudo apt update
  sudo apt install redis-server
  sudo service redis-server start
  ```

- **方式二**：使用 Memurai（Windows 原生 Redis）
  - 下载地址：https://www.memurai.com/get-memurai
  - ✅ 免费版即可
  - ✅ 默认端口：6379

#### ✅ FFmpeg（视频处理）
- **下载安装**：FFmpeg Windows 版本
  - 下载地址：https://www.gyan.dev/ffmpeg/builds/
  - ✅ 下载 `ffmpeg-release-essentials.zip`
  - ✅ 解压到 `C:\ffmpeg\`
  - ✅ 添加到系统 PATH：`C:\ffmpeg\bin`
  - ✅ 验证：`ffmpeg -version`

#### ✅ ImageMagick（图像处理）
- **下载安装**：ImageMagick for Windows
  - 下载地址：https://imagemagick.org/script/download.php#windows
  - ✅ 选择安装路径：`C:\Program Files\ImageMagick-7.x.x-Q16-HDRI`
  - ✅ 添加到系统 PATH
  - ✅ 验证：`magick -version`

### 1.2 验证环境
```powershell
# 打开 PowerShell，验证所有工具
python --version
pip --version
node --version
npm --version
git --version
psql --version
ffmpeg -version
magick -version
```

---

## 🔧 阶段二：数据库和服务配置（预计时间：30分钟）

### 2.1 配置 PostgreSQL

#### 方法一：使用 pgAdmin 图形界面（推荐，最简单）

1. **打开 pgAdmin**
   - 在开始菜单搜索 "pgAdmin 4" 并打开
   - 首次打开需要设置主密码（用于保护保存的密码）

2. **连接到 PostgreSQL 服务器**
   - 左侧面板，右键点击 "Servers" → "Create" → "Server"
   - General 标签页：
     - Name: `Local PostgreSQL`（任意名称）
   - Connection 标签页：
     - Host name/address: `localhost`
     - Port: `5432`
     - Username: `postgres`
     - Password: 输入安装 PostgreSQL 时设置的密码
   - 点击 "Save"

3. **创建数据库**
   - 展开服务器 → 右键点击 "Databases" → "Create" → "Database"
   - Database: `mediacms`
   - Owner: `postgres`
   - 点击 "Save"

4. **创建用户并设置权限**
   - 展开服务器 → 展开 "Login/Group Roles"
   - 右键点击 "Login/Group Roles" → "Create" → "Login/Group Role"
   - General 标签页：
     - Name: `mediacms`
   - Definition 标签页：
     - Password: `mediacms`
   - Privileges 标签页：
     - ✅ Can login? 勾选
     - ✅ Create databases? 勾选（可选）
   - 点击 "Save"

5. **授予数据库权限**
   - 展开 "Databases" → 右键点击 `mediacms` → "Query Tool"
   - 在查询编辑器中输入以下 SQL：
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;
   ALTER ROLE mediacms SET client_encoding TO 'utf8';
   ALTER ROLE mediacms SET default_transaction_isolation TO 'read committed';
   ALTER ROLE mediacms SET timezone TO 'UTC';
   ```
   - 点击 "Execute" (F5) 执行

#### 方法二：使用命令行（如果方法一失败）

**步骤 1：检查 PostgreSQL 服务是否运行**
```powershell
# 打开 PowerShell 或 CMD
# 检查 PostgreSQL 服务状态
sc query postgresql-x64-*
# 或使用服务管理器：services.msc，查找 postgresql 服务
```

**步骤 2：使用 psql 连接（需要密码）**
```powershell
# 方式 A：直接连接（会提示输入密码）
psql -U postgres -h localhost

# 方式 B：使用环境变量（避免交互式输入）
$env:PGPASSWORD='your_postgres_password'
psql -U postgres -h localhost

# 方式 C：使用 PostgreSQL bin 目录的完整路径
# 通常在：C:\Program Files\PostgreSQL\15\bin\psql.exe
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
```

**步骤 3：创建 SQL 脚本文件（推荐）**

创建文件 `setup-database.sql`：
```sql
-- 创建数据库
CREATE DATABASE mediacms;

-- 创建用户
CREATE USER mediacms WITH PASSWORD 'mediacms';

-- 设置编码和时区
ALTER ROLE mediacms SET client_encoding TO 'utf8';
ALTER ROLE mediacms SET default_transaction_isolation TO 'read committed';
ALTER ROLE mediacms SET timezone TO 'UTC';

-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;

-- 连接到新数据库并授予 schema 权限
\c mediacms
GRANT ALL ON SCHEMA public TO mediacms;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mediacms;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mediacms;
```

**步骤 4：执行 SQL 脚本**
```powershell
# 使用密码环境变量
$env:PGPASSWORD='your_postgres_password'
psql -U postgres -h localhost -f setup-database.sql

# 或交互式输入密码
psql -U postgres -h localhost -f setup-database.sql
```

**步骤 5：验证配置**
```powershell
# 测试连接到新数据库
psql -U mediacms -d mediacms -h localhost
# 输入密码：mediacms
# 如果成功，会显示：mediacms=>
# 输入 \q 退出
```

#### 方法三：一键创建脚本（最简单）

创建文件 `setup-postgres.bat`：
```batch
@echo off
echo ========================================
echo MediaCMS PostgreSQL 数据库配置脚本
echo ========================================
echo.

set PGPASSWORD=
set /p PGPASSWORD="请输入 postgres 用户密码: "

echo.
echo [创建] 正在创建数据库和用户...
echo.

psql -U postgres -h localhost -c "CREATE DATABASE mediacms;" 2>nul
if errorlevel 1 (
    echo [检查] 数据库可能已存在，继续...
)

psql -U postgres -h localhost -c "CREATE USER mediacms WITH PASSWORD 'mediacms';" 2>nul
if errorlevel 1 (
    echo [检查] 用户可能已存在，继续...
)

psql -U postgres -h localhost -c "ALTER ROLE mediacms SET client_encoding TO 'utf8';" 2>nul
psql -U postgres -h localhost -c "ALTER ROLE mediacms SET default_transaction_isolation TO 'read committed';" 2>nul
psql -U postgres -h localhost -c "ALTER ROLE mediacms SET timezone TO 'UTC';" 2>nul
psql -U postgres -h localhost -c "GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;" 2>nul

echo.
echo [验证] 测试数据库连接...
psql -U mediacms -d mediacms -h localhost -c "SELECT version();" 2>nul
if errorlevel 1 (
    echo [错误] 无法连接到数据库，请检查配置
) else (
    echo [成功] 数据库配置完成！
)
echo.
pause
```

#### 常见问题排查

**问题 1：psql 命令未找到**
```powershell
# 解决方法：添加到系统 PATH
# PostgreSQL bin 目录通常在：
# C:\Program Files\PostgreSQL\15\bin
# 或
# C:\Program Files\PostgreSQL\17\bin

# 临时添加到当前会话：
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"

# 永久添加：系统属性 → 环境变量 → Path → 添加 PostgreSQL bin 目录
```

**问题 2：密码认证失败（用户 mediacms Password 认证失败）**

这是最常见的问题，解决方法：

**方法 A：使用密码重置脚本（推荐）**
```powershell
# 运行我创建的密码重置脚本
.\fix-postgres-password.bat
# 脚本会自动检查并修复用户和密码问题
```

**方法 B：手动重置密码**
```powershell
# 1. 使用 postgres 用户连接
$env:PGPASSWORD='your_postgres_password'
psql -U postgres -h localhost

# 2. 在 psql 中执行以下命令
ALTER USER mediacms WITH PASSWORD 'mediacms';
# 或如果用户不存在，创建用户：
CREATE USER mediacms WITH PASSWORD 'mediacms';

# 3. 退出 psql
\q
```

**方法 C：检查并修复 pg_hba.conf 配置**
```powershell
# 1. 找到 pg_hba.conf 文件
# 位置通常在：C:\Program Files\PostgreSQL\15\data\pg_hba.conf
# 或：C:\Program Files\PostgreSQL\17\data\pg_hba.conf

# 2. 编辑文件，确保 local 连接使用正确的认证方式：
# 找到类似这样的行：
#   local   all             all                                     peer
# 或
#   local   all             all                                     ident
# 
# 修改为：
#   local   all             all                                     md5
# 或
#   local   all             all                                     scram-sha-256

# 3. 保存文件后，重启 PostgreSQL 服务
# 方法：services.msc → 找到 postgresql-x64-xx → 右键重启
```

**方法 D：使用 pgAdmin 重置密码**
1. 打开 pgAdmin
2. 连接到服务器
3. 展开 "Login/Group Roles"
4. 右键点击 `mediacms` → "Properties"
5. 在 "Definition" 标签页修改密码
6. 点击 "Save"

**问题 3：无法连接到服务器**
```powershell
# 检查 PostgreSQL 服务是否运行
services.msc
# 查找 postgresql-x64-xx 服务，确保状态为"正在运行"

# 或使用命令行
sc query postgresql-x64-*
```

**问题 4：权限不足**
```sql
-- 如果 postgres 用户无法创建数据库，检查：
-- 1. 是否以 postgres 用户登录
-- 2. 检查 pg_hba.conf 配置
-- 3. 尝试使用超级用户权限
```

#### 验证数据库连接
```powershell
# 方式 1：使用 psql
psql -U mediacms -d mediacms -h localhost
# 输入密码：mediacms
# 如果成功连接，输入 \q 退出

# 方式 2：使用 Python 测试（需要先安装 psycopg）
python -c "import psycopg2; conn = psycopg2.connect(dbname='mediacms', user='mediacms', password='mediacms', host='localhost'); print('连接成功！'); conn.close()"
```

### 2.2 配置 Redis

#### 如果使用 WSL2 Redis
```bash
# 在 WSL 中
sudo service redis-server start
redis-cli ping  # 应该返回 PONG
```

#### 如果使用 Memurai
- ✅ 启动 Memurai 服务（通常在系统托盘）
- ✅ 验证：`redis-cli ping`（需要先安装 Redis CLI）

---

## 🐍 阶段三：Python 后端环境（预计时间：30分钟）

### 3.1 创建 Python 虚拟环境

```powershell
# 进入项目目录
cd "E:\Graduation Project\cs001\mediacms"

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 如果 PowerShell 执行策略限制，先运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3.2 安装 Python 依赖

```powershell
# 确保虚拟环境已激活（提示符前应该有 (venv)）
# 升级 pip
python -m pip install --upgrade pip

# ⚠️ Windows 用户注意：使用 Windows 专用 requirements 文件
# requirements.txt 中包含 uwsgi，但 uwsgi 不支持 Windows
# 开发环境不需要 uwsgi（生产环境部署时才需要）

# 方式 A：使用 Windows 专用 requirements（推荐）
pip install -r requirements-windows.txt

# 方式 B：如果使用 requirements.txt，需要先排除 uwsgi
pip install -r requirements.txt --ignore-installed uwsgi

# 方式 C：手动安装（如果上述方法失败）
pip install Django==5.2.6
pip install djangorestframework==3.16.1
pip install django-allauth==65.4.1
pip install psycopg[binary,pool]==3.2.4
pip install django-redis==5.4.0
pip install celery==5.4.0
pip install drf-yasg==1.21.8
pip install Pillow==11.1.0
pip install django-imagekit==5.0.0
pip install markdown==3.7
pip install django-filter==24.3
pip install filetype==1.2.0
pip install django-mptt==0.16.0
pip install crispy-bootstrap5==2024.10
pip install requests==2.32.3
pip install django-celery-email==3.0.0
pip install m3u8==6.0.0
pip install django-debug-toolbar==5.0.1
pip install django-jazzmin==3.0.1
pip install pysubs2==1.8.0
pip install sentry-sdk[django]==2.23.1
pip install django-tinymce==4.1.0
pip install django-cors-headers==4.7.0

# 如果安装 psycopg 失败，可能需要先安装：
# pip install psycopg-binary
# 或使用国内镜像加速：
# pip install psycopg[binary,pool]==3.2.4 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果安装 python3-saml 失败（Windows 上可能需要额外依赖），可以暂时跳过：
# pip install python3-saml==1.16.0
# 如果失败，SAML 功能将不可用，但不影响基本功能
```

### 3.3 创建本地配置文件

```powershell
# 创建 local_settings.py
# 位置：cms/local_settings.py
```

创建文件 `cms/local_settings.py`：
```python
import os

# 基础配置
DEBUG = True
FRONTEND_HOST = "http://localhost:8080"  # Vue 前端地址
PORTAL_NAME = "MediaCMS 本地开发"

# 数据库配置（Windows 本地）
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mediacms",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "USER": "mediacms",
        "PASSWORD": "mediacms",
        "OPTIONS": {'pool': True},
    }
}

# Redis 配置（Windows 本地）
REDIS_LOCATION = "redis://127.0.0.1:6379/1"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery 配置
BROKER_URL = REDIS_LOCATION
CELERY_RESULT_BACKEND = BROKER_URL

# FFmpeg 路径（Windows）
FFMPEG_COMMAND = "ffmpeg"
FFPROBE_COMMAND = "ffprobe"

# 媒体文件路径（Windows 兼容）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, "media_files").replace("\\", "/")
STATIC_ROOT = os.path.join(BASE_DIR, "static").replace("\\", "/")

# 允许所有主机（开发环境）
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

# CORS 配置（允许 Vue 前端访问）
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True

# 邮件配置（开发环境，使用控制台输出）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 3.4 数据库迁移

```powershell
# 确保虚拟环境已激活，Redis 和 PostgreSQL 已启动

# 运行数据库迁移
python manage.py migrate

# 加载初始数据
python manage.py loaddata fixtures/encoding_profiles.json
python manage.py loaddata fixtures/categories.json

# 创建超级用户（管理员账号）
python manage.py createsuperuser
# 输入用户名、邮箱、密码
```

### 3.5 收集静态文件

```powershell
python manage.py collectstatic --noinput
```

---

## 🎨 阶段四：Vue 前端环境（预计时间：20分钟）

### 4.1 安装前端依赖

```powershell
# 进入 Vue 前端目录
cd frontend-vue

# 安装依赖（可能需要几分钟）
npm install

# 如果安装失败，尝试：
npm install --legacy-peer-deps
```

### 4.2 配置前端环境变量 ⚠️ **重要：必须创建**

**方式一：使用脚本自动创建（推荐）**
```powershell
# 运行脚本自动创建环境变量文件
.\create-frontend-env.bat
```

**方式二：手动创建**

创建文件 `frontend-vue/.env.development`：
```bash
# API 基础地址
VITE_API_BASE=http://localhost:8000/api

# 是否使用 CSRF
VITE_USE_CSRF=false

# Token 相关配置
VITE_ACCESS_HEADER=Authorization
VITE_ACCESS_PREFIX=Bearer

# Token 刷新端点
VITE_REFRESH_ENDPOINT=http://localhost:8000/api/v1/auth/refresh

# 前端地址（用于生成完整 URL）
VITE_FRONTEND_URL=http://localhost:8080

# 后端地址（用于直接 API 调用）
VITE_BACKEND_URL=http://localhost:8000
```

**注意：** 此文件是前端运行的关键配置文件，如果缺失会导致前端无法正常连接后端 API。

### 4.3 验证前端配置

```powershell
# 检查 vite.config.ts 中的代理配置是否正确
# 应该代理到 http://localhost:8000
```

---

## 🚀 阶段五：启动服务（预计时间：10分钟）

### 5.1 启动 Redis
```bash
# WSL 方式
wsl
sudo service redis-server start
exit

# 或 Memurai（自动启动）
```

### 5.2 启动 Celery Worker（新终端）

```powershell
# 激活虚拟环境
cd "E:\Graduation Project\cs001\mediacms"
.\venv\Scripts\Activate.ps1

# 启动 Celery Worker（短任务）
celery -A cms worker --loglevel=info -Q short_tasks -n short@%h

# 新终端启动 Celery Worker（长任务）
celery -A cms worker --loglevel=info -Q long_tasks -n long@%h

# 新终端启动 Celery Beat（定时任务）
celery -A cms beat --loglevel=info
```

### 5.3 启动 Django 后端（新终端）

```powershell
# 激活虚拟环境
cd "E:\Graduation Project\cs001\mediacms"
.\venv\Scripts\Activate.ps1

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000

# 访问 http://localhost:8000/admin 查看管理后台
```

### 5.4 启动 Vue 前端（新终端）

```powershell
# 进入前端目录
cd "E:\Graduation Project\cs001\mediacms\frontend-vue"

# 启动开发服务器
npm run dev

# 访问 http://localhost:8080
```

---

## ✅ 阶段六：验证测试（预计时间：30分钟）

### 6.1 验证后端服务

- [ ] 访问 `http://localhost:8000/admin`，使用超级用户登录
- [ ] 访问 `http://localhost:8000/api/v1/` 查看 API 文档
- [ ] 检查数据库连接正常
- [ ] 检查 Redis 连接正常

### 6.2 验证前端服务

- [ ] 访问 `http://localhost:8080`，查看首页
- [ ] 测试登录功能
- [ ] 测试注册功能
- [ ] 测试上传媒体功能
- [ ] 测试视频播放功能

### 6.3 检查控制台日志

- [ ] Django 控制台无错误
- [ ] Celery Worker 正常运行
- [ ] Vue 前端无编译错误
- [ ] 浏览器控制台无报错

---

## 🔍 常见问题排查

### 问题 1：PostgreSQL 连接失败
```powershell
# 检查 PostgreSQL 服务是否启动
# Windows 服务管理器：services.msc
# 查找 "postgresql-x64-xx" 服务，确保正在运行

# 检查防火墙是否阻止
# 检查端口 5432 是否被占用
netstat -ano | findstr :5432
```

### 问题 2：Redis 连接失败
```powershell
# 检查 Redis 是否运行
redis-cli ping

# 如果使用 WSL，确保 WSL 已启动
wsl --status
```

### 问题 3：FFmpeg 未找到
```powershell
# 检查 FFmpeg 是否在 PATH 中
ffmpeg -version

# 如果失败，手动添加到 PATH
# 系统属性 -> 环境变量 -> PATH -> 添加 C:\ffmpeg\bin
```

### 问题 4：Python 依赖安装失败

**错误：uwsgi 安装失败（Windows 不支持）**
```powershell
# 解决方法：使用 Windows 专用 requirements 文件
pip install -r requirements-windows.txt

# 或跳过 uwsgi 安装
pip install -r requirements.txt --ignore-installed uwsgi
```

**错误：psycopg 安装失败**
```powershell
# 解决方法 1：使用预编译的二进制版本
pip install psycopg-binary

# 解决方法 2：使用国内镜像
pip install psycopg[binary,pool]==3.2.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**错误：python3-saml 安装失败**
```powershell
# 解决方法 1：安装系统依赖（如果使用 WSL）
# 在 WSL 中：sudo apt-get install libxml2-dev libxmlsec1-dev

# 解决方法 2：暂时跳过（不影响基本功能）
pip install -r requirements-windows.txt --ignore-installed python3-saml

# 注意：跳过后 SAML 单点登录功能将不可用
```

**错误：其他依赖安装失败**
```powershell
# 尝试使用国内镜像加速
pip install -r requirements-windows.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或更新 pip
python -m pip install --upgrade pip

# 或逐个安装，找出问题包
pip install Django==5.2.6
pip install djangorestframework==3.16.1
# ... 逐个安装
```

### 问题 5：前端代理失败
```powershell
# 检查 vite.config.ts 中的代理配置
# 确保 target 指向正确的后端地址
# 检查后端是否在 8000 端口运行
```

---

## 📝 开发调试建议

### 日常开发流程

1. **启动顺序**：
   ```
   1. Redis 服务
   2. PostgreSQL 服务
   3. Celery Worker（2个终端）
   4. Celery Beat（1个终端）
   5. Django 后端（1个终端）
   6. Vue 前端（1个终端）
   ```

2. **调试技巧**：
   - 使用 Django Debug Toolbar（已安装）
   - 查看浏览器开发者工具（F12）
   - 查看 Celery 日志了解异步任务状态
   - 查看 Django 日志：`logs/debug.log`

3. **数据库管理**：
   - 使用 pgAdmin 图形界面
   - 或使用 Django Admin：`http://localhost:8000/admin`

---

## 🚢 阶段七：部署准备（预计时间：1小时）

### 7.1 构建前端生产版本

```powershell
cd frontend-vue

# 构建生产版本
npm run build

# 构建产物在 dist/ 目录
# 需要配置 Nginx 或集成到 Django 静态文件
```

### 7.2 准备部署配置

- [ ] 创建 `cms/local_settings_production.py`（生产环境配置）
- [ ] 修改 `DEBUG = False`
- [ ] 配置生产数据库
- [ ] 配置生产 Redis
- [ ] 配置 HTTPS 证书
- [ ] 配置域名和 ALLOWED_HOSTS

### 7.3 服务器部署检查清单

- [ ] 服务器已安装 Python 3.11+
- [ ] 服务器已安装 Node.js（如需要前端构建）
- [ ] 服务器已安装 PostgreSQL
- [ ] 服务器已安装 Redis
- [ ] 服务器已安装 FFmpeg
- [ ] 服务器已安装 Nginx（推荐）
- [ ] 服务器已配置防火墙规则
- [ ] 服务器已配置 SSL 证书（可选）

---

## 📊 时间估算总结

| 阶段 | 预计时间 | 实际时间 |
|------|---------|---------|
| 阶段一：环境准备 | 1-2小时 | |
| 阶段二：数据库配置 | 30分钟 | |
| 阶段三：Python 后端 | 30分钟 | |
| 阶段四：Vue 前端 | 20分钟 | |
| 阶段五：启动服务 | 10分钟 | |
| 阶段六：验证测试 | 30分钟 | |
| 阶段七：部署准备 | 1小时 | |
| **总计** | **4-5小时** | |

---

## 🎯 下一步行动

1. ✅ **立即开始**：阶段一（环境准备）
2. ⏳ **按顺序执行**：阶段二到阶段六
3. 🚀 **完成后**：阶段七（部署准备）

---

## 📚 参考文档

- [Django 官方文档](https://docs.djangoproject.com/)
- [Vue 3 官方文档](https://vuejs.org/)
- [PostgreSQL Windows 安装指南](https://www.postgresql.org/download/windows/)
- [Redis Windows 安装](https://redis.io/docs/getting-started/installation/install-redis-on-windows/)
- [FFmpeg Windows 安装](https://www.ffmpeg.org/download.html)

---

**祝你搭建顺利！如有问题，随时询问。** 🎉


# MediaCMS - 毕业设计项目

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](LICENSE.txt)

> 基于Django + Vue.js的现代化视频媒体内容管理系统
> 
> 本项目是一个功能完整的开源视频和媒体CMS系统，专为现代Web平台的媒体查看和分享需求而开发。

## 🎯 项目概述

MediaCMS是一个现代化的全功能开源视频和媒体内容管理系统，采用Django + Vue.js技术栈构建，包含完整的REST API接口。本项目在原版基础上进行了大量的中文本地化改进和功能优化。

### 🌟 主要特色

- **🏠 完全自主控制**: 私有化部署，数据完全掌控
- **🚀 现代技术栈**: Django/Python/Celery + Vue.js + PostgreSQL + Redis
- **🌍 中文本地化**: 完整的中文界面和用户体验
- **📱 响应式设计**: 支持桌面端和移动端访问
- **🔐 权限管理**: 基于角色的访问控制(RBAC)系统
- **🎬 多媒体支持**: 视频、音频、图片、PDF等多种格式
- **⚡ 高性能**: 异步任务处理和媒体转码
- **🔧 易于部署**: Docker容器化部署支持

## 📸 系统截图

<p align="center">
    <img src="docs/images/index.jpg" width="340" alt="首页">
    <img src="docs/images/video.jpg" width="340" alt="视频播放">
    <img src="docs/images/admin.jpg" width="340" alt="管理后台">
</p>

## ✨ 核心功能

### 🎥 媒体管理
- **多格式支持**: 视频(MP4, AVI, MOV等)、音频(MP3, WAV等)、图片(JPG, PNG等)、文档(PDF)
- **自动转码**: 支持多种分辨率和格式的自动转码
- **缩略图生成**: 自动生成视频缩略图和预览图
- **批量上传**: 支持多文件同时上传

### 👥 用户系统
- **用户注册/登录**: 支持邮箱验证和用户审核
- **个人资料**: 用户头像、简介、社交媒体链接
- **权限控制**: 管理员、普通用户等角色
- **活动追踪**: 用户行为记录和统计

### 🔍 内容发现
- **分类管理**: 灵活的分类和标签系统
- **搜索功能**: 全文搜索和高级筛选
- **推荐算法**: 基于内容和用户行为的推荐
- **热门内容**: 实时热门媒体排行

### 💬 互动功能
- **评论系统**: 支持嵌套回复和点赞
- **评分系统**: 用户评分和评价
- **分享功能**: 社交媒体分享和嵌入代码
- **收藏夹**: 个人收藏和播放列表
### 🎬 高级功能
- **视频编辑**: 视频裁剪、替换、保存为新文件或创建片段
- **自适应流媒体**: 通过HLS协议支持自适应视频流
- **多语言字幕**: 支持多语言字幕文件上传和显示
- **可扩展转码**: 基于优先级的转码系统，支持远程工作节点
- **分块上传**: 支持可暂停/可恢复的大文件上传
- **REST API**: 通过Swagger文档化的完整API接口

### 🔧 技术特性
- **多转码配置**: 支持多种分辨率(144p-1080p)和编码格式(h264, h265, vp9)
- **增强播放器**: 基于video.js的自定义播放器，支持多分辨率和播放速度
- **响应式设计**: 包含明暗主题切换
- **SAML支持**: 企业级单点登录集成
- **实时搜索**: 丰富的搜索功能和实时搜索建议

## 🚀 快速开始

### 📋 系统要求

- **操作系统**: Windows 10/11, Ubuntu 20.04+, CentOS 7+
- **Python**: 3.12+
- **数据库**: PostgreSQL 13+
- **缓存**: Redis 6+
- **内存**: 最小4GB，推荐8GB+
- **存储**: 最小20GB，推荐100GB+（用于媒体文件存储）

### 🛠️ 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/your-username/mediacms.git
cd mediacms
```

#### 2. 环境配置
```bash
# 复制环境变量配置文件
cp .env.example .env

# 编辑配置文件
# 设置数据库连接、Redis配置等
```

#### 3. 安装依赖
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend-vue
npm install
npm run build
cd ..
```

#### 4. 数据库初始化
```bash
# 运行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 加载初始数据
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/encoding_profiles.json
```

#### 5. 启动服务
```bash
# 启动Django开发服务器
python manage.py runserver 0.0.0.0:8000

# 启动Celery工作进程（新终端）
celery -A cms worker -l info

# 启动Celery定时任务（新终端）
celery -A cms beat -l info
```

### 🐳 Docker部署

```bash
# 使用Docker Compose快速部署
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 📖 使用指南

### 🔑 管理后台访问
- **URL**: http://localhost:8000/admin/
- **功能**: 用户管理、媒体审核、系统配置

### 🌐 前端界面访问
- **URL**: http://localhost:8000/
- **功能**: 媒体浏览、上传、播放、互动

### 📚 API文档
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/docs/api/

## 🎯 应用场景

- **🎓 教育机构**: 在线课程视频管理，学生学习资源平台
- **🏢 企业内训**: 内部培训视频，知识库管理
- **📺 媒体机构**: 新闻视频发布，内容管理平台
- **👥 社区平台**: 用户生成内容，社区视频分享
- **🏠 个人博客**: 个人视频作品集，生活记录平台

## 🔧 开发指南

### 📁 项目结构
```
mediacms/
├── cms/                    # Django核心配置
├── files/                  # 媒体文件管理
├── users/                  # 用户系统
├── actions/               # 用户行为记录
├── frontend-vue/          # Vue.js前端
├── static/                # 静态文件
├── templates/             # Django模板
├── docs/                  # 项目文档
└── requirements.txt       # Python依赖
```

### 🔄 开发流程
1. **Fork项目** 并创建功能分支
2. **编写代码** 并添加测试
3. **运行测试** 确保功能正常
4. **提交PR** 并描述更改内容

### 🧪 测试
```bash
# 运行Python测试
python manage.py test

# 运行前端测试
cd frontend-vue
npm run test
```

## 📄 许可证

本项目基于 [GNU Affero General Public License v3.0](LICENSE.txt) 开源协议发布。

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

### 贡献指南
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📞 联系方式

- **项目作者**: [wal]
- **邮箱**: [13030427437@163.com]
- **GitHub**: [https://github.com/3198073725]

## 🙏 致谢

- 感谢 [MediaCMS](https://github.com/mediacms-io/mediacms) 原项目团队
- 感谢所有贡献者和测试用户的支持

---

⭐ 如果这个项目对您有帮助，请给它一个Star！

## 🛠️ 技术栈

本项目使用以下优秀的技术和工具构建：

### 后端技术
- **Python 3.12** - 主要编程语言
- **Django 5.0** - Web框架
- **Django REST Framework** - API框架
- **Celery** - 异步任务队列
- **PostgreSQL** - 主数据库
- **Redis** - 缓存和消息队列

### 前端技术
- **Vue.js 3.0** - 前端框架
- **TypeScript** - 类型安全的JavaScript
- **Vite** - 构建工具
- **Element Plus** - UI组件库

### 媒体处理
- **FFmpeg** - 视频/音频处理
- **Bento4** - MP4工具集
- **video.js** - HTML5视频播放器
- **Fine Uploader** - 文件上传组件

### 部署运维
- **Docker** - 容器化部署
- **Nginx** - Web服务器和反向代理
- **uWSGI** - WSGI服务器

## 📊 项目统计

- **代码行数**: 50,000+ 行
- **支持语言**: 中文、英文等多语言
- **文件格式**: 支持20+种媒体格式
- **并发用户**: 支持1000+并发用户访问

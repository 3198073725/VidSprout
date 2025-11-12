# MediaCMS 管理员文档

## 目录

- [1. 欢迎](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#1-欢迎)
- [2. 单服务器安装](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#2-单服务器安装)
- [3. Docker 安装](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#3-docker-安装)
- [4. Docker 部署选项](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#4-docker-部署选项)
- [5. 配置](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#5-配置)
- [6. 管理页面](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#6-管理页面)
- [7. Django 管理仪表板](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#7-django-管理仪表板)
- [8. 门户工作流程](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#8-门户工作流程)
- [9. 用户角色](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#9-用户角色)
- [10. 为字幕和副标题添加语言](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#10-为字幕和副标题添加语言)
- [11. 添加/删除分类和标签](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#11-添加删除分类和标签)
- [12. 视频转码](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#12-视频转码)
- [13. 如何向侧边栏添加静态页面](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#13-如何向侧边栏添加静态页面)
- [14. 添加 Google Analytics](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#14-添加-google-analytics)
- [15. 调试电子邮件问题](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#15-调试电子邮件问题)
- [16. 常见问题解答](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#16-常见问题解答)
- [17. Cookie 同意代码](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#17-cookie-同意代码)
- [18. 禁用编码并仅显示原始文件](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#18-禁用编码并仅显示原始文件)
- [19. 视频圆角](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#19-视频圆角)
- [20. 翻译](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#20-翻译)
- [21. 如何更改视频的帧画面](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#21-如何更改视频的帧画面)
- [22. 基于角色的访问控制](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#22-基于角色的访问控制)
- [23. SAML 设置](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#23-saml-设置)
- [24. 身份提供商设置](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#24-身份提供商设置)
- [25. 自定义 URL](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#25-自定义-url)
- [26. 允许的文件类型](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#26-允许的文件类型)
- [27. 用户上传限制](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#27-用户上传限制)
- [28. 用于自动字幕的 Whisper 转录](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#28-用于自动字幕的-whisper-转录)

## 1. 欢迎

本页面专为负责设置、维护和修改 MediaCMS 软件的管理员创建。

## 2. 单服务器安装

核心依赖项是 python3、Django、celery、PostgreSQL、redis、ffmpeg。任何可以安装这些依赖项的系统都可以运行 MediaCMS。但 install.sh 仅在 Linux Ubuntu 24 和 22 版本中经过测试。

在已安装 git 工具的 Ubuntu 22/24 系统上，通过以下步骤可在几分钟内完成安装。

请确保以 root 用户身份在干净的系统上运行，因为自动脚本将安装和配置以下服务：Celery/PostgreSQL/Redis/Nginx，并将覆盖任何现有设置。

```
mkdir /home/mediacms.io && cd /home/mediacms.io/
git clone https://github.com/mediacms-io/mediacms
cd /home/mediacms.io/mediacms/ && bash ./install.sh
```

脚本将询问您是否有一个要部署 MediaCMS 的 URL，否则将使用 localhost。如果您提供了 URL，它将使用 Let's Encrypt 服务安装有效的 SSL 证书。

### 更新

如果您使用上述方式安装了 MediaCMS，请按以下方式更新：

```
cd /home/mediacms.io/mediacms # 进入 mediacms 目录
source  /home/mediacms.io/bin/activate # 使用虚拟环境
git pull # 更新代码
pip install -r requirements.txt -U # 运行 pip install 进行更新
python manage.py migrate # 运行 Django 迁移
sudo systemctl restart mediacms celery_long celery_short # 重启服务
```

### 从版本 2 更新到版本 3

版本 3 使用 Django 4 和 Celery 5，并且需要较新的 Python 3.x 版本。如果您是从旧版本更新，请确保首先更新 Python。版本 2 可以在 Python 3.6 上运行，但版本 3 需要 Python 3.8 或更高版本。

启动 Celery 的语法也已更改，因此您必须复制与 celery 相关的 systemctl 文件并重启。

```
# cp deploy/local_install/celery_long.service /etc/systemd/system/celery_long.service
# cp deploy/local_install/celery_short.service /etc/systemd/system/celery_short.service
# cp deploy/local_install/celery_beat.service /etc/systemd/system/celery_beat.service
# systemctl daemon-reload
# systemctl start celery_long celery_short celery_beat
```

### 配置

请查看此处的配置部分。

### 维护

可以使用 pg_dump 备份数据库，/home/mediacms.io/mediacms/media_files 上的 media_files 包含原始文件和编码/转码后的版本。

## 3. Docker 安装

## 安装

安装最新版本的 [Docker](https://docs.docker.com/get-docker/)和 [Docker Compose](https://docs.docker.com/compose/install/)。

对于 Ubuntu 系统，命令如下：

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

然后以 root 身份运行

```
git clone https://github.com/mediacms-io/mediacms
cd mediacms
```

默认选项是在服务器的所有可用 IP（包括 localhost）上提供 MediaCMS 服务。

如果您想探索更多选项（包括使用 letsencrypt 证书设置 https），请查看 [Docker 部署](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#4-docker-部署选项)部分，了解要使用的不同 docker-compose 设置。

运行

```
docker compose up
```

这将下载所有与 MediaCMS 相关的 Docker 镜像并启动所有容器。完成后，MediaCMS 将安装在 [http://localhost](http://localhost/)或 [http://ip](http://ip/)上。

已创建一个名为 admin 的用户，密码随机，您应该能够在迁移容器末尾看到它，例如：

```
migrations_1     | Created admin user with password: gwg1clfkwf
```

或者，如果您在使用的 docker-compose 文件（例如 `docker-compose.yaml`）中设置了 ADMIN_PASSWORD 变量，则该变量将设置为 admin 用户的密码。

`注意`：如果您想使用自动转录功能，您必须执行以下操作之一：

- 要么使用 docker-compose.full.yaml，在这种情况下运行 `docker-compose -f docker-compose.yaml -f docker-compose.full.yaml up`
- 或者编辑 docker-compose.yaml 文件，将 celery_worker 服务的镜像设置为 mediacms/mediacms:full 而不是 mediacms/mediacms:latest

此外，在 settings.py 文件中设置变量 `USE_WHISPER_TRANSCRIBE = True`

### 更新

获取最新的 MediaCMS 镜像并停止/启动容器

```
cd /path/to/mediacms/installation
docker pull mediacms/mediacms
docker compose down
docker compose up
```

### 从版本 2 更新到版本 3

版本 3 使用 Python 3.11 和 PostgreSQL 15。如果您是从使用 PostgreSQL 13 的旧版本更新，自动更新将无法工作，因为当 PostgreSQL 容器启动时您将收到以下消息：

```
db_1              | 2023-06-27 11:07:42.959 UTC [1] FATAL:  database files are incompatible with server
db_1              | 2023-06-27 11:07:42.959 UTC [1] DETAIL:  The data directory was initialized by PostgreSQL version 13, which is not compatible with this version 15.2.
```

此时有两个选项：要么编辑 Docker Compose 文件并使用现有的 postgres:13 镜像，要么您必须执行从 postgresql 13 到版本 15 的迁移。更多说明请参考 https://github.com/mediacms-io/mediacms/pull/749

## 配置

请查看此处的配置文档。

### 维护

数据库存储在 ../postgres_data/，media_files 存储在 media_files/。

## 4. Docker 部署选项

mediacms 镜像构建为使用 supervisord 作为主进程，它管理运行 mediacms 所需的一个或多个服务。我们可以通过将以下环境变量设置为 `yes`或 `no`来切换给定容器中运行的服务：

- ENABLE_UWSGI
- ENABLE_NGINX
- ENABLE_CELERY_BEAT
- ENABLE_CELERY_SHORT
- ENABLE_CELERY_LONG
- ENABLE_MIGRATIONS

默认情况下，所有这些服务都已启用，但为了创建可扩展的部署，可以禁用其中一些服务，将服务拆分为更小的服务。

另请参阅 `Dockerfile`了解您可能希望覆盖的其他环境变量。应用程序设置，例如 `FRONTEND_HOST`，也可以通过更新 `deploy/docker/local_settings.py`文件来覆盖。

要运行，请根据需要更新上述配置，通过运行 `docker compose build`构建镜像，然后运行 `docker compose run`

### 简单部署，通过 [http://localhost](http://localhost/)访问

主容器运行迁移、mediacms_web、celery_beat、celery_workers（celery_short 和 celery_long 服务），在端口 80 上公开，由 redis 和 postgres 数据库支持。

`deploy/docker/local_settings.py`中的 FRONTEND_HOST 配置为 [http://localhost](http://localhost/)，在 docker 主机上。

### 通过 letsencrypt 服务提供 SSL 证书的服务器，通过 [https://my_domain.com](https://my_domain.com/)访问

在尝试此方法之前，请确保 IP 指向 my_domain.com。

使用此方法时，使用 [此部署](https://tencent.yuanbao/docker-compose-letsencrypt.yaml)。

编辑此文件，将 `VIRTUAL_HOST`设置为 my_domain.com，`LETSENCRYPT_HOST`设置为 my_domain.com，并在 `LETSENCRYPT_EMAIL`中设置您的电子邮件。

编辑 `deploy/docker/local_settings.py`并将 `FRONTEND_HOST`设置为 [https://my_domain.com](https://my_domain.com/)。

现在运行 `docker compose -f docker-compose-letsencrypt.yaml up`，安装完成后，您将能够使用有效的 Letsencrypt 证书访问 [https://my_domain.com](https://my_domain.com/)！

### 高级部署，通过 [http://localhost:8000](http://localhost:8000/)访问

这里我们可以运行 1 个 mediacms_web 实例，`deploy/docker/local_settings.py`中的 FRONTEND_HOST 配置为 [http://localhost:8000](http://localhost:8000/)。这由一个单独的迁移实例引导，并由一个 celery_beat 实例和一个或多个 celery_worker 实例支持。Redis 和 postgres 容器也用于持久化。客户端可以在 docker 主机上的 [http://localhost:8000](http://localhost:8000/)访问服务。这类似于 [此部署](https://tencent.yuanbao/docker-compose.yaml)，其中在 FRONTEND_HOST 中定义了 `port`。

### 高级部署，带反向代理，通过 [http://mediacms.io](http://mediacms.io/)访问

这里我们可以使用 `jwilder/nginx-proxy`反向代理到一个或多个 mediacms_web 实例，并由先前部署中提到的其他服务支持。`deploy/docker/local_settings.py`中的 FRONTEND_HOST 配置为 [http://mediacms.io](http://mediacms.io/)，nginx-proxy 暴露端口 80。客户端可以访问 [http://mediacms.io](http://mediacms.io/)上的服务（假设 DNS 或主机文件已正确设置以指向 nginx-proxy 实例的 IP）。这类似于 [此部署](https://tencent.yuanbao/docker-compose-http-proxy.yaml)。

### 高级部署，带反向代理，通过 [https://localhost](https://localhost/)访问

反向代理（`jwilder/nginx-proxy`）可以配置为使用自签名证书、letsencrypt 或 CA 签名证书提供 SSL 终止（请参阅：https://hub.docker.com/r/jwilder/nginx-proxy或 [LetsEncrypt 示例](https://www.singularaspect.com/use-nginx-proxy-and-letsencrypt-companion-to-host-multiple-websites/)）。在这种情况下，FRONTEND_HOST 应设置为 [https://mediacms.io](https://mediacms.io/)。这类似于 [此部署](https://tencent.yuanbao/docker-compose-http-proxy.yaml)。

### 可扩展的部署架构（Docker、Swarm、Kubernetes）

下面的架构概括了上述所有部署场景，并为基于 kubernetes 和 docker swarm 的其他部署提供了概念设计。它通过使用多个 mediacms_web 实例和 celery_workers 允许水平扩展。对于大型部署，可以采用托管 postgres、redis 和存储。

## 5. 配置

`cms/settings.py`中提供了多个选项，大多数允许或应该禁止的内容都在那里描述。

建议通过将它们添加到 `local_settings.py`来覆盖它们中的任何一个。

如果是单服务器安装，请添加到 `cms/local_settings.py`。

如果是 docker compose 安装，请添加到 `deploy/docker/local_settings.py`。这将自动覆盖 `cms/local_settings.py`。

任何更改都需要重新启动 MediaCMS 才能生效。

单服务器安装：编辑 `cms/local_settings.py`，进行更改并重新启动 MediaCMS

```
#systemctl restart mediacms
```

Docker Compose 安装：编辑 `deploy/docker/local_settings.py`，进行更改并重新启动 MediaCMS 容器

```
#docker compose restart web celery_worker celery_beat
```

### 5.1 更改门户徽标

白色主题的默认 svg 文件在 `static/images/logo_dark.svg`，深色主题的在 `static/images/logo_light.svg`。

您可以通过编辑 `settings.py`中的 `PORTAL_LOGO_DARK_SVG`和 `PORTAL_LOGO_LIGHT_SVG`变量来指定新的 svg 路径以进行覆盖。

您也可以使用自定义 png，通过在 `settings.py`中设置变量 `PORTAL_LOGO_DARK_PNG`和 `PORTAL_LOGO_LIGHT_PNG`。svg 文件优先于 png 文件，因此如果两者都设置，将使用 svg 文件。

在任何情况下，请确保文件放在 static/images 文件夹中。

### 5.2 设置全局门户标题

设置 `PORTAL_NAME`，例如：

```
PORTAL_NAME = '我的超棒门户'
```

### 5.3 控制谁可以添加媒体

默认情况下 `CAN_ADD_MEDIA = "all"`意味着所有注册用户都可以添加媒体。其他有效选项是：

- **email_verified**，用户不仅必须注册帐户，还必须验证电子邮件（通过点击注册时发送的链接）。显然电子邮件配置需要工作，否则用户将收不到电子邮件。
- **advancedUser**，只有被标记为高级用户的用户才能添加媒体。管理员或 MediaCMS 经理可以通过编辑用户个人资料并选择 advancedUser 来使用户成为高级用户。

### 5.4 什么是门户工作流程

`PORTAL_WORKFLOW`变量指定新上传媒体的处理方式，即它们是否出现在列表（如索引页或搜索）中。

- **public** 是默认选项，意味着媒体可以出现在列表上。如果媒体类型是视频，则至少有一个成功生成文件编码版本的任务完成后，它才会出现。对于其他类型的文件，如图像/音频，它们会立即出现。
- **private** 意味着新上传的内容是私有的 - 只有用户或 MediaCMS 编辑、经理和管理员可以看到它。他们也可以将状态设置为公开或未列出。
- **unlisted** 意味着项目是未列出的。但是，如果用户访问未列出媒体的 URL，它将被显示（与私有相反）。

### 5.5 显示或隐藏登录按钮

显示按钮：

```
LOGIN_ALLOWED = True
```

隐藏按钮：

```
LOGIN_ALLOWED = False
```

### 5.6 显示或隐藏注册按钮

显示按钮：

```
REGISTER_ALLOWED = True
```

隐藏按钮：

```
REGISTER_ALLOWED = False
```

### 5.7 显示或隐藏上传媒体按钮

显示：

```
UPLOAD_MEDIA_ALLOWED = True
```

隐藏：

```
UPLOAD_MEDIA_ALLOWED = False
```

### 5.8 显示或隐藏操作按钮（如喜欢/不喜欢/报告）

对以下任何一项进行更改（True/False）：

```
- CAN_LIKE_MEDIA = True  # 是否显示喜欢媒体按钮
- CAN_DISLIKE_MEDIA = True  # 是否显示不喜欢媒体按钮
- CAN_REPORT_MEDIA = True  # 是否显示报告媒体按钮
- CAN_SHARE_MEDIA = True  # 是否显示分享媒体按钮
```

### 5.9 显示或隐藏媒体上的下载选项

编辑 `templates/config/installation/features.html`并设置：

```
download: false
```

### 5.10 媒体被报告后自动隐藏

为变量 `REPORTED_TIMES_THRESHOLD`设置一个较小的数字。

例如：

```
REPORTED_TIMES_THRESHOLD = 2
```

一旦达到限制，媒体将变为私有状态，并向管理员发送电子邮件。

### 5.11 在媒体上传页面设置自定义消息

此消息将出现在媒体拖放表单下方。

```
PRE_UPLOAD_MEDIA_MESSAGE = '自定义消息'
```

### 5.12 设置电子邮件配置

根据提供商设置正确的配置。

```
DEFAULT_FROM_EMAIL = 'info@mediacms.io'
EMAIL_HOST_PASSWORD = 'xyz'
EMAIL_HOST_USER = 'info@mediacms.io'
EMAIL_USE_TLS = True
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = 'mediacms.io'
EMAIL_PORT = 587
ADMIN_EMAIL_LIST = ['info@mediacms.io']
```

### 5.13 禁止来自特定域的用户注册

通过此变量设置注册无效的域：

```
RESTRICTED_DOMAINS_FOR_USER_REGISTRATION = [
    'xxx.com', 'emaildomainwhatever.com']
```

或者，只允许许可的域进行注册。当您在组织内将 mediacms 用作私有服务时，这可能很有用，并且希望给予组织内人员免费注册，但拒绝所有其他域的注册。设置此选项将禁止列表中未包含的所有域进行注册。默认是一个空列表，将被忽略。要禁用，请设置为空列表。

```
ALLOWED_DOMAINS_FOR_USER_REGISTRATION = [
	"private.com",
	"vod.private.com",
	"my.favorite.domain",
	"test.private.com"]
```

### 5.14 需要由 MediaCMS 编辑/经理/管理员审核

设置值：

```
MEDIA_IS_REVIEWED = False
```

现在任何上传的媒体都需要经过审核才能出现在列表中。

MediaCMS 编辑/经理/管理员可以访问媒体页面并进行编辑，在那里他们可以看到将媒体标记为已审核的选项。默认情况下，此选项设置为 True，因此所有媒体都不需要审核。

### 5.15 指定播放列表的最大媒体数量

在变量 `MAX_MEDIA_PER_PLAYLIST`上设置不同的阈值。

例如：

```
MAX_MEDIA_PER_PLAYLIST = 14
```

### 5.16 指定可以上传的媒体的最大大小

更改 `UPLOAD_MAX_SIZE`。

默认为 4GB。

```
UPLOAD_MAX_SIZE = 800 * 1024 * 1000 * 5
```

### 5.17 指定评论的最大大小

更改 `MAX_CHARS_FOR_COMMENT`。

默认：

```
MAX_CHARS_FOR_COMMENT = 10000
```

### 5.18 并行上传多少个文件

为 `UPLOAD_MAX_FILES_NUMBER`设置不同的阈值。

默认：

```
UPLOAD_MAX_FILES_NUMBER = 100
```

### 5.19 强制用户在注册时确认其电子邮件

电子邮件确认的默认选项是可选。将此设置为强制性，以强制用户在登录前确认其电子邮件。

```
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

### 5.20 限制帐户登录尝试次数

达到此数字后：

```
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 20
```

设置超时（以秒为单位）：

```
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 5
```

### 5.21 禁止用户注册

将以下变量设置为 False：

```
USERS_CAN_SELF_REGISTER = False
```

### 5.22 配置通知

已实现的全局通知由以下选项控制：

```
USERS_NOTIFICATIONS = {
    'MEDIA_ADDED': True,
}
```

如果您想禁用新媒体的通知，请设置为 False。

管理员也会在不同事件上收到通知，将以下任何一项设置为 False 以禁用。

```
ADMINS_NOTIFICATIONS = {
    'NEW_USER': True,
    'MEDIA_ADDED': True,
    'MEDIA_REPORTED': True,
}
```

- NEW_USER：添加了新用户。
- MEDIA_ADDED：添加了媒体。
- MEDIA_REPORTED：媒体的报告被触发。

### 5.23 配置仅限成员访问媒体

- 将门户工作流程设置为公开，但同时设置 `GLOBAL_LOGIN_REQUIRED = True`，以便只有登录的用户才能看到内容。
- 如果您想自己添加成员，可以设置 `REGISTER_ALLOWED = False`，或者查看 `cms/settings.py`中影响注册的 "django-allauth 设置" 选项。例如，将门户设置为仅限邀请，或将电子邮件确认设置为强制性，以便您控制谁可以注册。

### 5.24 启用站点地图

是否在 http://your_installation/sitemap.xml生成站点地图文件（默认：False）

```
GENERATE_SITEMAP = True
```

### 5.25 控制谁可以添加评论

默认情况下 `CAN_COMMENT = "all"`意味着所有注册用户都可以添加评论。其他有效选项是：

- **email_verified**，用户不仅必须注册帐户，还必须验证电子邮件（通过点击注册时发送的链接）。显然电子邮件配置需要工作，否则用户将收不到电子邮件。
- **advancedUser**，只有被标记为高级用户的用户才能添加评论。管理员或 MediaCMS 经理可以通过编辑用户个人资料并选择 advancedUser 来使用户成为高级用户。

### 5.26 控制匿名用户是否可以列出所有用户

默认情况下，匿名用户可以查看平台上所有用户的列表。要将其限制为仅限经过身份验证的用户，请设置：

```
ALLOW_ANONYMOUS_USER_LISTING = False
```

当设置为 False 时，只有登录的用户才能访问用户列表 API 端点。

### 5.27 控制谁可以看到成员页面

默认情况下 `CAN_SEE_MEMBERS_PAGE = "all"`意味着所有注册用户都可以看到成员页面。其他有效选项是：

- **editors**，只有 MediaCMS 编辑可以查看该页面。
- **admins**，只有 MediaCMS 管理员可以查看该页面。

### 5.28 要求注册时批准用户

默认情况下，用户不需要批准，因此他们可以在注册后立即登录（如果注册开放）。但是，如果参数 `USERS_NEEDS_TO_BE_APPROVED`设置为 `True`，他们将首先必须由其管理员批准帐户，然后才能成功登录。

管理员可以通过以下方式批准用户：1. 通过 Django 管理界面，2. 通过用户管理页面，3. 通过直接编辑个人资料页面。在所有情况下，将 'Is approved' 设置为 True。

## 6. 管理页面

待编写。

## 7. Django 管理仪表板

## 8. 门户工作流程

谁可以发布内容，内容如何出现在公共列表中。状态（私有、未列出、公开）之间的区别。

## 9. 用户角色

MediaCMS 经理、MediaCMS 编辑、登录用户之间的区别。

## 10. 为字幕和副标题添加语言

待编写。

## 11. 添加/删除分类和标签

通过管理部分 - http://your_installation/admin/

## 12. 视频转码

通过 https://your_installation/admin/files/encodeprofile/修改 `编码配置文件`数据库表来添加/删除分辨率和配置文件。

例如，任何配置文件的 `Active`状态都可以切换以启用或禁用它。

## 13. 如何向侧边栏添加静态页面

### 1. 在 templates/cms/ 中创建您的 html 页面

例如，复制并重命名 about.html。

```
sudo cp templates/cms/about.html templates/cms/volunteer.html
```

### 2. 在 static/css/ 中创建您的 css 文件

```
touch static/css/volunteer.css
```

### 3. 在您的 html 文件中，更新 block headermeta 以反映您的新页面

```
{% block headermeta %}
<meta property="og:title" content="Volunteer - {{PORTAL_NAME}}">
<meta property="og:type" content="website">
<meta property="og:description" content="">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "BreadcrumbList",
	"itemListElement": [{
		"@type": "ListItem",
		"position": 1,
        "name": "{{PORTAL_NAME}}",
        "item": {
			"@type": "WebPage",
	        "@id": "{{FRONTEND_HOST}}"
	    }
    },
    {
		"@type": "ListItem",
		"position": 2,
        "name": "Volunteer",
        "item": {
			"@type": "VolunteerPage",
	        "@id": "{{FRONTEND_HOST}}/volunteer"
	    }
    }]
}
</script>
<link href="{% static "css/volunteer.css" %}" rel="stylesheet"/>
{% endblock headermeta %}
```

### 4. 在您的 html 文件中，更新 block innercontent 以反映您的实际内容

编写任何您喜欢的内容。

### 5. 在您的 css 文件中，为您的 html 文件编写匹配的样式。

编写任何您喜欢的样式。

### 6. 将您的视图添加到 files/views.py

```
def volunteer(request):
    """Volunteer 视图"""
    context = {}
    return render(request, "cms/volunteer.html", context)
```

### 7. 将您的 URL 模式添加到 files/urls.py

```
urlpatterns = [
    url(r"^$", views.index),
    url(r"^about", views.about, name="about"),
    url(r"^volunteer", views.volunteer, name="volunteer"),
```

### 8. 将您的页面添加到左侧边栏

要将您的页面链接作为菜单项添加到左侧边栏，

在 _commons.js 的最后一行之后添加以下代码。

```
/* 检查给定的选择器是否已加载。 */
const checkElement = async selector => {
    while ( document.querySelector(selector) === null) {
      await new Promise( resolve =>  requestAnimationFrame(resolve) )
    }
    return document.querySelector(selector);
  };

/* 检查侧边栏导航菜单是否已加载，然后添加菜单项。 */
checkElement('.nav-menu')
.then((element) => {
     (function(){
        var a = document.createElement('a');
        a.href = "/volunteer";
        a.title = "Volunteer";

        var s = document.createElement('span');
        s.className = "menu-item-icon";

        var icon = document.createElement('i');
        icon.className = "material-icons";
        icon.setAttribute("data-icon", "people");

        s.appendChild(icon);
        a.appendChild(s);

        var linkText = document.createTextNode("Volunteer");
        var t = document.createElement('span');

        t.appendChild(linkText);
        a.appendChild(t);

        var listItem = document.createElement('li');
        listItem.className = "link-item";
        listItem.appendChild(a);

        // 如果已登出使用第3个 nav-menu
        var elem = document.querySelector(".nav-menu:nth-child(3) nav ul");
        var loc = elem.innerText;
        if (loc.includes("About")){
          elem.insertBefore(listItem, elem.children[2]);
        } else { // 如果已登录使用第4个 nav-menu
          elem = document.querySelector(".nav-menu:nth-child(4) nav ul");
          elem.insertBefore(listItem, elem.children[2]);
        }
    })();
});
```

### 9. 重新启动 mediacms Web 服务器

在 Docker 上：

```
sudo docker stop mediacms_web_1 && sudo docker start mediacms_web_1
```

否则：

```
sudo systemctl restart mediacms
```

## 14. 添加 Google Analytics

由 @alberto98fx 贡献的说明。

1. 创建一个文件：

```
touch $DIR/mediacms/templates/tracking.html
```

1. 添加 Gtag/Analytics 脚本。
2. 在 `$DIR/mediacms/templates/root.html`中，您会看到一个类似这样的文件：

```
<head>
    {% block head %}

        <title>{% block headtitle %}{{PORTAL_NAME}}{% endblock headtitle %}</title>

        {% include "common/head-meta.html" %}

        {% block headermeta %}

        <meta property="og:title" content="{{PORTAL_NAME}}">
        <meta property="og:type" content="website">

        {%endblock headermeta %}

        {% block externallinks %}{% endblock externallinks %}

        {% include "common/head-links.html" %}

        {% block topimports %}{%endblock topimports %}

        {% include "config/index.html" %}

    {% endblock head %}

</head>
```

1. 在 `<head>`部分的末尾添加 `{% include "tracking.html" %}`。
2. 如果您使用 Docker 并且没有挂载整个目录，您需要绑定一个新卷：

```
web:
    image: mediacms/mediacms:latest
    restart: unless-stopped
    ports:
      - "80:80"
    deploy:
      replicas: 1
    volumes:
      - ./templates/root.html:/home/mediacms.io/mediacms/templates/root.html
      - ./templates/tracking.html://home/mediacms.io/mediacms/templates/tracking.html
```

## 15. 调试电子邮件问题

在本指南的 [配置](https://tencent.yuanbao/chat?from=launch&conversation=a825edcd-db7b-4680-b326-a06117d42127&project_id=&project_name=#5-配置)部分，我们已经看到了如何编辑电子邮件设置。

如果我们仍然无法从 MediaCMS 接收电子邮件，以下内容可能有助于我们调试问题 - 在大多数情况下，这是设置正确的用户名、密码或 TLS 选项的问题。

进入 Django shell，例如，如果您使用单服务器安装：

```
source  /home/mediacms.io/bin/activate
python manage.py shell
```

在 shell 内部：

```
from django.core.mail import EmailMessage
from django.conf import settings

settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

email = EmailMessage(
    '标题',
    '消息',
    settings.DEFAULT_FROM_EMAIL,
    ['recipient@email.com'],
)
email.send(fail_silently=False)
```

您有机会要么收到电子邮件（在这种情况下，它将发送到 recipient@email.com），要么您将看到错误。

例如，在为我的 Gmail 帐户指定错误密码时，我得到：

```
SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials d4sm12687785wrc.34 - gsmtp')
```

## 16. 常见问题解答

视频正在播放，但大型视频文件的预览缩略图没有显示。

可能是精灵图文件没有正确创建。

在这种情况下，files.tasks.produce_sprite_from_video() 函数的输出是这样的：

```
convert-im6.q16: width or height exceeds limit `/tmp/img001.jpg' @ error/cache.c/OpenPixelCache/3912.
```

解决方案：编辑文件 `/etc/ImageMagick-6/policy.xml`并为包含 width 和 height 的行设置更大的值。例如：

```
<policy domain="resource" name="height" value="16000KP"/>
  <policy domain="resource" name="width" value="16000KP"/>
```

现在新添加的视频文件将能够生成缩略图预览所需的精灵图文件。要对现有视频重新运行该任务，请进入 Django shell。

```
root@8433f923ccf5:/home/mediacms.io/mediacms# source  /home/mediacms.io/bin/activate
root@8433f923ccf5:/home/mediacms.io/mediacms# python manage.py shell
Python 3.8.14 (default, Sep 13 2022, 02:23:58)
```

并运行：

```
In [1]: from files.models import Media
In [2]: from files.tasks import produce_sprite_from_video

In [3]: for media in Media.objects.filter(media_type='video', sprites=''):
   ...:     produce_sprite_from_video(media.friendly_token)
```

这将为任务失败的视频重新创建精灵图。

## 17. Cookie 同意代码

在文件 `templates/components/header.html`中，您可以找到一个简单的 Cookie 同意代码。它被注释掉了，因此您必须删除 `{% comment %}`和 `{% endcomment %}`行才能启用它。或者您可以用您自己的处理 Cookie 同意横幅的代码替换该部分。

## 18. 禁用编码并仅显示原始文件

当视频上传时，它们会被编码为多个分辨率，这个过程称为转码。有时这是不需要的，您只需要显示原始文件，例如当 MediaCMS 在低性能服务器上运行时。要实现这一点，请编辑 settings.py 并设置：

```
DO_NOT_TRANSCODE_VIDEO = True
```

这将禁用转码过程，并且只显示原始文件。请注意，这也会禁用精灵图文件的创建，因此您将无法在视频播放器上看到预览缩略图。

## 19. 视频圆角

默认情况下，视频播放器和媒体项目现在在大屏幕上（不在移动设备上）具有圆角。如果您不喜欢此更改，请在 `local_settings.py`中设置 `USE_ROUNDED_CORNERS = False`。

## 20. 翻译

### 20.1 设置默认语言

默认情况下，MediaCMS 提供多种语言。要设置默认语言，请编辑 `settings.py`并将 LANGUAGE_CODE 设置为其中一种语言的代码。

### 20.2 移除现有语言

要限制显示为可用的语言数量，请从 `settings.py`中的 LANGUAGES 列表中移除它们或将其注释掉。只显示列表中存在的语言。

### 20.3 改进现有翻译

要改进已翻译语言中的现有翻译内容，请通过 `files/frontend-translations/`中的代码名称检查语言，并编辑相应的文件。

### 20.4 向现有翻译添加更多内容

并非所有文本都已翻译，因此您可能随时发现需要添加到翻译中的缺失字符串。这里的想法是：

a) 您在代码中将文本标记为可翻译。

b) 您添加翻译后的字符串。

对于 a)，您必须查看要翻译的字符串是位于前端目录（React 应用程序）中还是 Django 模板中。两者都有示例。

1. Django 模板，位于 templates/ 目录中。查看 `templates/cms/about.html`以了解如何完成的示例。
2. 前端代码（React），查看 `frontend`中如何使用 `translateString`。

在字符串被标记为可翻译后，首先将字符串添加到 `files/frontend-translations/en.py`，然后运行：

```
python manage.py process_translations
```

以便在所有语言中填充该字符串。如果不遵循此过程，PR 将不被接受。您不必将字符串翻译成所有支持的语言，但必须运行该命令并为所有语言在现有字典中填充新字符串。这确保了任何语言中都没有缺失的待翻译字符串。

运行此命令后，将字符串翻译成您想要的语言。如果要翻译的字符串位于 Django 模板中，则无需重新构建前端。如果更改位于前端，则必须重新构建才能看到更改。Makefile 命令 `make build-frontend`可以帮助完成此操作。

### 20.5 添加新语言并进行翻译

要添加新语言：在 settings.py 中添加语言，然后在 `files/frontend-translations/`中添加文件。确保通过复制 `files/frontend-translations/en.py`来复制初始字符串。

## 21. 如何更改视频的帧画面

默认情况下，观看视频时，您可以将鼠标悬停并看到名为精灵图的小图像，这些图像是每 10 秒从视频中提取的。您可以通过执行以下操作将此数字更改为更小的值：

- 编辑 ./frontend/src/static/js/components/media-viewer/VideoViewer/index.js 并将 `seconds: 10`更改为您喜欢的值，例如 2。
- 编辑 settings.py 并为值 SPRITE_NUM_SECS 设置相同的数字。
- 现在您必须重新构建前端：最简单的方法是运行 `make build-frontend`，这需要 Docker。

之后，新上传的视频将使用新的秒数生成精灵图。

## 22. 基于角色的访问控制

默认情况下，系统上任何媒体都有 3 种状态：公开、未列出、私有。当添加 RBAC 支持时，属于某个组的用户有权访问发布到与该组关联的一个或多个类别的媒体。工作流程如下：

1. 创建一个组。
2. 将一个类别与该组关联。
3. 将一个用户添加到该组。

现在用户即使媒体处于私有状态也可以查看媒体。用户还可以在类别页面中看到所有媒体。

当用户被添加到组时，他们可以被设置为成员、贡献者、经理。

- 成员：用户可以查看发布到与此组关联的一个或多个类别上的媒体。
- 贡献者：除了查看，用户还可以编辑与此组关联的类别中的媒体。他们还可以将媒体发布到此类别。
- 经理：目前与贡献者相同。

RBAC 促进的用例：

- 查看处于私有状态的媒体：如果启用了 RBAC，如果用户是某个组的成员，该组与某个类别关联，并且媒体发布到该类别，则用户可以查看该媒体。
- 编辑媒体：如果启用了 RBAC，并且用户是一个或多个类别的贡献者，只要这些类别与一个组关联，他们就可以将媒体发布到这些类别。
- 查看类别的所有媒体：如果启用了 RBAC，并且用户访问某个类别，他们可以看到发布到该类别的所有媒体的列表，无论其状态如何，前提是该类别与用户所属的组关联。
- 查看与用户所属组关联的所有类别：如果启用了 RBAC，并且用户访问类别列表，他们可以查看与用户所属组关联的所有类别。

如何启用 RBAC 支持：

在 `local_settings.py`中设置：

```
USE_RBAC = True
```

并重新启动实例。

## 23. SAML 设置

SAML 身份验证是支持的，同时可以选择利用 SAML 响应并执行有用的操作，例如设置用户在 MediaCMS 中的角色或参与组。

要启用 SAML 支持，请编辑 local_settings.py 并设置以下选项：

```
USE_RBAC = True
USE_SAML = True
USE_IDENTITY_PROVIDERS = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SOCIALACCOUNT_ADAPTER = 'saml_auth.adapter.SAMLAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    "saml": {
        "provider_class": "saml_auth.custom.provider.CustomSAMLProvider",
    }
}
```

设置 SAML 提供商：

- 步骤 1：添加 SAML 身份提供商

  1. 导航到管理面板。
  2. 选择"身份提供商"。
  3. 按如下方式配置：
     - **提供商**：saml
     - **提供商 ID**：提供商的 ID。
     - **IDP 配置名称**：提供商的名称。
     - **客户端 ID**：登录时使用的标识符，与 IDP 共享。
     - **站点**：设置默认站点。

- 步骤 2：添加 SAML 配置

  选择 SAML 配置选项卡，创建一个新的并设置：

1. **IDP ID**：必须是 URL。
2. **IDP 证书**：来自您的 SAML 提供商的 x509cert。
3. **SSO URL**：
4. **SLO URL**：
5. **SP 元数据 URL**：IDP 将使用的元数据 URL。这可以是 https://{portal}/saml/metadata并且由 MediaCMS 自动生成。

- 步骤 3：设置其他选项
  1. **电子邮件设置**：
     - `verified_email`：启用时，来自 SAML 响应的电子邮件将被标记为已验证。
     - `Remove from groups`：启用时，如果用户已从 IDP 上的组中移除，则在登录后将从组中移除用户。
  2. **全局角色映射**：将 SAML 返回的角色（在 SAML 配置选项卡中设置）映射到 MediaCMS 中的角色。
  3. **组角色映射**：将 SAML 返回的角色（在 SAML 配置选项卡中设置）映射到用户将被添加到的组中的角色。
  4. **组映射**：这将创建与此 IDP 关联的组。来自 SAML 的组 ID，与 MediaCMS 组关联。
  5. **类别映射**：这将 SAML 响应中的组 ID 映射到 MediaCMS 中的类别。

完整的 SAML 部署与 [EntraID 指南和故障排除步骤可在此处获得。](https://tencent.yuanbao/saml_entraid_setup.md)。本指南也可用作其他 IDP 的参考。

## 24. 身份提供商设置

已添加一个单独的 Django 应用程序 identity_providers，以便简化与不同身份提供商相关的一系列配置。如果启用此功能，它将提供以下选项：

- 允许通过 Django 管理界面添加身份提供商，并设置一系列映射，例如组映射、全局角色映射等。虽然 SAML 是开箱即用唯一可以添加的提供商，但任何受 django allauth 支持的身份提供商都可以通过最少的努力添加。如果身份提供商的响应包含属性如角色或组，则这些可以映射到 MediaCMS 特定角色（高级用户、编辑、经理、管理员）和组（rbac 组）。
- 在用户通过身份验证后保存 SAML 响应日志（也可用于其他提供商）。
- 允许通过管理界面指定登录选项列表（例如系统登录、身份提供商登录）。

要启用身份提供商，请在 `local_settings.py`中设置以下设置：

```
USE_IDENTITY_PROVIDERS = True
```

访问管理界面，您将看到身份提供商选项卡，并且可以添加一个。

## 25. 自定义 URL

要启用自定义 URL，请在 settings.py 或 local_settings.py 中设置 `ALLOW_CUSTOM_MEDIA_URLS = True`。

这将允许在编辑媒体时编辑媒体的 URL。如果 URL 已被占用，您将收到无法更新此 URL 的消息。

## 26. 允许的文件类型

MediaCMS 对新文件上传执行识别尝试，并且仅允许 `ALLOWED_MEDIA_UPLOAD_TYPES`设置中指定的某些文件类型。默认情况下，仅允许 ["video", "audio", "image", "pdf"] 文件。

当文件未被识别为这些允许的类型之一时，该文件将从系统中删除，并且会有一条条目表明这是不受支持的媒体类型。

如果您想更改允许的文件类型，请在您的 `settings.py`或 `local_settings.py`文件中编辑 `ALLOWED_MEDIA_UPLOAD_TYPES`列表。如果在此列表中指定了 'all'，则不执行检查，并且允许所有文件。

## 27. 用户上传限制

MediaCMS 允许您设置每个用户可以上传的媒体文件的最大数量。这由 `settings.py`或 `local_settings.py`中的 `NUMBER_OF_MEDIA_USER_CAN_UPLOAD`设置控制。默认情况下，每个用户设置为 100 个媒体项目。

当用户达到此限制时，他们将无法上传新媒体，直到删除一些现有内容。此限制适用于用户在系统中的角色或权限。

要更改每个用户允许的最大上传数量，请在您的设置文件中修改 `NUMBER_OF_MEDIA_USER_CAN_UPLOAD`值：

```
NUMBER_OF_MEDIA_USER_CAN_UPLOAD = 5
```

## 28. 用于自动字幕的 Whisper 转录

MediaCMS 可以与 OpenAI 的 Whisper 集成，自动为您的媒体文件生成字幕。此功能对于使您的内容更易于访问非常有用。

### 工作原理

当为媒体文件触发 whisper 转录任务时，MediaCMS 运行 `whisper`命令行工具来处理音频并生成 VTT 格式的字幕文件。生成的字幕随后与媒体关联，并在"自动"语言选项下可用。

### 配置

转录功能仅适用于 Docker 安装。要启用此功能，您必须使用 `docker-compose.full.yaml`文件，因为它包含具有必要要求的镜像，或者您也可以设置 celery_worker 服务使用 mediacms:full 镜像而不是 mediacms:latest。然后您还必须在 local_settings.py 文件中设置：`USE_WHISPER_TRANSCRIBE = True`。

默认情况下，所有用户都有能力发送请求将视频转录，以及转录并翻译成英语。如果您希望更改此行为，可以编辑 `settings.py`文件并设置 `USER_CAN_TRANSCRIBE_VIDEO=False`。

转录默认使用 Whisper 语音转文本的基础模型。但是，您可以通过编辑 `settings.py`中的 `WHISPER_MODEL`设置来更改模型。

默认模型是 'base'，但您可以选择其他可用的模型，如 'tiny'、'small'、'medium' 或 'large'。较大的模型通常提供更高的准确性，但需要更多的处理时间和资源。

```
WHISPER_MODEL = 'base'  # 可选值: 'tiny', 'base', 'small', 'medium', 'large'
```

### 使用说明

1. 启用转录功能后，用户可以在媒体页面上找到"生成自动字幕"的选项。
2. 转录过程可能需要一些时间，具体取决于视频的长度和所选的 Whisper 模型。
3. 转录完成后，字幕将自动与媒体关联，并可在播放器中选择。
4. 如果启用了翻译功能，用户还可以选择将字幕翻译成英语。

### 性能考虑

- 使用较大的 Whisper 模型（如 'medium' 或 'large'）将需要更多的计算资源和时间。
- 对于较长的视频，转录过程可能需要相当长的时间。
- 确保您的服务器有足够的 CPU 和内存资源来处理转录任务。

### 故障排除

如果转录失败，请检查以下内容：

1. 确保已正确设置 `USE_WHISPER_TRANSCRIBE = True`。
2. 验证使用的是包含 Whisper 的完整镜像（mediacms:full）。
3. 检查日志以了解任何错误消息。
4. 确保服务器有足够的资源来处理转录任务。

通过正确配置和使用 Whisper 转录功能，您可以大大增强 MediaCMS 平台上媒体的可访问性。
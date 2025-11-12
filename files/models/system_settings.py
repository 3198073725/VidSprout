"""
系统设置模型 - 扩展版
支持78个配置项的动态配置
"""
from django.db import models
from django.core.cache import cache


class SystemSettings(models.Model):
    """系统设置模型 - 单例模式，支持通过管理界面动态配置"""
    
    # ==================== 基本设置 ====================
    site_name = models.CharField(
        max_length=200,
        default='MediaCMS',
        help_text='站点名称'
    )
    site_description = models.TextField(
        default='开源媒体内容管理系统',
        help_text='站点描述'
    )
    site_keywords = models.CharField(
        max_length=500,
        default='视频,媒体,CMS',
        help_text='站点关键词'
    )
    allow_registration = models.BooleanField(
        default=True,
        help_text='允许用户注册'
    )
    require_approval = models.BooleanField(
        default=False,
        help_text='新用户需要审核'
    )
    enable_comments = models.BooleanField(
        default=True,
        help_text='允许评论'
    )
    moderate_comments = models.BooleanField(
        default=False,
        help_text='评论需要审核'
    )
    enable_ratings = models.BooleanField(
        default=True,
        help_text='允许评分'
    )
    enable_reporting = models.BooleanField(
        default=True,
        help_text='允许举报'
    )
    
    # ==================== 上传设置 ====================
    max_file_size = models.IntegerField(
        default=1024,
        help_text='最大文件大小(MB)'
    )
    allowed_video_formats = models.CharField(
        max_length=200,
        default='mp4,avi,mov,mkv,flv',
        help_text='允许的视频格式'
    )
    allowed_image_formats = models.CharField(
        max_length=200,
        default='jpg,jpeg,png,gif,webp',
        help_text='允许的图片格式'
    )
    allowed_audio_formats = models.CharField(
        max_length=200,
        default='mp3,wav,ogg,flac',
        help_text='允许的音频格式'
    )
    auto_encode = models.BooleanField(
        default=True,
        help_text='自动编码'
    )
    default_quality = models.CharField(
        max_length=20,
        default='medium',
        choices=[
            ('low', '低质量'),
            ('medium', '中等质量'),
            ('high', '高质量'),
            ('ultra', '超高质量')
        ],
        help_text='默认编码质量'
    )
    generate_thumbnails = models.BooleanField(
        default=True,
        help_text='生成缩略图'
    )
    
    # ==================== 安全设置 ====================
    enable_captcha = models.BooleanField(
        default=False,
        help_text='启用验证码'
    )
    max_login_attempts = models.IntegerField(
        default=5,
        help_text='最大登录尝试次数'
    )
    lockout_duration = models.IntegerField(
        default=15,
        help_text='登录锁定时间(分钟)'
    )
    enable_moderation = models.BooleanField(
        default=True,
        help_text='启用内容审核'
    )
    enable_word_filter = models.BooleanField(
        default=True,
        help_text='敏感词过滤'
    )
    allowed_domains = models.TextField(
        default='http://localhost:5173\nhttp://localhost:5174',
        help_text='允许的域名(跨域),每行一个'
    )
    
    # ==================== 邮件设置 ====================
    enable_email = models.BooleanField(
        default=False,
        help_text='启用邮件发送'
    )
    smtp_host = models.CharField(
        max_length=200,
        default='smtp.gmail.com',
        help_text='SMTP服务器'
    )
    smtp_port = models.IntegerField(
        default=587,
        help_text='SMTP端口'
    )
    from_email = models.EmailField(
        default='noreply@mediacms.io',
        help_text='发件人邮箱'
    )
    from_name = models.CharField(
        max_length=100,
        default='MediaCMS',
        help_text='发件人名称'
    )
    use_tls = models.BooleanField(
        default=True,
        help_text='使用TLS'
    )
    send_welcome_email = models.BooleanField(
        default=True,
        help_text='注册欢迎邮件'
    )
    send_comment_notification = models.BooleanField(
        default=True,
        help_text='评论通知邮件'
    )
    send_like_notification = models.BooleanField(
        default=False,
        help_text='点赞通知邮件'
    )
    
    # ==================== 功能开关（新增）====================
    login_allowed = models.BooleanField(
        default=True,
        help_text='显示登录按钮'
    )
    register_allowed = models.BooleanField(
        default=True,
        help_text='显示注册按钮'
    )
    upload_media_allowed = models.BooleanField(
        default=True,
        help_text='显示上传按钮'
    )
    can_like_media = models.BooleanField(
        default=True,
        help_text='显示点赞按钮'
    )
    can_dislike_media = models.BooleanField(
        default=True,
        help_text='显示踩按钮'
    )
    can_report_media = models.BooleanField(
        default=True,
        help_text='显示举报按钮'
    )
    can_share_media = models.BooleanField(
        default=True,
        help_text='显示分享按钮'
    )
    timestamp_in_timebar = models.BooleanField(
        default=False,
        help_text='时间戳评论显示在时间轴'
    )
    allow_mention_in_comments = models.BooleanField(
        default=False,
        help_text='允许@提及用户'
    )
    allow_video_trimmer = models.BooleanField(
        default=True,
        help_text='允许视频剪辑'
    )
    allow_custom_media_urls = models.BooleanField(
        default=False,
        help_text='允许自定义媒体URL'
    )
    generate_sitemap = models.BooleanField(
        default=False,
        help_text='生成站点地图'
    )
    load_from_cdn = models.BooleanField(
        default=False,
        help_text='从CDN加载静态资源'
    )
    global_login_required = models.BooleanField(
        default=False,
        help_text='需要登录才能访问整个站点'
    )
    show_original_media = models.BooleanField(
        default=True,
        help_text='显示原始文件链接'
    )
    
    # ==================== 用户权限（新增）====================
    can_add_media = models.CharField(
        max_length=20,
        default='all',
        choices=[
            ('all', '所有人'),
            ('email_verified', '已验证邮箱'),
            ('advancedUser', '高级用户')
        ],
        help_text='谁可以上传媒体'
    )
    can_comment = models.CharField(
        max_length=20,
        default='all',
        choices=[
            ('all', '所有人'),
            ('email_verified', '已验证邮箱'),
            ('advancedUser', '高级用户')
        ],
        help_text='谁可以评论'
    )
    can_see_members_page = models.CharField(
        max_length=20,
        default='all',
        choices=[
            ('all', '所有人'),
            ('editors', '编辑'),
            ('admins', '管理员')
        ],
        help_text='谁可以查看会员页面'
    )
    users_needs_to_be_approved = models.BooleanField(
        default=False,
        help_text='新用户需要管理员批准'
    )
    allow_anonymous_user_listing = models.BooleanField(
        default=True,
        help_text='匿名用户可列出所有用户'
    )
    allow_anonymous_actions = models.CharField(
        max_length=200,
        default='report,like,dislike,watch',
        help_text='允许匿名用户的操作（逗号分隔）'
    )
    time_to_action_anonymous = models.IntegerField(
        default=600,
        help_text='匿名用户操作限制间隔（秒）'
    )
    number_of_media_user_can_upload = models.IntegerField(
        default=100,
        help_text='用户最大上传媒体数量'
    )
    
    # ==================== 内容管理（新增）====================
    reported_times_threshold = models.IntegerField(
        default=10,
        help_text='举报多少次后自动设为私有'
    )
    max_chars_for_comment = models.IntegerField(
        default=10000,
        help_text='评论最大字符数'
    )
    max_media_per_playlist = models.IntegerField(
        default=70,
        help_text='播放列表最大媒体数'
    )
    related_media_strategy = models.CharField(
        max_length=20,
        default='content',
        choices=[
            ('content', '按内容'),
            ('author', '按作者')
        ],
        help_text='相关媒体推荐策略'
    )
    default_theme = models.CharField(
        max_length=20,
        default='light',
        choices=[
            ('light', '亮色'),
            ('dark', '暗色')
        ],
        help_text='默认主题'
    )
    use_rounded_corners = models.BooleanField(
        default=True,
        help_text='使用圆角UI'
    )
    video_player_featured_video_on_index = models.BooleanField(
        default=False,
        help_text='首页显示特色视频播放器'
    )
    pre_upload_media_message = models.TextField(
        default='',
        blank=True,
        help_text='上传前提示消息'
    )
    cannot_add_media_message = models.TextField(
        default='User cannot add media, or maximum number of media uploads has been reached.',
        help_text='无法上传时的提示消息'
    )
    sidebar_footer_text = models.TextField(
        default='',
        blank=True,
        help_text='侧边栏页脚文本'
    )
    
    # ==================== 编码设置（新增）====================
    do_not_transcode_video = models.BooleanField(
        default=False,
        help_text='禁用视频转码（仅显示原始文件）'
    )
    ffmpeg_default_preset = models.CharField(
        max_length=20,
        default='medium',
        choices=[
            ('ultrafast', '极快'),
            ('superfast', '超快'),
            ('veryfast', '很快'),
            ('faster', '较快'),
            ('fast', '快'),
            ('medium', '中等'),
            ('slow', '慢'),
            ('slower', '较慢'),
            ('veryslow', '很慢'),
        ],
        help_text='FFmpeg编码预设'
    )
    chunkize_video_duration = models.IntegerField(
        default=300,
        help_text='视频分块时长（秒）'
    )
    video_chunks_duration = models.IntegerField(
        default=240,
        help_text='每个分块持续时间（秒）'
    )
    minimum_resolutions_to_encode = models.CharField(
        max_length=100,
        default='144,240',
        help_text='最小编码分辨率（逗号分隔）'
    )
    sprite_num_secs = models.IntegerField(
        default=10,
        help_text='精灵图间隔（秒）'
    )
    slideshow_items = models.IntegerField(
        default=30,
        help_text='幻灯片展示图片数量'
    )
    calculate_md5sum = models.BooleanField(
        default=False,
        help_text='计算上传文件的MD5校验和'
    )
    
    # ==================== UI配置（新增）====================
    portal_logo_dark_svg = models.CharField(
        max_length=200,
        default='/static/images/logo_dark.svg',
        help_text='暗色Logo SVG路径'
    )
    portal_logo_light_svg = models.CharField(
        max_length=200,
        default='/static/images/logo_light.svg',
        help_text='亮色Logo SVG路径'
    )
    extra_css_paths = models.TextField(
        default='',
        blank=True,
        help_text='额外CSS文件路径（每行一个）'
    )
    portal_workflow = models.CharField(
        max_length=20,
        default='public',
        choices=[
            ('public', '公开'),
            ('private', '私有'),
            ('unlisted', '不列出')
        ],
        help_text='门户工作流模式'
    )
    time_zone = models.CharField(
        max_length=50,
        default='Asia/Shanghai',
        help_text='系统时区'
    )
    language_code = models.CharField(
        max_length=10,
        default='zh-hans',
        choices=[
            ('en', 'English'),
            ('zh-hans', '简体中文'),
            ('zh-hant', '繁体中文'),
            ('ja', '日本語'),
            ('ko', '한국어'),
            ('es', 'Español'),
            ('fr', 'Français'),
            ('de', 'Deutsch'),
            ('ru', 'Русский'),
            ('ar', 'العربية'),
        ],
        help_text='默认语言'
    )
    
    # ==================== 元数据 ====================
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='最后更新者'
    )
    
    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'
    
    def __str__(self):
        return f"系统设置 (更新于: {self.last_updated})"
    
    @classmethod
    def get_settings(cls):
        """获取系统设置（单例模式）"""
        # 先从缓存获取
        settings = cache.get('system_settings')
        if settings:
            return settings
        
        # 从数据库获取或创建
        settings, created = cls.objects.get_or_create(pk=1)
        
        # 缓存设置（1小时）
        cache.set('system_settings', settings, 3600)
        
        return settings
    
    def save(self, *args, **kwargs):
        """保存时清除缓存"""
        super().save(*args, **kwargs)
        cache.delete('system_settings')
    
    def to_dict(self):
        """转换为字典（分类）"""
        return {
            # 基本设置
            'basic': {
                'siteName': self.site_name,
                'siteDescription': self.site_description,
                'siteKeywords': self.site_keywords,
                'allowRegistration': self.allow_registration,
                'requireApproval': self.require_approval,
                'enableComments': self.enable_comments,
                'moderateComments': self.moderate_comments,
                'enableRatings': self.enable_ratings,
                'enableReporting': self.enable_reporting,
            },
            # 上传设置
            'upload': {
                'maxFileSize': self.max_file_size,
                'allowedVideoFormats': self.allowed_video_formats,
                'allowedImageFormats': self.allowed_image_formats,
                'allowedAudioFormats': self.allowed_audio_formats,
                'autoEncode': self.auto_encode,
                'defaultQuality': self.default_quality,
                'generateThumbnails': self.generate_thumbnails,
            },
            # 安全设置
            'security': {
                'enableCaptcha': self.enable_captcha,
                'maxLoginAttempts': self.max_login_attempts,
                'lockoutDuration': self.lockout_duration,
                'enableModeration': self.enable_moderation,
                'enableWordFilter': self.enable_word_filter,
                'allowedDomains': self.allowed_domains,
            },
            # 邮件设置
            'email': {
                'enableEmail': self.enable_email,
                'smtpHost': self.smtp_host,
                'smtpPort': self.smtp_port,
                'fromEmail': self.from_email,
                'fromName': self.from_name,
                'useTLS': self.use_tls,
                'sendWelcomeEmail': self.send_welcome_email,
                'sendCommentNotification': self.send_comment_notification,
                'sendLikeNotification': self.send_like_notification,
            },
            # 功能开关
            'features': {
                'loginAllowed': self.login_allowed,
                'registerAllowed': self.register_allowed,
                'uploadMediaAllowed': self.upload_media_allowed,
                'canLikeMedia': self.can_like_media,
                'canDislikeMedia': self.can_dislike_media,
                'canReportMedia': self.can_report_media,
                'canShareMedia': self.can_share_media,
                'timestampInTimebar': self.timestamp_in_timebar,
                'allowMentionInComments': self.allow_mention_in_comments,
                'allowVideoTrimmer': self.allow_video_trimmer,
                'allowCustomMediaUrls': self.allow_custom_media_urls,
                'generateSitemap': self.generate_sitemap,
                'loadFromCdn': self.load_from_cdn,
                'globalLoginRequired': self.global_login_required,
                'showOriginalMedia': self.show_original_media,
            },
            # 用户权限
            'permissions': {
                'canAddMedia': self.can_add_media,
                'canComment': self.can_comment,
                'canSeeMembersPage': self.can_see_members_page,
                'usersNeedsToBeApproved': self.users_needs_to_be_approved,
                'allowAnonymousUserListing': self.allow_anonymous_user_listing,
                'allowAnonymousActions': self.allow_anonymous_actions,
                'timeToActionAnonymous': self.time_to_action_anonymous,
                'numberOfMediaUserCanUpload': self.number_of_media_user_can_upload,
            },
            # 内容管理
            'content': {
                'reportedTimesThreshold': self.reported_times_threshold,
                'maxCharsForComment': self.max_chars_for_comment,
                'maxMediaPerPlaylist': self.max_media_per_playlist,
                'relatedMediaStrategy': self.related_media_strategy,
                'defaultTheme': self.default_theme,
                'useRoundedCorners': self.use_rounded_corners,
                'videoPlayerFeaturedVideoOnIndex': self.video_player_featured_video_on_index,
                'preUploadMediaMessage': self.pre_upload_media_message,
                'cannotAddMediaMessage': self.cannot_add_media_message,
                'sidebarFooterText': self.sidebar_footer_text,
            },
            # 编码设置
            'encoding': {
                'doNotTranscodeVideo': self.do_not_transcode_video,
                'ffmpegDefaultPreset': self.ffmpeg_default_preset,
                'chunkizeVideoDuration': self.chunkize_video_duration,
                'videoChunksDuration': self.video_chunks_duration,
                'minimumResolutionsToEncode': self.minimum_resolutions_to_encode,
                'spriteNumSecs': self.sprite_num_secs,
                'slideshowItems': self.slideshow_items,
                'calculateMd5sum': self.calculate_md5sum,
            },
            # UI配置
            'ui': {
                'portalLogoDarkSvg': self.portal_logo_dark_svg,
                'portalLogoLightSvg': self.portal_logo_light_svg,
                'extraCssPaths': self.extra_css_paths,
                'portalWorkflow': self.portal_workflow,
                'timeZone': self.time_zone,
                'languageCode': self.language_code,
            },
            # 元数据
            'meta': {
                'lastUpdated': self.last_updated.isoformat() if self.last_updated else None,
                'updatedBy': self.updated_by.username if self.updated_by else None,
            }
        }

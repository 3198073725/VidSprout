"""
系统管理API视图
"""
import platform
import psutil
import sys
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from files.permissions import IsMediacmsManager
from files.models.system_settings import SystemSettings


class SystemSettingsView(APIView):
    """系统设置API"""
    
    permission_classes = (IsMediacmsManager,)
    
    def get(self, request):
        """获取系统设置"""
        try:
            settings_obj = SystemSettings.get_settings()
            return Response(settings_obj.to_dict())
        except Exception as e:
            return Response(
                {'detail': f'获取设置失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        """更新系统设置"""
        try:
            settings_obj = SystemSettings.get_settings()
            data = request.data
            
            # 更新基本设置
            if 'basic' in data:
                basic = data['basic']
                settings_obj.site_name = basic.get('siteName', settings_obj.site_name)
                settings_obj.site_description = basic.get('siteDescription', settings_obj.site_description)
                settings_obj.site_keywords = basic.get('siteKeywords', settings_obj.site_keywords)
                settings_obj.allow_registration = basic.get('allowRegistration', settings_obj.allow_registration)
                settings_obj.require_approval = basic.get('requireApproval', settings_obj.require_approval)
                settings_obj.enable_comments = basic.get('enableComments', settings_obj.enable_comments)
                settings_obj.moderate_comments = basic.get('moderateComments', settings_obj.moderate_comments)
                settings_obj.enable_ratings = basic.get('enableRatings', settings_obj.enable_ratings)
                settings_obj.enable_reporting = basic.get('enableReporting', settings_obj.enable_reporting)
            
            # 更新上传设置
            if 'upload' in data:
                upload = data['upload']
                settings_obj.max_file_size = upload.get('maxFileSize', settings_obj.max_file_size)
                settings_obj.allowed_video_formats = upload.get('allowedVideoFormats', settings_obj.allowed_video_formats)
                settings_obj.allowed_image_formats = upload.get('allowedImageFormats', settings_obj.allowed_image_formats)
                settings_obj.allowed_audio_formats = upload.get('allowedAudioFormats', settings_obj.allowed_audio_formats)
                settings_obj.auto_encode = upload.get('autoEncode', settings_obj.auto_encode)
                settings_obj.default_quality = upload.get('defaultQuality', settings_obj.default_quality)
                settings_obj.generate_thumbnails = upload.get('generateThumbnails', settings_obj.generate_thumbnails)
            
            # 更新安全设置
            if 'security' in data:
                security = data['security']
                settings_obj.enable_captcha = security.get('enableCaptcha', settings_obj.enable_captcha)
                settings_obj.max_login_attempts = security.get('maxLoginAttempts', settings_obj.max_login_attempts)
                settings_obj.lockout_duration = security.get('lockoutDuration', settings_obj.lockout_duration)
                settings_obj.enable_moderation = security.get('enableModeration', settings_obj.enable_moderation)
                settings_obj.enable_word_filter = security.get('enableWordFilter', settings_obj.enable_word_filter)
                settings_obj.allowed_domains = security.get('allowedDomains', settings_obj.allowed_domains)
            
            # 更新邮件设置
            if 'email' in data:
                email = data['email']
                settings_obj.enable_email = email.get('enableEmail', settings_obj.enable_email)
                settings_obj.smtp_host = email.get('smtpHost', settings_obj.smtp_host)
                settings_obj.smtp_port = email.get('smtpPort', settings_obj.smtp_port)
                settings_obj.from_email = email.get('fromEmail', settings_obj.from_email)
                settings_obj.from_name = email.get('fromName', settings_obj.from_name)
                settings_obj.use_tls = email.get('useTLS', settings_obj.use_tls)
                settings_obj.send_welcome_email = email.get('sendWelcomeEmail', settings_obj.send_welcome_email)
                settings_obj.send_comment_notification = email.get('sendCommentNotification', settings_obj.send_comment_notification)
                settings_obj.send_like_notification = email.get('sendLikeNotification', settings_obj.send_like_notification)
            
            # 更新功能开关（第一阶段新增）
            if 'features' in data:
                features = data['features']
                settings_obj.login_allowed = features.get('loginAllowed', settings_obj.login_allowed)
                settings_obj.register_allowed = features.get('registerAllowed', settings_obj.register_allowed)
                settings_obj.upload_media_allowed = features.get('uploadMediaAllowed', settings_obj.upload_media_allowed)
                settings_obj.can_like_media = features.get('canLikeMedia', settings_obj.can_like_media)
                settings_obj.can_dislike_media = features.get('canDislikeMedia', settings_obj.can_dislike_media)
                settings_obj.can_report_media = features.get('canReportMedia', settings_obj.can_report_media)
                settings_obj.can_share_media = features.get('canShareMedia', settings_obj.can_share_media)
                settings_obj.timestamp_in_timebar = features.get('timestampInTimebar', settings_obj.timestamp_in_timebar)
                settings_obj.allow_mention_in_comments = features.get('allowMentionInComments', settings_obj.allow_mention_in_comments)
                settings_obj.allow_video_trimmer = features.get('allowVideoTrimmer', settings_obj.allow_video_trimmer)
                settings_obj.allow_custom_media_urls = features.get('allowCustomMediaUrls', settings_obj.allow_custom_media_urls)
                settings_obj.generate_sitemap = features.get('generateSitemap', settings_obj.generate_sitemap)
                settings_obj.load_from_cdn = features.get('loadFromCdn', settings_obj.load_from_cdn)
                settings_obj.global_login_required = features.get('globalLoginRequired', settings_obj.global_login_required)
                settings_obj.show_original_media = features.get('showOriginalMedia', settings_obj.show_original_media)
            
            # 更新用户权限（第一阶段新增）
            if 'permissions' in data:
                permissions = data['permissions']
                settings_obj.can_add_media = permissions.get('canAddMedia', settings_obj.can_add_media)
                settings_obj.can_comment = permissions.get('canComment', settings_obj.can_comment)
                settings_obj.can_see_members_page = permissions.get('canSeeMembersPage', settings_obj.can_see_members_page)
                settings_obj.users_needs_to_be_approved = permissions.get('usersNeedsToBeApproved', settings_obj.users_needs_to_be_approved)
                settings_obj.allow_anonymous_user_listing = permissions.get('allowAnonymousUserListing', settings_obj.allow_anonymous_user_listing)
                settings_obj.allow_anonymous_actions = permissions.get('allowAnonymousActions', settings_obj.allow_anonymous_actions)
                settings_obj.time_to_action_anonymous = permissions.get('timeToActionAnonymous', settings_obj.time_to_action_anonymous)
                settings_obj.number_of_media_user_can_upload = permissions.get('numberOfMediaUserCanUpload', settings_obj.number_of_media_user_can_upload)
            
            # 保存并记录更新者
            settings_obj.updated_by = request.user
            settings_obj.save()
            
            return Response(settings_obj.to_dict())
            
        except Exception as e:
            return Response(
                {'detail': f'保存设置失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([IsMediacmsManager])
def get_system_monitoring(request):
    """获取系统监控数据"""
    try:
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # 网络流量
        network = psutil.net_io_counters()
        
        # 系统信息
        uptime_seconds = (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
        uptime_days = int(uptime_seconds // 86400)
        uptime_hours = int((uptime_seconds % 86400) // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        
        system_info = {
            'cpu': round(cpu_percent, 1),
            'memory': round(memory_percent, 1),
            'disk': round(disk_percent, 1),
            'network': round((network.bytes_sent + network.bytes_recv) / 1024 / 1024, 2),  # MB
            'uploadSpeed': round(network.bytes_sent / 1024 / 1024, 2),  # MB
            'downloadSpeed': round(network.bytes_recv / 1024 / 1024, 2),  # MB
        }
        
        system_details = {
            'os': f'{platform.system()} {platform.release()}',
            'hostname': platform.node(),
            'pythonVersion': platform.python_version(),
            'djangoVersion': __import__('django').get_version(),
            'uptime': f'{uptime_days} 天 {uptime_hours} 小时 {uptime_minutes} 分钟',
            'database': settings.DATABASES['default']['ENGINE'].split('.')[-1],
        }
        
        # 进程信息
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                # 只显示相关的进程
                if any(keyword in info['name'].lower() for keyword in ['python', 'gunicorn', 'celery', 'redis', 'postgres', 'mysql']):
                    processes.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'cpu': round(info['cpu_percent'] or 0, 2),
                        'memory': round(info['memory_percent'] or 0, 2),
                        'status': info['status'] if info['status'] else 'unknown'
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # 限制进程数量
        processes = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:10]
        
        # 生成趋势数据（过去24小时，每小时一个数据点）
        now = datetime.now()
        trend_data = []
        for i in range(24):
            time_point = now - timedelta(hours=23-i)
            trend_data.append({
                'date': time_point.strftime('%H:%M'),
                'count': round(cpu_percent + (i % 5 - 2) * 5, 1)  # 模拟历史数据
            })
        
        return Response({
            'systemInfo': system_info,
            'systemDetails': system_details,
            'processes': processes,
            'trendData': trend_data,
        })
        
    except Exception as e:
        return Response(
            {'detail': f'获取监控数据失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsMediacmsManager])
def test_email(request):
    """测试邮件发送"""
    try:
        settings_obj = SystemSettings.get_settings()
        
        if not settings_obj.enable_email:
            return Response(
                {'detail': '邮件功能未启用'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 发送测试邮件
        recipient_email = request.data.get('email', request.user.email)
        
        subject = f'[{settings_obj.site_name}] 测试邮件'
        message = f'''
        您好,

        这是一封来自 {settings_obj.site_name} 的测试邮件。

        如果您收到这封邮件，说明邮件配置正确。

        ---
        发送时间: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        '''
        
        send_mail(
            subject,
            message,
            settings_obj.from_email,
            [recipient_email],
            fail_silently=False,
        )
        
        return Response({
            'detail': f'测试邮件已发送到 {recipient_email}'
        })
        
    except Exception as e:
        return Response(
            {'detail': f'发送测试邮件失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


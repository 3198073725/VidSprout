"""
联系表单API视图
"""
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact_form(request):
    """
    处理联系表单提交
    
    接收参数：
    - name: 姓名
    - email: 邮箱
    - subject: 主题
    - message: 消息内容
    """
    try:
        name = request.data.get('name', '').strip()
        email = request.data.get('email', '').strip()
        subject = request.data.get('subject', '未指定主题').strip()
        message = request.data.get('message', '').strip()
        
        # 验证必填字段
        if not name:
            return Response(
                {'detail': '请提供姓名'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not email:
            return Response(
                {'detail': '请提供邮箱地址'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not message:
            return Response(
                {'detail': '请提供消息内容'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 构建邮件内容
        email_subject = f'[MediaCMS 联系表单] {subject}'
        email_body = f"""
收到来自网站联系表单的新消息：

姓名：{name}
邮箱：{email}
主题：{subject}

消息内容：
{message}

---
此邮件由 MediaCMS 自动发送
        """
        
        # 发送邮件（如果配置了邮件服务器）
        try:
            admin_emails = [admin[1] for admin in settings.ADMINS] if hasattr(settings, 'ADMINS') and settings.ADMINS else []
            
            if not admin_emails:
                # 如果没有配置管理员邮箱，使用默认邮箱
                admin_emails = [getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@localhost')]
            
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@mediacms.io'),
                recipient_list=admin_emails,
                fail_silently=False,
            )
            
            logger.info(f'联系表单提交成功：{name} ({email})')
            
            return Response(
                {'detail': '消息已成功发送，我们会尽快回复您！'},
                status=status.HTTP_200_OK
            )
            
        except Exception as email_error:
            # 邮件发送失败，记录日志但不返回错误
            logger.warning(f'联系表单邮件发送失败：{str(email_error)}')
            
            # 即使邮件发送失败，也记录到日志供管理员查看
            logger.info(f'联系表单（邮件发送失败但已记录）：\n姓名：{name}\n邮箱：{email}\n主题：{subject}\n消息：{message}')
            
            return Response(
                {'detail': '消息已接收，我们会尽快处理'},
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.error(f'处理联系表单时出错：{str(e)}')
        return Response(
            {'detail': '提交失败，请稍后重试'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


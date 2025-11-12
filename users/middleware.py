"""
用户状态检查中间件
检查已登录用户是否被封禁
"""
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class UserActiveCheckMiddleware(MiddlewareMixin):
    """
    检查已认证用户是否处于活跃状态
    如果用户被封禁（is_active=False），返回403错误
    """
    
    def process_request(self, request):
        # 只检查 API 请求
        if not request.path.startswith('/api/'):
            return None
        
        # 跳过登录、注册等不需要认证的端点
        skip_paths = [
            '/api/v1/login',
            '/api/v1/register',
            '/api/v1/media',  # 公开的媒体列表
            '/api/v1/categories',
            '/api/v1/tags',
            '/api/v1/search',
        ]
        
        # 检查是否是需要跳过的路径
        for skip_path in skip_paths:
            if request.path.startswith(skip_path):
                return None
        
        # 检查用户是否已认证
        if hasattr(request, 'user') and request.user.is_authenticated:
            # 检查用户是否被封禁
            if not request.user.is_active:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f'Blocked user attempted API access: {request.user.username} - {request.path}')
                
                return JsonResponse(
                    {
                        'detail': '您的账号已被封禁，请联系管理员',
                        'message': '您的账号已被封禁，请联系管理员',
                        'code': 'user_blocked',
                        'blocked': True,
                        'non_field_errors': ['您的账号已被封禁，请联系管理员']
                    },
                    status=403
                )
        
        return None


"""
自定义认证类
"""
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.authtoken.models import Token
from cms.permissions import UserBlockedException


class TokenAuthentication(BaseTokenAuthentication):
    """
    自定义 Token 认证类，在用户被封禁时返回自定义错误响应
    """
    
    def authenticate_credentials(self, key):
        # 直接查询token，绕过父类的is_active检查
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            from rest_framework import exceptions
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        # 获取用户
        user = token.user
        
        # 检查用户是否被封禁（在抛出自定义异常前检查）
        if not user.is_active:
            # 抛出自定义的封禁异常
            raise UserBlockedException()
        
        return (user, token)


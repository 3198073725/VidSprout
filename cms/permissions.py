"""
自定义权限类
"""
from django.conf import settings
from rest_framework import permissions
from rest_framework.exceptions import APIException


class UserBlockedException(APIException):
    """用户被封禁异常"""
    status_code = 403
    default_detail = '您的账号已被封禁，请联系管理员'
    default_code = 'user_blocked'
    
    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail
        
        # 创建详细的错误响应
        self.detail = {
            'detail': detail,
            'message': detail,
            'code': 'user_blocked',
            'blocked': True,
            'non_field_errors': [detail]
        }


class IsActiveUser(permissions.IsAuthenticated):
    """
    检查用户是否已认证且处于活跃状态
    如果用户被封禁，返回自定义的错误响应
    """
    
    def has_permission(self, request, view):
        # 首先检查用户是否已认证
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查用户是否被封禁
        if not request.user.is_active:
            # 抛出自定义的封禁异常
            raise UserBlockedException()
        
        return True


class IsUserOrManager(permissions.BasePermission):
    """检查是否是用户本人或管理员"""
    
    def has_permission(self, request, view):
        # 用户必须已认证
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查是否被封禁
        if not request.user.is_active:
            raise UserBlockedException()
        
        return True
    
    def has_object_permission(self, request, view, obj):
        from files.methods import is_mediacms_manager
        
        # 管理员可以访问所有对象
        if is_mediacms_manager(request.user):
            return True
        
        # 用户只能访问自己的对象
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        
        # 如果对象就是用户本身
        if obj == request.user:
            return True
        
        return False


class IsAuthorizedToAdd(permissions.BasePermission):
    """检查用户是否被授权添加媒体"""
    
    def has_permission(self, request, view):
        from files.methods import user_allowed_to_upload
        
        # GET 请求不需要检查
        if request.method == 'GET':
            return True
        
        # POST/PUT/PATCH/DELETE 需要检查上传权限
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查是否被封禁
        if not request.user.is_active:
            raise UserBlockedException()
        
        return user_allowed_to_upload(request)


class IsAuthorizedToAddComment(permissions.BasePermission):
    """检查用户是否被授权添加评论"""
    
    def has_permission(self, request, view):
        # GET 请求不需要检查
        if request.method == 'GET':
            return True
        
        # POST/PUT/PATCH/DELETE 需要检查评论权限
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查是否被封禁
        if not request.user.is_active:
            raise UserBlockedException()
        
        # 检查评论权限设置
        can_comment = getattr(settings, 'CAN_COMMENT', 'all')
        
        if can_comment == "all":
            return True
        elif can_comment == "email_verified":
            return getattr(request.user, 'email_is_verified', False)
        elif can_comment == "advancedUser":
            return getattr(request.user, 'advancedUser', False)
        
        return False


class IsUserOrEditor(permissions.BasePermission):
    """检查是否是用户本人或编辑"""
    
    def has_permission(self, request, view):
        # GET 请求允许所有人（包括匿名用户）
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # POST/PUT/PATCH/DELETE 请求需要认证
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查是否被封禁
        if not request.user.is_active:
            raise UserBlockedException()
        
        return True
    
    def has_object_permission(self, request, view, obj):
        from files.methods import is_mediacms_editor
        
        # GET/HEAD/OPTIONS 请求允许所有人（用于查看公开内容）
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 对于修改操作，编辑可以访问所有对象
        if is_mediacms_editor(request.user):
            return True
        
        # 用户只能修改自己的对象
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        
        return False

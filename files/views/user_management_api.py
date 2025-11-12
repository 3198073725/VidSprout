"""
用户管理API
提供用户的增删改查、封禁解封、角色设置等功能
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import User
from users.serializers import AdminUserSerializer
from files.permissions import IsMediacmsManager, IsMediacmsEditor
from files.methods import is_mediacms_manager


class UserDetailAPI(APIView):
    """单个用户的详情、更新、删除"""
    
    permission_classes = (IsMediacmsEditor,)
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        tags=['User Management'],
        operation_summary='获取用户详情',
        responses={200: AdminUserSerializer}
    )
    def get(self, request, user_id, format=None):
        """获取用户详情"""
        try:
            user = User.objects.get(id=user_id)
            serializer = AdminUserSerializer(user, context={"request": request})
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"detail": "用户不存在"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        tags=['User Management'],
        operation_summary='更新用户信息',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='姓名'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='描述'),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否活跃'),
                'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否超级管理员'),
                'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否管理员'),
                'is_manager': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否管理者'),
                'is_editor': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否编辑者'),
            }
        ),
        responses={200: AdminUserSerializer}
    )
    def patch(self, request, user_id, format=None):
        """更新用户信息"""
        # 调试日志
        print(f"PATCH 用户 {user_id}:")
        print(f"  request.user: {request.user}")
        print(f"  is_superuser: {request.user.is_superuser}")
        print(f"  is_staff: {request.user.is_staff}")
        print(f"  is_manager: {getattr(request.user, 'is_manager', False)}")
        print(f"  is_editor: {getattr(request.user, 'is_editor', False)}")
        print(f"  is_mediacms_manager: {is_mediacms_manager(request.user)}")
        
        if not is_mediacms_manager(request.user):
            print(f"  ❌ 权限检查失败！")
            return Response(
                {"detail": "无权限"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(id=user_id)
            
            # 允许更新的字段
            allowed_fields = [
                'name', 'description', 'is_active', 
                'is_superuser', 'is_staff', 'is_manager', 'is_editor'
            ]
            
            for field in allowed_fields:
                if field in request.data:
                    setattr(user, field, request.data[field])
            
            user.save()
            
            serializer = AdminUserSerializer(user, context={"request": request})
            return Response(serializer.data)
            
        except User.DoesNotExist:
            return Response(
                {"detail": "用户不存在"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        tags=['User Management'],
        operation_summary='删除用户',
        responses={204: '删除成功'}
    )
    def delete(self, request, user_id, format=None):
        """删除用户"""
        if not is_mediacms_manager(request.user):
            return Response(
                {"detail": "无权限"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(id=user_id)
            # 不允许删除自己
            if user.id == request.user.id:
                return Response(
                    {"detail": "不能删除自己"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except User.DoesNotExist:
            return Response(
                {"detail": "用户不存在"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UserActionAPI(APIView):
    """用户操作API（封禁、解封等）"""
    
    permission_classes = (IsMediacmsManager,)
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        tags=['User Management'],
        operation_summary='用户操作',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['action'],
            properties={
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['block', 'unblock'],
                    description='操作类型'
                ),
            }
        ),
        responses={200: '操作成功'}
    )
    def post(self, request, user_id, format=None):
        """执行用户操作"""
        action = request.data.get('action')
        
        try:
            user = User.objects.get(id=user_id)
            
            # 不允许操作自己
            if user.id == request.user.id:
                return Response(
                    {"detail": "不能操作自己"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if action == 'block':
                user.is_active = False
                user.save()
                return Response({"detail": "用户已封禁"})
                
            elif action == 'unblock':
                user.is_active = True
                user.save()
                return Response({"detail": "用户已解封"})
                
            else:
                return Response(
                    {"detail": "无效的操作类型"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except User.DoesNotExist:
            return Response(
                {"detail": "用户不存在"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UserBatchOperationsAPI(APIView):
    """用户批量操作API"""
    
    permission_classes = (IsMediacmsManager,)
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        tags=['User Management'],
        operation_summary='用户批量操作',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_ids', 'action'],
            properties={
                'user_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='用户ID列表'
                ),
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['delete', 'block', 'unblock', 'set_manager', 'set_editor', 'remove_role'],
                    description='操作类型'
                ),
            }
        ),
        responses={200: '操作成功'}
    )
    def post(self, request, format=None):
        """批量操作用户"""
        user_ids = request.data.get('user_ids', [])
        action = request.data.get('action')
        
        if not user_ids:
            return Response(
                {"detail": "用户ID列表不能为空"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 过滤掉当前用户
        users = User.objects.filter(id__in=user_ids).exclude(id=request.user.id)
        
        if action == 'delete':
            count = users.count()
            users.delete()
            return Response({"detail": f"已删除{count}个用户"})
            
        elif action == 'block':
            count = users.update(is_active=False)
            return Response({"detail": f"已封禁{count}个用户"})
            
        elif action == 'unblock':
            count = users.update(is_active=True)
            return Response({"detail": f"已解封{count}个用户"})
            
        elif action == 'set_manager':
            count = users.update(is_manager=True)
            return Response({"detail": f"已设置{count}个用户为管理者"})
            
        elif action == 'set_editor':
            count = users.update(is_editor=True)
            return Response({"detail": f"已设置{count}个用户为编辑者"})
            
        elif action == 'remove_role':
            count = users.update(is_manager=False, is_editor=False)
            return Response({"detail": f"已移除{count}个用户的角色"})
            
        else:
            return Response(
                {"detail": "无效的操作类型"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from actions.models import USER_MEDIA_ACTIONS, MediaAction

from ..models import Media
from ..serializers import MediaSerializer

VALID_USER_ACTIONS = [action for action, name in USER_MEDIA_ACTIONS]


class UserActions(APIView):
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='action', type=openapi.TYPE_STRING, in_=openapi.IN_PATH, description='action', required=True, enum=VALID_USER_ACTIONS),
        ],
        tags=['Users'],
        operation_summary='List user actions',
        operation_description='Lists user actions',
    )
    def get(self, request, action):
        media = []
        if action in VALID_USER_ACTIONS:
            if request.user.is_authenticated:
                media = Media.objects.select_related("user").filter(mediaactions__user=request.user, mediaactions__action=action).order_by("-mediaactions__action_date")
            elif request.session.session_key:
                media = (
                    Media.objects.select_related("user")
                    .filter(
                        mediaactions__session_key=request.session.session_key,
                        mediaactions__action=action,
                    )
                    .order_by("-mediaactions__action_date")
                )

        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        page = paginator.paginate_queryset(media, request)
        serializer = MediaSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='action', type=openapi.TYPE_STRING, in_=openapi.IN_PATH, description='action', required=True, enum=VALID_USER_ACTIONS),
        ],
        tags=['Users'],
        operation_summary='Delete all user actions',
        operation_description='Deletes all user actions of specified type (e.g., clear all watch history)',
    )
    def delete(self, request, action):
        """批量删除用户的指定类型操作记录"""
        if not request.user.is_authenticated:
            return Response(
                {"detail": "需要登录才能删除操作记录"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if action not in VALID_USER_ACTIONS:
            return Response(
                {"detail": "无效的操作类型"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 删除用户的所有指定操作记录
        deleted_count = MediaAction.objects.filter(
            user=request.user,
            action=action
        ).delete()
        
        return Response(
            {
                "detail": f"已删除 {deleted_count[0]} 条{action}记录",
                "count": deleted_count[0],
                "action": action
            },
            status=status.HTTP_200_OK
        )

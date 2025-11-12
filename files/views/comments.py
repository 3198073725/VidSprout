from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import (
    FileUploadParser,
    FormParser,
    JSONParser,
    MultiPartParser,
)
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from actions.models import CommentAction
from cms.permissions import IsAuthorizedToAddComment
from users.models import User

from ..methods import (
    check_comment_for_mention,
    is_mediacms_editor,
    notify_user_on_comment,
)
from ..models import Comment, Media
from ..serializers import CommentSerializer


class CommentList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorizedToAddComment)
    parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY, description='Page number'),
            openapi.Parameter(name='author', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY, description='username'),
        ],
        tags=['Comments'],
        operation_summary='Lists Comments',
        operation_description='Paginated listing of all comments',
        responses={
            200: openapi.Response('response description', CommentSerializer(many=True)),
        },
    )
    def get(self, request, format=None):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        comments = Comment.objects.filter(media__state="public").order_by("-add_date")
        comments = comments.prefetch_related("user")
        comments = comments.prefetch_related("media")
        params = self.request.query_params
        if "author" in params:
            author_param = params["author"].strip()
            user_queryset = User.objects.all()
            user = get_object_or_404(user_queryset, username=author_param)
            comments = comments.filter(user=user)

        page = paginator.paginate_queryset(comments, request)

        serializer = CommentSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class CommentDetail(APIView):
    """Comments related views
    Listings of comments for a media (GET)
    Create comment (POST)
    Delete comment (DELETE)
    """

    permission_classes = (IsAuthorizedToAddComment,)
    parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)

    def get_object(self, friendly_token):
        try:
            media = Media.objects.select_related("user").get(friendly_token=friendly_token)
            self.check_object_permissions(self.request, media)
            if media.state == "private" and self.request.user != media.user:
                return Response({"detail": "media is private"}, status=status.HTTP_400_BAD_REQUEST)
            return media
        except PermissionDenied:
            return Response({"detail": "bad permissions"}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response(
                {"detail": "media file does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='sort', 
                type=openapi.TYPE_STRING, 
                in_=openapi.IN_QUERY, 
                description='Sort order: newest, hottest, most_liked',
                enum=['newest', 'hottest', 'most_liked']
            ),
        ],
        tags=['Media'],
        operation_summary='List comments for a media',
        operation_description='Returns paginated comments with optional sorting',
    )
    def get(self, request, friendly_token):
        # list comments for a media
        media = self.get_object(friendly_token)
        if isinstance(media, Response):
            return media
        
        # 获取排序参数
        sort_by = request.query_params.get('sort', 'newest')
        
        # 基础查询
        comments = media.comments.filter().prefetch_related("user")
        
        # 根据排序参数进行排序
        if sort_by == 'newest':
            # 最新：按创建时间倒序
            comments = comments.order_by('-add_date')
        elif sort_by == 'hottest':
            # 最热：按回复数 + 点赞数排序
            from django.db.models import Count, Q
            
            # 为每个评论计算热度分数（回复数 * 2 + 点赞数）
            comments = comments.annotate(
                reply_count=Count('children'),
                like_count=Count('commentactions', filter=Q(commentactions__action='like'))
            ).order_by('-reply_count', '-like_count', '-add_date')
        elif sort_by == 'most_liked':
            # 最多点赞：按点赞数倒序
            from django.db.models import Count, Q
            comments = comments.annotate(
                like_count=Count('commentactions', filter=Q(commentactions__action='like'))
            ).order_by('-like_count', '-add_date')
        else:
            # 默认最新
            comments = comments.order_by('-add_date')
        
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[],
        tags=['Media'],
        operation_summary='to_be_written',
        operation_description='to_be_written',
    )
    def delete(self, request, friendly_token, uid=None):
        """Delete a comment
        Administrators, MediaCMS editors and managers,
        media owner, and comment owners, can delete a comment
        """
        if uid:
            try:
                comment = Comment.objects.get(uid=uid)
            except BaseException:
                return Response(
                    {"detail": "comment does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (comment.user == self.request.user) or comment.media.user == self.request.user or is_mediacms_editor(self.request.user):
                comment.delete()
            else:
                return Response({"detail": "bad permissions"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[],
        tags=['Media'],
        operation_summary='to_be_written',
        operation_description='to_be_written',
    )
    def post(self, request, friendly_token):
        """Create a comment"""
        media = self.get_object(friendly_token)
        if isinstance(media, Response):
            return media

        if not media.enable_comments:
            return Response(
                {"detail": "comments not allowed here"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user, media=media)
            if request.user != media.user:
                notify_user_on_comment(friendly_token=media.friendly_token)
            # here forward the comment to check if a user was mentioned
            if settings.ALLOW_MENTION_IN_COMMENTS:
                check_comment_for_mention(friendly_token=media.friendly_token, comment_text=serializer.data['text'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentLike(APIView):
    """Handle comment like/unlike actions"""
    
    permission_classes = (IsAuthorizedToAddComment,)
    parser_classes = (JSONParser,)
    
    def get_comment(self, uid):
        """Get comment by uid"""
        try:
            return Comment.objects.get(uid=uid)
        except Comment.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        tags=['Comments'],
        operation_summary='Like a comment',
        operation_description='Like or unlike a comment',
    )
    def post(self, request, uid):
        """Like a comment"""
        comment = self.get_comment(uid)
        if not comment:
            return Response(
                {"detail": "评论不存在"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查是否已经点赞
        existing_like = CommentAction.objects.filter(
            user=request.user,
            comment=comment,
            action='like'
        ).first()
        
        if existing_like:
            # 已点赞，取消点赞
            existing_like.delete()
            return Response({
                "detail": "已取消点赞",
                "action": "unlike"
            }, status=status.HTTP_200_OK)
        else:
            # 未点赞，创建点赞
            CommentAction.objects.create(
                user=request.user,
                comment=comment,
                action='like'
            )
            return Response({
                "detail": "点赞成功",
                "action": "like"
            }, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        tags=['Comments'],
        operation_summary='Unlike a comment',
        operation_description='Remove like from a comment',
    )
    def delete(self, request, uid):
        """Unlike a comment"""
        comment = self.get_comment(uid)
        if not comment:
            return Response(
                {"detail": "评论不存在"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 删除点赞
        deleted = CommentAction.objects.filter(
            user=request.user,
            comment=comment,
            action='like'
        ).delete()
        
        if deleted[0] > 0:
            return Response({
                "detail": "已取消点赞"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "未点赞过该评论"
            }, status=status.HTTP_400_BAD_REQUEST)

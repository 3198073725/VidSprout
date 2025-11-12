"""
管理员专用 API 视图
提供仪表板统计、系统监控、批量操作等管理功能
"""
from django.conf import settings
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from users.serializers import UserSerializer
from files.models import Media, Comment, Category
from files.serializers import MediaSerializer, CommentSerializer
from files.permissions import IsMediacmsManager, IsMediacmsEditor
from files.methods import is_mediacms_manager


class DashboardStatsView(APIView):
    """仪表板统计数据"""
    
    permission_classes = (IsMediacmsEditor,)
    
    @swagger_auto_schema(
        operation_summary='获取仪表板统计数据',
        operation_description='返回系统总体统计信息',
        tags=['Admin'],
    )
    def get(self, request):
        # 基础统计
        total_media = Media.objects.count()
        total_users = User.objects.count()
        total_comments = Comment.objects.count()
        
        # 今日新增
        today = timezone.now().date()
        today_media = Media.objects.filter(add_date__date=today).count()
        today_users = User.objects.filter(date_joined__date=today).count()
        
        # 近7天新增（用于趋势计算）
        week_ago = timezone.now() - timedelta(days=7)
        week_media = Media.objects.filter(add_date__gte=week_ago).count()
        week_users = User.objects.filter(date_joined__gte=week_ago).count()
        
        # 计算趋势（相对于前一周）
        prev_week = timezone.now() - timedelta(days=14)
        prev_week_media = Media.objects.filter(
            add_date__gte=prev_week, 
            add_date__lt=week_ago
        ).count()
        prev_week_users = User.objects.filter(
            date_joined__gte=prev_week, 
            date_joined__lt=week_ago
        ).count()
        
        media_trend = ((week_media - prev_week_media) / prev_week_media * 100) if prev_week_media > 0 else 0
        users_trend = ((week_users - prev_week_users) / prev_week_users * 100) if prev_week_users > 0 else 0
        
        # 总观看数和点赞数
        total_views = Media.objects.aggregate(Sum('views'))['views__sum'] or 0
        total_likes = Media.objects.aggregate(Sum('likes'))['likes__sum'] or 0
        
        # 媒体类型分布
        media_by_type = list(Media.objects.values('media_type').annotate(
            count=Count('id'),
            total_views=Sum('views')
        ))
        
        # 编码状态统计
        encoding_stats = list(Media.objects.values('encoding_status').annotate(
            count=Count('id')
        ))
        
        # 近30天的趋势数据
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_stats = []
        for i in range(30):
            day = timezone.now().date() - timedelta(days=29-i)
            media_count = Media.objects.filter(add_date__date=day).count()
            views_count = Media.objects.filter(add_date__date=day).aggregate(Sum('views'))['views__sum'] or 0
            daily_stats.append({
                'date': day.strftime('%Y-%m-%d'),
                'media': media_count,
                'views': views_count
            })
        
        # 待审核内容统计
        pending_media = Media.objects.filter(is_reviewed=False).count()
        reported_media = Media.objects.filter(reported_times__gt=0).count()
        
        # 活跃用户（近7天有上传或评论的用户）
        active_users = User.objects.filter(
            Q(media__add_date__gte=week_ago) | 
            Q(comment__add_date__gte=week_ago)
        ).distinct().count()
        
        return Response({
            'overview': {
                'total_media': total_media,
                'total_users': total_users,
                'total_comments': total_comments,
                'total_views': total_views,
                'total_likes': total_likes,
                'today_media': today_media,
                'today_users': today_users,
                'media_trend': round(media_trend, 2),
                'users_trend': round(users_trend, 2),
            },
            'media_by_type': media_by_type,
            'encoding_stats': encoding_stats,
            'daily_stats': daily_stats,
            'pending': {
                'pending_media': pending_media,
                'reported_media': reported_media,
            },
            'active_users': active_users,
        })


class UserBatchActionsView(APIView):
    """用户批量操作"""
    
    permission_classes = (IsMediacmsManager,)
    
    @swagger_auto_schema(
        operation_summary='批量操作用户',
        operation_description='支持批量删除、封禁、解封、设置角色',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['action', 'user_ids'],
            properties={
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['delete', 'block', 'unblock', 'set_editor', 'set_manager', 'remove_role'],
                    description='操作类型'
                ),
                'user_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='用户ID列表'
                ),
            }
        ),
        tags=['Admin'],
    )
    def post(self, request):
        action = request.data.get('action')
        user_ids = request.data.get('user_ids', [])
        
        if not action or not user_ids:
            return Response(
                {'error': '缺少必要参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 过滤掉超级管理员和当前用户
        users = User.objects.filter(
            username__in=user_ids
        ).exclude(
            Q(is_superuser=True) | Q(username=request.user.username)
        )
        
        result = {'success': 0, 'failed': 0, 'message': ''}
        
        try:
            if action == 'delete':
                count = users.count()
                users.delete()
                result['success'] = count
                result['message'] = f'成功删除 {count} 个用户'
                
            elif action == 'block':
                count = users.update(is_active=False)
                result['success'] = count
                result['message'] = f'成功封禁 {count} 个用户'
                
            elif action == 'unblock':
                count = users.update(is_active=True)
                result['success'] = count
                result['message'] = f'成功解封 {count} 个用户'
                
            elif action == 'set_editor':
                count = users.update(is_editor=True)
                result['success'] = count
                result['message'] = f'成功设置 {count} 个编辑'
                
            elif action == 'set_manager':
                count = users.update(is_manager=True)
                result['success'] = count
                result['message'] = f'成功设置 {count} 个管理员'
                
            elif action == 'remove_role':
                count = users.update(is_editor=False, is_manager=False)
                result['success'] = count
                result['message'] = f'成功移除 {count} 个用户的角色'
                
            else:
                return Response(
                    {'error': '不支持的操作类型'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(result)
            
        except Exception as e:
            return Response(
                {'error': f'操作失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MediaBatchActionsView(APIView):
    """媒体批量操作增强版"""
    
    permission_classes = (IsMediacmsEditor,)
    
    @swagger_auto_schema(
        operation_summary='批量操作媒体',
        operation_description='支持批量删除、审核、设置精选、修改状态、分类等',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['action', 'media_ids'],
            properties={
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['delete', 'approve', 'reject', 'feature', 'unfeature', 'set_public', 'set_private', 'set_unlisted', 'set_category'],
                    description='操作类型'
                ),
                'media_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='媒体friendly_token列表'
                ),
                'category': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='分类标题（仅用于set_category操作）'
                ),
            }
        ),
        tags=['Admin'],
    )
    def post(self, request):
        action = request.data.get('action')
        media_ids = request.data.get('media_ids', [])
        category_title = request.data.get('category')
        
        if not action or not media_ids:
            return Response(
                {'error': '缺少必要参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        media_qs = Media.objects.filter(friendly_token__in=media_ids)
        
        result = {'success': 0, 'failed': 0, 'message': ''}
        
        try:
            if action == 'delete':
                count = media_qs.count()
                media_qs.delete()
                result['success'] = count
                result['message'] = f'成功删除 {count} 个媒体'
                
            elif action == 'approve':
                count = media_qs.update(is_reviewed=True)
                result['success'] = count
                result['message'] = f'成功审核 {count} 个媒体'
                
            elif action == 'reject':
                count = media_qs.update(is_reviewed=False)
                result['success'] = count
                result['message'] = f'成功拒绝 {count} 个媒体'
                
            elif action == 'feature':
                count = media_qs.update(featured=True)
                result['success'] = count
                result['message'] = f'成功设置 {count} 个精选媒体'
                
            elif action == 'unfeature':
                count = media_qs.update(featured=False)
                result['success'] = count
                result['message'] = f'成功取消 {count} 个精选媒体'
                
            elif action == 'set_public':
                count = media_qs.update(state='public')
                result['success'] = count
                result['message'] = f'成功设置 {count} 个媒体为公开'
                
            elif action == 'set_private':
                count = media_qs.update(state='private')
                result['success'] = count
                result['message'] = f'成功设置 {count} 个媒体为私有'
                
            elif action == 'set_unlisted':
                count = media_qs.update(state='unlisted')
                result['success'] = count
                result['message'] = f'成功设置 {count} 个媒体为不公开'
                
            elif action == 'set_category':
                if not category_title:
                    return Response(
                        {'error': '缺少分类参数'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                try:
                    category = Category.objects.get(title=category_title)
                    count = 0
                    for media in media_qs:
                        media.category.clear()
                        media.category.add(category)
                        count += 1
                    result['success'] = count
                    result['message'] = f'成功设置 {count} 个媒体的分类'
                except Category.DoesNotExist:
                    return Response(
                        {'error': f'分类 "{category_title}" 不存在'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {'error': '不支持的操作类型'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(result)
            
        except Exception as e:
            return Response(
                {'error': f'操作失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SystemMonitoringView(APIView):
    """系统监控"""
    
    permission_classes = (IsMediacmsManager,)
    
    @swagger_auto_schema(
        operation_summary='获取系统监控数据',
        operation_description='返回系统资源使用情况',
        tags=['Admin'],
    )
    def get(self, request):
        import psutil
        import os
        
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            memory_total = round(memory.total / (1024 ** 3), 2)  # GB
            memory_used = round(memory.used / (1024 ** 3), 2)
            memory_percent = memory.percent
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            disk_total = round(disk.total / (1024 ** 3), 2)
            disk_used = round(disk.used / (1024 ** 3), 2)
            disk_percent = disk.percent
            
            # 网络IO
            net_io = psutil.net_io_counters()
            bytes_sent = round(net_io.bytes_sent / (1024 ** 2), 2)  # MB
            bytes_recv = round(net_io.bytes_recv / (1024 ** 2), 2)
            
            # 系统负载（仅Unix系统）
            try:
                load_avg = os.getloadavg()
            except AttributeError:
                load_avg = [0, 0, 0]  # Windows系统
            
            # 数据库连接数（简化版）
            from django.db import connection
            db_queries = len(connection.queries) if settings.DEBUG else 0
            
            return Response({
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'load_avg': list(load_avg),
                },
                'memory': {
                    'total': memory_total,
                    'used': memory_used,
                    'percent': memory_percent,
                },
                'disk': {
                    'total': disk_total,
                    'used': disk_used,
                    'percent': disk_percent,
                },
                'network': {
                    'bytes_sent': bytes_sent,
                    'bytes_recv': bytes_recv,
                },
                'database': {
                    'queries': db_queries,
                },
            })
        except Exception as e:
            return Response(
                {'error': f'获取监控数据失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 函数式视图（用于简单的API）

@swagger_auto_schema(
    method='get',
    operation_summary='获取热门分类',
    operation_description='返回媒体数量最多的分类',
    tags=['Admin'],
)
@api_view(['GET'])
@permission_classes([IsMediacmsEditor])
def get_popular_categories(request):
    """获取热门分类"""
    categories = Category.objects.annotate(
        media_count=Count('media')
    ).order_by('-media_count')[:10]
    
    data = [{
        'title': cat.title,
        'media_count': cat.media_count,
        'description': cat.description,
    } for cat in categories]
    
    return Response(data)


@swagger_auto_schema(
    method='get',
    operation_summary='获取活跃用户',
    operation_description='返回上传媒体最多的用户',
    tags=['Admin'],
)
@api_view(['GET'])
@permission_classes([IsMediacmsEditor])
def get_active_users(request):
    """获取活跃用户"""
    users = User.objects.annotate(
        media_count=Count('media')
    ).order_by('-media_count')[:10]
    
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


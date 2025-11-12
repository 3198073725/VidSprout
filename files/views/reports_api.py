"""
举报管理 API
处理媒体举报相关的功能
"""
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from files.models import Media, Comment
from actions.models import MediaAction
from files.permissions import IsMediacmsManager
from files.serializers import MediaSerializer


class ReportListAPI(APIView):
    """举报列表API"""
    
    permission_classes = (IsMediacmsManager,)
    
    @swagger_auto_schema(
        operation_summary='获取举报列表',
        operation_description='获取媒体举报列表，支持筛选和分页',
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='页码'),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='每页数量'),
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='状态筛选: pending/resolved/ignored'),
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='搜索关键词'),
        ],
        tags=['Admin'],
    )
    def get(self, request):
        """
        获取举报列表
        """
        # 获取参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        status_filter = request.GET.get('status', '')
        search = request.GET.get('search', '')
        
        # 查询所有举报类型的MediaAction
        reports = MediaAction.objects.filter(
            action='report'
        ).select_related('user', 'media', 'media__user').order_by('-action_date')
        
        # 状态筛选（通过extra_info字段存储状态）
        if status_filter:
            if status_filter == 'pending':
                # 未处理的举报（extra_info不包含status或status=pending）
                reports = reports.filter(
                    Q(extra_info__icontains='"status": "pending"') | 
                    ~Q(extra_info__icontains='"status"')
                )
            elif status_filter == 'resolved':
                reports = reports.filter(extra_info__icontains='"status": "resolved"')
            elif status_filter == 'ignored':
                reports = reports.filter(extra_info__icontains='"status": "ignored"')
        
        # 搜索
        if search:
            reports = reports.filter(
                Q(extra_info__icontains=search) |
                Q(media__title__icontains=search) |
                Q(user__username__icontains=search)
            )
        
        # 总数
        total = reports.count()
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        reports_page = reports[start:end]
        
        # 构造返回数据
        results = []
        for report in reports_page:
            # 解析extra_info中的JSON数据
            import json
            try:
                extra_data = json.loads(report.extra_info) if report.extra_info else {}
            except:
                extra_data = {'reason': report.extra_info or ''}
            
            # 获取状态
            report_status = extra_data.get('status', 'pending')
            
            results.append({
                'id': report.id,
                'type': 'media',  # 当前只支持媒体举报
                'target_id': report.media.friendly_token,
                'target_title': report.media.title,
                'target_url': f'/view?m={report.media.friendly_token}',
                'reason': extra_data.get('reason', '其他'),
                'description': extra_data.get('description', ''),
                'status': report_status,
                'reporter_id': report.user.username if report.user else 'anonymous',
                'reporter_name': report.user.name if report.user and report.user.name else (report.user.username if report.user else '匿名用户'),
                'created_at': report.action_date.isoformat(),
                'handled_at': extra_data.get('handled_at', ''),
                'handler_name': extra_data.get('handler_name', ''),
                # 媒体相关信息
                'media': {
                    'friendly_token': report.media.friendly_token,
                    'title': report.media.title,
                    'thumbnail_url': report.media.thumbnail_url,
                    'author': report.media.user.username,
                    'views': report.media.views,
                    'reported_times': report.media.reported_times,
                }
            })
        
        return Response({
            'count': total,
            'results': results,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })


class ReportDetailAPI(APIView):
    """举报详情和处理API"""
    
    permission_classes = (IsMediacmsManager,)
    
    @swagger_auto_schema(
        operation_summary='更新举报状态',
        operation_description='标记举报为已处理或已忽略',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['action'],
            properties={
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['resolve', 'ignore', 'delete_media'],
                    description='操作类型'
                ),
                'note': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='处理备注'
                ),
            }
        ),
        tags=['Admin'],
    )
    def post(self, request, report_id):
        """
        处理举报
        """
        try:
            report = MediaAction.objects.get(id=report_id, action='report')
        except MediaAction.DoesNotExist:
            return Response(
                {'error': '举报不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        action = request.data.get('action')
        note = request.data.get('note', '')
        
        if not action:
            return Response(
                {'error': '缺少action参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 解析当前extra_info
        import json
        try:
            extra_data = json.loads(report.extra_info) if report.extra_info else {}
        except:
            extra_data = {'reason': report.extra_info or ''}
        
        # 更新状态
        if action == 'resolve':
            extra_data['status'] = 'resolved'
            extra_data['handled_at'] = timezone.now().isoformat()
            extra_data['handler_name'] = request.user.username
            extra_data['note'] = note
            message = '已标记为已处理'
            
        elif action == 'ignore':
            extra_data['status'] = 'ignored'
            extra_data['handled_at'] = timezone.now().isoformat()
            extra_data['handler_name'] = request.user.username
            extra_data['note'] = note
            message = '已忽略该举报'
            
        elif action == 'delete_media':
            # 删除被举报的媒体
            extra_data['status'] = 'resolved'
            extra_data['handled_at'] = timezone.now().isoformat()
            extra_data['handler_name'] = request.user.username
            extra_data['note'] = note
            extra_data['action_taken'] = 'media_deleted'
            
            # 先保存举报状态，再删除媒体（避免外键约束错误）
            media_to_delete = report.media
            report.extra_info = json.dumps(extra_data, ensure_ascii=False)
            report.save()
            
            # 现在删除媒体（会级联删除所有相关的MediaAction记录）
            media_to_delete.delete()
            
            # 直接返回，不需要再次保存report（因为report已被级联删除）
            return Response({
                'success': True,
                'message': '已删除被举报的媒体',
                'report': {
                    'id': report.id,
                    'status': extra_data.get('status'),
                    'handled_at': extra_data.get('handled_at'),
                    'handler_name': extra_data.get('handler_name'),
                    'action_taken': 'media_deleted'
                }
            })
            
            message = '已删除被举报的媒体'
            
        else:
            return Response(
                {'error': '无效的操作类型'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 保存更新
        report.extra_info = json.dumps(extra_data, ensure_ascii=False)
        report.save()
        
        return Response({
            'success': True,
            'message': message,
            'report': {
                'id': report.id,
                'status': extra_data.get('status'),
                'handled_at': extra_data.get('handled_at'),
                'handler_name': extra_data.get('handler_name'),
            }
        })


@api_view(['GET'])
@permission_classes((IsMediacmsManager,))
@swagger_auto_schema(
    operation_summary='获取举报统计',
    operation_description='获取举报数量统计信息',
    tags=['Admin'],
)
def get_report_stats(request):
    """
    获取举报统计信息
    """
    # 总举报数
    total_reports = MediaAction.objects.filter(action='report').count()
    
    # 待处理举报数（extra_info不包含status或status=pending）
    pending_reports = MediaAction.objects.filter(
        action='report'
    ).filter(
        Q(extra_info__icontains='"status": "pending"') | 
        ~Q(extra_info__icontains='"status"')
    ).count()
    
    # 已处理举报数
    resolved_reports = MediaAction.objects.filter(
        action='report',
        extra_info__icontains='"status": "resolved"'
    ).count()
    
    # 已忽略举报数
    ignored_reports = MediaAction.objects.filter(
        action='report',
        extra_info__icontains='"status": "ignored"'
    ).count()
    
    # 今日新增举报
    today = timezone.now().date()
    today_reports = MediaAction.objects.filter(
        action='report',
        action_date__date=today
    ).count()
    
    # 被举报最多的媒体
    most_reported = Media.objects.filter(
        reported_times__gt=0
    ).order_by('-reported_times')[:5]
    
    most_reported_data = [{
        'friendly_token': media.friendly_token,
        'title': media.title,
        'reported_times': media.reported_times,
        'thumbnail_url': media.thumbnail_url,
    } for media in most_reported]
    
    return Response({
        'total': total_reports,
        'pending': pending_reports,
        'resolved': resolved_reports,
        'ignored': ignored_reports,
        'today': today_reports,
        'most_reported_media': most_reported_data,
    })


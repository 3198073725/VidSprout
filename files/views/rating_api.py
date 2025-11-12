"""
评分相关API视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from ..models import RatingCategory, Rating, Media
from ..serializers import RatingCategorySerializer, RatingSerializer

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='get',
    tags=['Ratings'],
    operation_summary='获取启用的评分分类列表',
    operation_description='返回所有已启用的评分分类',
    responses={200: RatingCategorySerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def list_rating_categories(request):
    """获取所有启用的评分分类"""
    categories = RatingCategory.objects.filter(enabled=True).order_by('title')
    serializer = RatingCategorySerializer(categories, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    tags=['Ratings'],
    operation_summary='获取媒体的评分统计',
    operation_description='返回指定媒体的各分类评分统计信息',
    manual_parameters=[
        openapi.Parameter(
            'friendly_token',
            openapi.IN_PATH,
            description='媒体的友好令牌',
            type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: openapi.Response(
            description='评分统计信息',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ratings': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'category_title': openapi.Schema(type=openapi.TYPE_STRING),
                                'average_score': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'user_score': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        )
                    )
                }
            )
        ),
        404: 'Media not found'
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_media_ratings(request, friendly_token):
    """获取媒体的评分统计"""
    try:
        media = Media.objects.get(friendly_token=friendly_token)
    except Media.DoesNotExist:
        return Response(
            {'detail': '媒体不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 获取所有启用的评分分类
    categories = RatingCategory.objects.filter(enabled=True)
    ratings_data = []
    
    for category in categories:
        # 获取该分类下该媒体的所有评分
        ratings = Rating.objects.filter(media=media, rating_category=category)
        count = ratings.count()
        
        # 计算平均分
        if count > 0:
            total = sum(r.score for r in ratings)
            average = round(total / count, 1)
        else:
            average = None
        
        # 获取当前用户的评分
        user_score = None
        if request.user.is_authenticated:
            user_rating = ratings.filter(user=request.user).first()
            if user_rating:
                user_score = user_rating.score
        
        ratings_data.append({
            'category_id': category.id,
            'category_title': category.title,
            'average_score': average,
            'count': count,
            'user_score': user_score,
        })
    
    return Response({'ratings': ratings_data})


from django.conf import settings
from rest_framework import serializers

from .methods import is_mediacms_editor
from .models import Category, Comment, EncodeProfile, Media, Playlist, Tag, Rating, RatingCategory

# TODO: put them in a more DRY way


class MediaSerializer(serializers.ModelSerializer):
    # to be used in APIs as show related media
    user = serializers.ReadOnlyField(source="user.username")
    url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    author_thumbnail = serializers.SerializerMethodField()
    
    # 标签和分类的读取字段（返回完整对象列表）
    tags_info = serializers.SerializerMethodField(read_only=True)
    categories_info = serializers.SerializerMethodField(read_only=True)
    
    # 支持分类和标签的更新（使用标题字符串列表，仅写入）
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        help_text="List of tag titles for update"
    )
    category = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        help_text="List of category titles for update"
    )

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def get_api_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url(api=True))

    def get_thumbnail_url(self, obj):
        if obj.thumbnail_url:
            return self.context["request"].build_absolute_uri(obj.thumbnail_url)
        else:
            return None

    def get_author_profile(self, obj):
        return self.context["request"].build_absolute_uri(obj.author_profile())

    def get_author_thumbnail(self, obj):
        return self.context["request"].build_absolute_uri(obj.author_thumbnail())
    
    def get_tags_info(self, obj):
        """返回标签信息列表"""
        return [{"title": tag.title} for tag in obj.tags.all()]
    
    def get_categories_info(self, obj):
        """返回分类信息列表"""
        return [{"title": cat.title, "description": cat.description} for cat in obj.category.all()]
    
    def update(self, instance, validated_data):
        from .models import Tag, Category
        
        # 处理标签
        if 'tags' in validated_data:
            tag_titles = validated_data.pop('tags')
            instance.tags.clear()
            for tag_title in tag_titles:
                tag, _ = Tag.objects.get_or_create(title=tag_title.strip())
                instance.tags.add(tag)
        
        # 处理分类
        if 'category' in validated_data:
            category_titles = validated_data.pop('category')
            instance.category.clear()
            for cat_title in category_titles:
                try:
                    category = Category.objects.get(title=cat_title.strip())
                    instance.category.add(category)
                except Category.DoesNotExist:
                    pass  # 忽略不存在的分类
        
        # 更新其他字段
        return super().update(instance, validated_data)

    class Meta:
        model = Media
        read_only_fields = (
            "friendly_token",
            "user",
            "add_date",
            "media_type",
            "duration",
            "encoding_status",
            "views",
            "likes",
            "dislikes",
            "reported_times",
            "size",
            "is_reviewed",
            # featured 移出只读字段，允许管理员更新
        )
        fields = (
            "friendly_token",
            "url",
            "api_url",
            "user",
            "title",
            "description",
            "add_date",
            "views",
            "media_type",
            "state",
            "duration",
            "thumbnail_url",
            "is_reviewed",
            "preview_url",
            "author_name",
            "author_profile",
            "author_thumbnail",
            "encoding_status",
            "views",
            "likes",
            "dislikes",
            "reported_times",
            "featured",
            "user_featured",
            "size",
            "uploaded_poster",
            "enable_comments",  # 添加允许评论字段
            "tags",           # 写入用
            "category",       # 写入用
            "tags_info",      # 读取用
            "categories_info", # 读取用
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if False and request and 'category' in self.fields:
            # this is not working
            user = request.user
            if is_mediacms_editor(user):
                pass
            else:
                if getattr(settings, 'USE_RBAC', False):
                    # Filter category queryset based on user permissions
                    non_rbac_categories = Category.objects.filter(is_rbac_category=False)
                    rbac_categories = user.get_rbac_categories_as_contributor()
                    self.fields['category'].queryset = non_rbac_categories.union(rbac_categories)


class SingleMediaSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Media
        read_only_fields = (
            "friendly_token",
            "user",
            "add_date",
            "views",
            "media_type",
            "state",
            "duration",
            "encoding_status",
            "views",
            "likes",
            "dislikes",
            "reported_times",
            "size",
            "video_height",
            "is_reviewed",
        )
        fields = (
            "url",
            "user",
            "title",
            "description",
            "add_date",
            "edit_date",
            "media_type",
            "state",
            "duration",
            "thumbnail_url",
            "poster_url",
            "thumbnail_time",
            "url",
            "sprites_url",
            "preview_url",
            "author_name",
            "author_profile",
            "author_thumbnail",
            "encodings_info",
            "encoding_status",
            "views",
            "likes",
            "dislikes",
            "reported_times",
            "featured",  # 添加全局精选字段
            "user_featured",
            "original_media_url",
            "size",
            "video_height",
            "enable_comments",
            "categories_info",
            "is_reviewed",
            "edit_url",
            "tags_info",
            "hls_info",
            "license",
            "subtitles_info",
            "chapter_data",
            "ratings_info",
            "add_subtitle_url",
            "allow_download",
            "slideshow_items",
        )


class MediaSearchSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def get_api_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url(api=True))

    class Meta:
        model = Media
        fields = (
            "title",
            "author_name",
            "author_profile",
            "thumbnail_url",
            "add_date",
            "views",
            "description",
            "friendly_token",
            "duration",
            "url",
            "api_url",
            "media_type",
            "preview_url",
            "categories_info",
        )


class EncodeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncodeProfile
        fields = ("name", "extension", "resolution", "codec", "description")


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Category
        fields = (
            "title",
            "description",
            "is_global",
            "media_count",
            "user",
            "thumbnail_url",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("title", "media_count", "thumbnail_url")


class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Playlist
        read_only_fields = ("add_date", "user")
        fields = ("add_date", "title", "description", "user", "media_count", "url", "api_url", "thumbnail_url")


class PlaylistDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Playlist
        read_only_fields = ("add_date", "user")
        fields = ("title", "add_date", "user_thumbnail_url", "description", "user", "media_count", "url", "thumbnail_url")


class CommentSerializer(serializers.ModelSerializer):
    author_profile = serializers.ReadOnlyField(source="user.get_absolute_url")
    author_name = serializers.SerializerMethodField()
    author_thumbnail_url = serializers.ReadOnlyField(source="user.thumbnail_url")
    parent = serializers.CharField(required=False, allow_null=True)
    likes = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        """返回用户名称，如果 name 为空则返回 username"""
        if obj.user.name and obj.user.name.strip():
            return obj.user.name
        return obj.user.username
    
    def get_likes(self, obj):
        """返回评论的点赞数"""
        from actions.models import CommentAction
        return CommentAction.objects.filter(comment=obj, action='like').count()
    
    def get_user_liked(self, obj):
        """返回当前用户是否点赞了该评论"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from actions.models import CommentAction
            return CommentAction.objects.filter(
                user=request.user, 
                comment=obj, 
                action='like'
            ).exists()
        return False
    
    def validate_parent(self, value):
        """验证 parent 字段，接受 UUID 或 None"""
        if value is None or value == '':
            return None
        
        try:
            # 尝试通过 uid 查找父评论
            parent_comment = Comment.objects.get(uid=value)
            return parent_comment
        except Comment.DoesNotExist:
            raise serializers.ValidationError("父评论不存在")
        except ValueError:
            raise serializers.ValidationError("无效的父评论 ID")
    
    def to_representation(self, instance):
        """将 parent 对象转换为 uid 字符串"""
        ret = super().to_representation(instance)
        if instance.parent:
            ret['parent'] = str(instance.parent.uid)
        else:
            ret['parent'] = None
        return ret

    class Meta:
        model = Comment
        read_only_fields = ("add_date", "uid", "likes", "user_liked")
        fields = (
            "add_date",
            "text",
            "parent",
            "author_thumbnail_url",
            "author_profile",
            "author_name",
            "media_url",
            "uid",
            "likes",
            "user_liked",
        )


class RatingCategorySerializer(serializers.ModelSerializer):
    """评分分类序列化器"""
    
    class Meta:
        model = RatingCategory
        fields = (
            "id",
            "title",
            "description",
            "enabled",
        )
        read_only_fields = ("id",)


class RatingSerializer(serializers.ModelSerializer):
    """评分序列化器"""
    category_title = serializers.ReadOnlyField(source="rating_category.title")
    user_name = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Rating
        fields = (
            "id",
            "score",
            "rating_category",
            "category_title",
            "user_name",
            "add_date",
        )
        read_only_fields = ("id", "add_date", "category_title", "user_name")

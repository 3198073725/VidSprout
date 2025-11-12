from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def get_api_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url(api=True))

    def get_thumbnail_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.thumbnail_url())

    class Meta:
        model = User
        read_only_fields = [
            "date_added",
            "is_featured",
            "uid",
            "username",
            "advancedUser",
            "is_editor",
            "is_manager",
            "email_is_verified",
        ]
        fields = [
            "description",
            "date_added",
            "name",
            "is_featured",
            "thumbnail_url",
            "url",
            "api_url",
            "username",
            "advancedUser",
            "is_editor",
            "is_manager",
            "email_is_verified",
            "notification_on_comments",
        ]

        if settings.USERS_NEEDS_TO_BE_APPROVED:
            fields.append("is_approved")
            read_only_fields.append("is_approved")


class UserDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def get_api_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url(api=True))

    def get_thumbnail_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.thumbnail_url())

    class Meta:
        model = User
        read_only_fields = ("date_added", "is_featured", "uid", "username")
        fields = (
            "description",
            "date_added",
            "name",
            "is_featured",
            "thumbnail_url",
            "banner_thumbnail_url",
            "url",
            "username",
            "media_info",
            "api_url",
            "edit_url",
            "default_channel_edit_url",
        )
        extra_kwargs = {"name": {"required": False}}


class AdminUserSerializer(serializers.ModelSerializer):
    """管理后台专用的用户序列化器，包含所有管理相关字段"""
    url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def get_api_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url(api=True))

    def get_thumbnail_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.thumbnail_url())
    
    def get_logo(self, obj):
        """获取用户头像URL"""
        return self.context["request"].build_absolute_uri(obj.thumbnail_url())

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "description",
            "logo",
            "thumbnail_url",
            "url",
            "api_url",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_manager",
            "is_editor",
            "is_featured",
            "date_joined",
            "last_login",
            "advancedUser",
            "email_is_verified",
        ]
        read_only_fields = ["id", "username", "date_joined", "last_login"]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if settings.ACCOUNT_LOGIN_METHODS == {"username"} and not username:
            raise serializers.ValidationError('username is required to log in.')
        else:
            username_or_email = username
        if settings.ACCOUNT_LOGIN_METHODS == {"email"} and not email:
            raise serializers.ValidationError('email is required to log in.')
        else:
            username_or_email = email

        if settings.ACCOUNT_LOGIN_METHODS == {"username", "email"} and not (username or email):
            raise serializers.ValidationError('username or email is required to log in.')
        else:
            username_or_email = username or email

        if password is None:
            raise serializers.ValidationError('password is required to log in.')

        # 先检查用户是否存在
        try:
            # 尝试通过用户名或邮箱查找用户
            from django.db.models import Q
            user_obj = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )
            
            # 检查用户是否被封禁
            if not user_obj.is_active:
                raise serializers.ValidationError('该账号已被封禁，请联系管理员。')
            
            # 用户存在且未被封禁，验证密码
            user = authenticate(username=username_or_email, password=password)
            
            if user is None:
                # 用户存在但密码错误
                raise serializers.ValidationError('密码错误，请重试。')
                
        except User.DoesNotExist:
            # 用户不存在
            raise serializers.ValidationError('该账号不存在，请先注册。')

        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)

        return {'email': user.email, 'username': user.username, 'token': token.key}


class RegisterSerializer(serializers.Serializer):
    """用户注册序列化器"""
    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text='用户名（4-150个字符）'
    )
    email = serializers.EmailField(
        required=True,
        help_text='邮箱地址'
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        help_text='密码'
    )
    name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text='显示名称（可选）'
    )
    
    def validate_username(self, value):
        """验证用户名"""
        if len(value) < 4:
            raise serializers.ValidationError('用户名长度不能少于4个字符')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value
    
    def validate_email(self, value):
        """验证邮箱"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('邮箱已被注册')
        return value
    
    def create(self, validated_data):
        """创建用户"""
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        name = validated_data.get('name', username)
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name
        )
        
        # 生成 token
        token = Token.objects.create(user=user)
        
        # 返回用户信息（包含 token）
        user.token = token.key
        return user

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from drf_yasg import openapi as openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
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

from cms.permissions import IsUserOrManager
from files.methods import is_mediacms_editor, is_mediacms_manager

from .forms import ChannelForm, UserForm
from .models import Channel, User
from .serializers import LoginSerializer, RegisterSerializer, UserDetailSerializer, UserSerializer


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return None


def view_user(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")
    context["user"] = user
    context["CAN_EDIT"] = True if ((user and user == request.user) or is_mediacms_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediacms_manager(request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (user.allow_contact or is_mediacms_editor(request.user)) else False
    return render(request, "cms/user.html", context)


def shared_with_me(request, username):
    context = {}
    user = get_user(username=username)
    if not user or (user != request.user):
        return HttpResponseRedirect("/")

    context["user"] = user
    context["CAN_EDIT"] = True
    context["CAN_DELETE"] = True
    return render(request, "cms/user_shared_with_me.html", context)


def shared_by_me(request, username):
    context = {}
    user = get_user(username=username)
    if not user or (user != request.user):
        return HttpResponseRedirect("/")

    context["user"] = user
    context["CAN_EDIT"] = True
    context["CAN_DELETE"] = True
    return render(request, "cms/user_shared_by_me.html", context)


def view_user_playlists(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")

    context["user"] = user
    context["CAN_EDIT"] = True if ((user and user == request.user) or is_mediacms_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediacms_manager(request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (user.allow_contact or is_mediacms_editor(request.user)) else False

    return render(request, "cms/user_playlists.html", context)


def view_user_about(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")

    context["user"] = user
    context["CAN_EDIT"] = True if ((user and user == request.user) or is_mediacms_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediacms_manager(request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (user.allow_contact or is_mediacms_editor(request.user)) else False

    return render(request, "cms/user_about.html", context)


@login_required
def edit_user(request, username):
    user = get_user(username=username)
    if not user or (user != request.user and not is_mediacms_manager(request.user)):
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = UserForm(request.user, request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = UserForm(request.user, instance=user)
    return render(request, "cms/user_edit.html", {"form": form})


def view_channel(request, friendly_token):
    context = {}
    channel = Channel.objects.filter(friendly_token=friendly_token).first()
    if not channel:
        user = None
    else:
        user = channel.user
    context["user"] = user
    context["CAN_EDIT"] = True if ((user and user == request.user) or is_mediacms_manager(request.user)) else False
    return render(request, "cms/channel.html", context)


@login_required
def edit_channel(request, friendly_token):
    channel = Channel.objects.filter(friendly_token=friendly_token).first()
    if not (channel and request.user.is_authenticated and (request.user == channel.user)):
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = ChannelForm(request.POST, request.FILES, instance=channel)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.save()
            return HttpResponseRedirect(request.user.get_absolute_url())
    else:
        form = ChannelForm(instance=channel)
    return render(request, "cms/channel_edit.html", {"form": form})


@swagger_auto_schema(
    methods=['post'],
    manual_parameters=[],
    tags=['Users'],
    operation_summary='Contact user',
    operation_description='Contact user through email, if user has set this option',
)
@api_view(["POST"])
def contact_user(request, username):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "request need be authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    user = User.objects.filter(username=username).first()
    if user and (user.allow_contact or is_mediacms_editor(request.user)):
        from_email = request.user.email
        subject = f"[{settings.PORTAL_NAME}] - Message from {from_email}"
        body = request.data.get("body")
        body = """
You have received a message through the contact form\n
Sender name: %s
Sender email: %s\n
\n %s
""" % (
            request.user.name,
            from_email,
            body,
        )
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            reply_to=[from_email],
        )
        email.send(fail_silently=True)

    return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)

    def get_permissions(self):
        if not settings.ALLOW_ANONYMOUS_USER_LISTING:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY, description='Page number'),
            openapi.Parameter(name='name', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY, description='Search by name or username'),
        ],
        tags=['Users'],
        operation_summary='List users',
        operation_description='Paginated listing of users',
    )
    def get(self, request, format=None):
        if settings.CAN_SEE_MEMBERS_PAGE == "editors" and not is_mediacms_editor(request.user):
            raise PermissionDenied("You do not have permission to view this page.")

        if settings.CAN_SEE_MEMBERS_PAGE == "admins" and not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to view this page.")

        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        users = User.objects.filter()

        name = request.GET.get("name", "").strip()
        if name:
            users = users.filter(Q(name__icontains=name) | Q(username__icontains=name))

        if settings.USERS_NEEDS_TO_BE_APPROVED:
            is_approved = request.GET.get("is_approved")
            if is_approved == "true":
                users = users.filter(is_approved=True)
            elif is_approved == "false":
                users = users.filter(Q(is_approved=False) | Q(is_approved__isnull=True))

        page = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password", "email", "name"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=["Users"],
        operation_summary="Create user",
        operation_description="Create a new user. Only for managers.",
        responses={201: UserSerializer},
    )
    def post(self, request, format=None):
        if not is_mediacms_manager(request.user):
            raise PermissionDenied("You do not have permission to create users.")

        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        name = request.data.get("name")

        if not all([username, password, email, name]):
            return Response({"detail": "username, password, email, and name are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email, name=name)

        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    """"""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrManager)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
            # this need be explicitly called, and will call
            # has_object_permission() after has_permission has succeeded
            self.check_object_permissions(self.request, user)
            return user
        except PermissionDenied:
            return Response({"detail": "not enough permissions"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='username', type=openapi.TYPE_STRING, in_=openapi.IN_PATH, description='username', required=True),
        ],
        tags=['Users'],
        operation_summary='List user details',
        operation_description='Get user details',
    )
    def get(self, request, username, format=None):
        # Get user details
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        serializer = UserDetailSerializer(user, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="logo", in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description="logo"),
            openapi.Parameter(name="description", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="description"),
            openapi.Parameter(name="name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="name"),
            openapi.Parameter(name='username', type=openapi.TYPE_STRING, in_=openapi.IN_PATH, description='username', required=True),
        ],
        tags=['Users'],
        operation_summary='Edit user details',
        operation_description='Post user details - authenticated view',
        responses={201: openapi.Response('response description', UserDetailSerializer), 400: 'bad request'},
    )
    def post(self, request, username, format=None):
        # USER
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        serializer = UserDetailSerializer(user, data=request.data, context={"request": request})
        if serializer.is_valid():
            logo = request.data.get("logo")
            if logo:
                serializer.save(logo=logo)
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='action', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="action to perform ('change_password' or 'approve_user' or 'disapprove_user')"),
            openapi.Parameter(name='password', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="new password (if action is 'change_password')"),
        ],
        tags=['Users'],
        operation_summary='Update user details',
        operation_description='Allows a user to change their password. Allows a manager to approve a user.',
    )
    def put(self, request, username, format=None):
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        action = request.data.get("action")

        if action == "change_password":
            # Permission to edit user is already checked by self.get_user -> self.check_object_permissions
            password = request.data.get("password")
            if not password:
                return Response({"detail": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()

        elif action == "approve_user":
            if not is_mediacms_manager(request.user):
                raise PermissionDenied("You do not have permission to approve users.")
            user.is_approved = True
            user.save()
        elif action == "disapprove_user":
            if not is_mediacms_manager(request.user):
                raise PermissionDenied("You do not have permission to approve users.")
            user.is_approved = False
            user.save()
        else:
            return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserDetailSerializer(user, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[],
        tags=['Users'],
        operation_summary='to_be_written',
        operation_description='to_be_written',
    )
    def delete(self, request, username, format=None):
        # Delete a user
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserWhoami(generics.RetrieveAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    queryset = User.objects.all()
    permission_classes = (IsUserOrManager,)  # 使用自定义权限类，会检查封禁状态
    serializer_class = UserDetailSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='Whoami user information',
        operation_description='Whoami user information',
        responses={200: openapi.Response('response description', UserDetailSerializer), 403: 'Forbidden'},
    )
    def get(self, request, *args, **kwargs):
        return super(UserWhoami, self).get(request, *args, **kwargs)


class AdminUserWhoami(APIView):
    """管理员专用的用户信息接口，返回权限相关字段"""
    permission_classes = (IsUserOrManager,)  # 使用自定义权限类，会检查封禁状态
    
    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name or user.username,  # 如果 name 为空，使用 username
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_manager': getattr(user, 'is_manager', False),
            'is_editor': getattr(user, 'is_editor', False),
            'date_joined': user.date_joined.isoformat() if user.date_joined else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
        }
        # 调试日志
        print(f"AdminUserWhoami 返回数据: {data}")
        return Response(data)


class UserToken(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='Get a user token',
        operation_description="Returns an authenticated user's token",
        responses={200: 'token', 403: 'Forbidden'},
    )
    def get(self, request, *args, **kwargs):
        token = Token.objects.filter(user=request.user).first()
        if not token:
            token = Token.objects.create(user=request.user)

        return Response({'token': str(token)}, status=200)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []  # 禁用认证，避免 CSRF 检查
    serializer_class = LoginSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='Login url',
        operation_description="Login url endpoint. According to what the portal provides, you may provide username and/or email, plus the password",
        manual_parameters=[
            openapi.Parameter(name="username", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="username"),
            openapi.Parameter(name="email", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="email"),
            openapi.Parameter(name="password", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="password"),
        ],
        responses={200: openapi.Response('user details', LoginSerializer), 404: 'Bad request'},
    )
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """用户注册 API"""
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []  # 禁用认证，避免 CSRF 检查
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='用户注册',
        operation_description="用户注册接口，支持 JSON 和 FormData 格式",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名（4-150个字符）'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='邮箱地址'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='显示名称（可选）'),
            },
        ),
        responses={
            201: openapi.Response(
                '注册成功',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='认证令牌'),
                    }
                )
            ),
            400: '请求参数错误'
        }
    )
    def post(self, request):
        """处理注册请求"""
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建用户
        user = serializer.save()
        
        # 返回用户信息和token
        return Response(
            {
                'username': user.username,
                'email': user.email,
                'token': user.token,
                'name': user.name
            },
            status=status.HTTP_201_CREATED
        )


class PasswordResetView(APIView):
    """密码重置请求视图"""
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='请求密码重置',
        operation_description='发送密码重置邮件到指定邮箱地址',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    format='email', 
                    description='要重置密码的邮箱地址'
                ),
            },
        ),
        responses={
            200: openapi.Response(
                '重置邮件发送成功',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: '请求参数错误'
        }
    )
    def post(self, request):
        """处理密码重置请求"""
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'detail': '邮箱地址是必需的'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证邮箱格式
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'detail': '请输入有效的邮箱地址'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查用户是否存在
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 为了安全起见，即使用户不存在也返回成功消息
            return Response(
                {'message': '如果该邮箱地址存在于我们的系统中，您将收到密码重置邮件'},
                status=status.HTTP_200_OK
            )
        
        # 发送密码重置邮件
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        from django.template.loader import render_to_string
        from django.core.mail import send_mail
        from django.contrib.sites.shortcuts import get_current_site
        from django.conf import settings
        
        # 生成密码重置令牌
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # 获取当前站点信息
        current_site = get_current_site(request)
        site_name = getattr(settings, 'PORTAL_NAME', current_site.name)
        domain = current_site.domain
        
        # 渲染邮件内容
        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': uid,
            'user': user,
            'token': token,
            'protocol': 'https' if request.is_secure() else 'http',
        }
        
        subject = render_to_string('registration/password_reset_subject.txt', context)
        subject = ''.join(subject.splitlines())  # 移除换行符
        
        message = render_to_string('registration/password_reset_email.html', context)
        
        # 发送密码重置邮件
        try:
            import logging
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            logger = logging.getLogger(__name__)
            logger.info(f'尝试发送密码重置邮件到: {user.email}')
            logger.info(f'SMTP 配置: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            logger.info(f'发件人: {settings.DEFAULT_FROM_EMAIL}')
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = user.email
            
            # 添加 HTML 内容
            html_part = MIMEText(message, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 尝试多种 SMTP 配置
            configs = [
                {"port": 465, "use_ssl": True, "use_tls": False, "name": "SSL 465端口"},
                {"port": 587, "use_ssl": False, "use_tls": True, "name": "TLS 587端口"},
                {"port": 25, "use_ssl": False, "use_tls": True, "name": "TLS 25端口"},
            ]
            
            success = False
            for config in configs:
                try:
                    logger.info(f'尝试使用 {config["name"]} 连接')
                    
                    # 连接 SMTP 服务器
                    if config['use_ssl']:
                        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, config['port'])
                    else:
                        server = smtplib.SMTP(settings.EMAIL_HOST, config['port'])
                    
                    server.set_debuglevel(0)  # 关闭调试模式
                    
                    # 启动 TLS 加密
                    if config['use_tls'] and not config['use_ssl']:
                        server.starttls()
                    
                    # 登录
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    
                    # 发送邮件
                    text = msg.as_string()
                    server.sendmail(settings.DEFAULT_FROM_EMAIL, [user.email], text)
                    server.quit()
                    
                    logger.info(f'使用 {config["name"]} 发送邮件成功')
                    success = True
                    break
                    
                except Exception as config_error:
                    logger.warning(f'{config["name"]} 配置失败: {str(config_error)}')
                    continue
            
            if not success:
                raise Exception("所有 SMTP 配置都失败了")
            
            logger.info(f'密码重置邮件发送成功到: {user.email}')
            
        except smtplib.SMTPAuthenticationError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'SMTP 认证失败: {str(e)}')
            logger.error('请检查邮箱用户名和授权码是否正确')
            # 不重新抛出异常，返回成功消息（安全考虑）
            
        except smtplib.SMTPException as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'SMTP 错误: {str(e)}')
            logger.error(f'收件人: {user.email}')
            logger.error(f'SMTP 设置: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            # 不重新抛出异常，返回成功消息（安全考虑）
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'邮件发送失败: {str(e)}')
            logger.error(f'收件人: {user.email}')
            # 不重新抛出异常，返回成功消息（安全考虑）
        
        return Response(
            {'message': '如果该邮箱地址存在于我们的系统中，您将收到密码重置邮件'},
            status=status.HTTP_200_OK
        )

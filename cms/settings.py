import os
from pathlib import Path

from celery.schedules import crontab
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Security settings from environment variables
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'False'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('DJANGO_SECRET_KEY environment variable is required')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# PORTAL NAME, this is the portal title and
# is also shown on several places as emails
PORTAL_NAME = os.getenv('PORTAL_NAME', 'MediaCMS')
PORTAL_DESCRIPTION = os.getenv('PORTAL_DESCRIPTION', '')
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Shanghai')

# who can add media
# valid options include 'all', 'email_verified', 'advancedUser'
CAN_ADD_MEDIA = "all"

# who can comment
# valid options include 'all', 'email_verified', 'advancedUser'
CAN_COMMENT = "all"

# valid choices here are 'public', 'private', 'unlisted
PORTAL_WORKFLOW = "public"

# valid values: 'light', 'dark'.
DEFAULT_THEME = "light"


# These are passed on every request
# if set to False will not fetch external content
# this is only for the static files, as fonts/css/js files loaded from CDNs
# not for user uploaded media!
LOAD_FROM_CDN = False
LOGIN_ALLOWED = True  # whether the login button appears
REGISTER_ALLOWED = True  # whether the register button appears
UPLOAD_MEDIA_ALLOWED = True  # whether the upload media button appears
CAN_LIKE_MEDIA = True  # whether the like media appears
CAN_DISLIKE_MEDIA = True  # whether the dislike media appears
CAN_REPORT_MEDIA = True  # whether the report media appears
CAN_SHARE_MEDIA = True  # whether the share media appears
# how many times an item need be reported
# to get to private state automatically
REPORTED_TIMES_THRESHOLD = 10
ALLOW_ANONYMOUS_ACTIONS = ["report", "like", "dislike", "watch"]  # need be a list

# experimental functionality for user ratings - does not work
ALLOW_RATINGS = False
ALLOW_RATINGS_CONFIRMED_EMAIL_ONLY = True

# ip of the server should be part of this
ALLOWED_HOSTS = ["*", "mediacms.io", "127.0.0.1", "localhost"]

FRONTEND_HOST = "http://localhost"
# this variable - along with SSL_FRONTEND_HOST is used on several places
# as email where a URL need appear etc

# FRONTEND_HOST needs an http prefix - at the end of the file
# there's a conversion to https with the SSL_FRONTEND_HOST env
INTERNAL_IPS = "127.0.0.1"

# settings that are related with UX/appearance
# whether a featured item appears enlarged with player on index page
VIDEO_PLAYER_FEATURED_VIDEO_ON_INDEX_PAGE = False

PRE_UPLOAD_MEDIA_MESSAGE = ""

# Email settings from environment variables
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'djcelery_email.backends.CeleryEmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@localhost')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
ADMIN_EMAIL_LIST = os.getenv('ADMIN_EMAIL_LIST', DEFAULT_FROM_EMAIL).split(',')


MEDIA_IS_REVIEWED = True  # whether an admin needs to review a media file.
# By default consider this is not needed.
# If set to False, then each new media need be reviewed otherwise
# it won't appear on public listings

# if set to True the url for original file is returned to the API.
SHOW_ORIGINAL_MEDIA = True
# Keep in mind that nginx will serve the file unless there's
# some authentication taking place. Check nginx file and setup a
# basic http auth user/password if you want to restrict access

MAX_MEDIA_PER_PLAYLIST = 70
# bytes, size of uploaded media
UPLOAD_MAX_SIZE = 800 * 1024 * 1000 * 5

MAX_CHARS_FOR_COMMENT = 10000  # so that it doesn't end up huge
TIMESTAMP_IN_TIMEBAR = False  # shows timestamped comments in the timebar for videos
ALLOW_MENTION_IN_COMMENTS = False  # allowing to mention other users with @ in the comments

# valid options: content, author
RELATED_MEDIA_STRATEGY = "content"

# Whether or not to generate a sitemap.xml listing the pages on the site (default: False)
GENERATE_SITEMAP = False

USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

# these are the portal logos (dark and light)
# set new paths for svg or png if you want to override
# svg has priority over png, so if you want to use
# custom pngs and not svgs, remove the lines with svgs
# or set as empty strings
# example:
# PORTAL_LOGO_DARK_SVG = ""
# PORTAL_LOGO_LIGHT_SVG = ""
# place the files on static/images folder
PORTAL_LOGO_DARK_SVG = "/static/images/logo_dark.svg"
PORTAL_LOGO_DARK_PNG = "/static/images/logo_dark.png"
PORTAL_LOGO_LIGHT_SVG = "/static/images/logo_light.svg"
PORTAL_LOGO_LIGHT_PNG = "/static/images/logo_dark.png"

# paths to extra css files to be included, eg "/static/css/custom.css"
# place css inside static/css folder
EXTRA_CSS_PATHS = []
# protection agains anonymous users
# per ip address limit, for actions as like/dislike/report
TIME_TO_ACTION_ANONYMOUS = 10 * 60

# django-allauth settings
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_EMAIL_REQUIRED = True  # new users need to specify email
ACCOUNT_EMAIL_VERIFICATION = "optional"  # 'mandatory' 'none'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_ADAPTER = "users.adapter.MyAccountAdapter"
ACCOUNT_SIGNUP_FORM_CLASS = "users.forms.SignupForm"
ACCOUNT_USERNAME_VALIDATORS = "users.validators.custom_username_validators"
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# registration won't be open, might also consider to remove links for register
USERS_CAN_SELF_REGISTER = True

RESTRICTED_DOMAINS_FOR_USER_REGISTRATION = ["xxx.com", "emaildomainwhatever.com"]

# by default users do not need to be approved. If this is set to True, then new users
# will have to be approved before they can login successfully
USERS_NEEDS_TO_BE_APPROVED = False

# Comma separated list of domains:  ["organization.com", "private.organization.com", "org2.com"]
# Empty list disables.
ALLOWED_DOMAINS_FOR_USER_REGISTRATION = []

# django rest settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "cms.authentication.TokenAuthentication",  # 使用自定义认证类
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}


# SECRET_KEY is now loaded from environment variables at the top of the file

# Use pathlib for better path handling
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIRECTORY = os.getenv('TEMP_DIRECTORY', '/tmp')  # Don't use a temp directory inside BASE_DIR!!!

# Static and media files configuration
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'static'))
MEDIA_ROOT = os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media_files'))

# Media directories - using relative paths as required by Django
MEDIA_UPLOAD_DIR = 'original/'
MEDIA_ENCODING_DIR = 'encoded/'
THUMBNAIL_UPLOAD_DIR = f'{MEDIA_UPLOAD_DIR}thumbnails/'
SUBTITLES_UPLOAD_DIR = f'{MEDIA_UPLOAD_DIR}subtitles/'
HLS_DIR = str(Path(MEDIA_ROOT) / 'hls')

# FFmpeg configuration from environment variables
FFMPEG_COMMAND = os.getenv('FFMPEG_COMMAND', 'ffmpeg')
FFPROBE_COMMAND = os.getenv('FFPROBE_COMMAND', 'ffprobe')
MP4HLS = os.getenv('MP4HLS_COMMAND', 'mp4hls')

MASK_IPS_FOR_ACTIONS = True
# how many seconds a process in running state without reporting progress is
# considered as stale...unfortunately v9 seems to not include time
# some times so raising this high
RUNNING_STATE_STALE = 60 * 60 * 2

FRIENDLY_TOKEN_LEN = 9

# for videos, after that duration get split into chunks
# and encoded independently
CHUNKIZE_VIDEO_DURATION = 60 * 5
# aparently this has to be smaller than VIDEO_CHUNKIZE_DURATION
VIDEO_CHUNKS_DURATION = 60 * 4

# always get these two, even if upscaling
MINIMUM_RESOLUTIONS_TO_ENCODE = [144, 240]

# default settings for notifications
# not all of them are implemented

USERS_NOTIFICATIONS = {
    "MEDIA_ADDED": True,  # in use
    "MEDIA_ENCODED": False,  # not implemented
    "MEDIA_REPORTED": True,  # in use
}

ADMINS_NOTIFICATIONS = {
    "NEW_USER": True,  # in use
    "MEDIA_ADDED": True,  # in use
    "MEDIA_ENCODED": False,  # not implemented
    "MEDIA_REPORTED": True,  # in use
}


# this is for fineuploader - media uploads
UPLOAD_DIR = "uploads/"
CHUNKS_DIR = "chunks/"

# number of files to upload using fineuploader at once
UPLOAD_MAX_FILES_NUMBER = 100
CONCURRENT_UPLOADS = True
CHUNKS_DONE_PARAM_NAME = "done"
FILE_STORAGE = "django.core.files.storage.DefaultStorage"

X_FRAME_OPTIONS = "ALLOWALL"
# EMAIL_BACKEND is configured above with environment variable support
CELERY_EMAIL_TASK_CONFIG = {
    "queue": "short_tasks",
}

POST_UPLOAD_AUTHOR_MESSAGE_UNLISTED_NO_COMMENTARY = ""
# a message to be shown on the author of a media file and only
# only in case where unlisted workflow is used and no commentary
# exists

CANNOT_ADD_MEDIA_MESSAGE = "User cannot add media, or maximum number of media uploads has been reached."

# mp4hls command, part of Bento4
MP4HLS_COMMAND = "/home/mediacms.io/mediacms/Bento4-SDK-1-6-0-637.x86_64-unknown-linux/bin/mp4hls"

# highly experimental, related with remote workers
ADMIN_TOKEN = ""
# this is used by remote workers to push
# encodings once they are done
# USE_BASIC_HTTP = True
# BASIC_HTTP_USER_PAIR = ('user', 'password')
# specify basic auth user/password pair for use with the
# remote workers, if nginx basic auth is setup
# apache2-utils need be installed
# then run
# htpasswd -c /home/mediacms.io/mediacms/deploy/.htpasswd user
# and set a password
# edit /etc/nginx/sites-enabled/mediacms.io and
# uncomment the two lines related to htpasswd


AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = [
    "admin_customizations",
    "django.contrib.auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "imagekit",
    "files.apps.FilesConfig",
    "users.apps.UsersConfig",
    "actions.apps.ActionsConfig",
    "rbac.apps.RbacConfig",
    "identity_providers.apps.IdentityProvidersConfig",
    "debug_toolbar",
    "mptt",
    "crispy_forms",
    "crispy_bootstrap5",
    "uploader.apps.UploaderConfig",
    "djcelery_email",
    "drf_yasg",
    "allauth.socialaccount.providers.saml",
    "saml_auth.apps.SamlAuthConfig",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "users.middleware.UserActiveCheckMiddleware",  # 检查用户是否被封禁
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "cms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "files.context_processors.stuff",
            ],
        },
    },
]

WSGI_APPLICATION = "cms.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": ("username", "email", "first_name", "last_name"),
            "max_similarity": 0.7,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 7,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

LOGS_DIR = os.path.join(BASE_DIR, "logs")

error_filename = os.path.join(LOGS_DIR, "debug.log")
if not os.path.exists(LOGS_DIR):
    try:
        os.mkdir(LOGS_DIR)
    except PermissionError:
        pass

if not os.path.isfile(error_filename):
    open(error_filename, 'a').close()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": error_filename,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# Database configuration from environment variables
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'mediacms'),
        'USER': os.getenv('DB_USER', 'mediacms'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mediacms'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {'pool': True}
    }
}


# Redis configuration from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_DB = os.getenv('REDIS_DB', '1')

# Build Redis URL
if REDIS_PASSWORD:
    REDIS_LOCATION = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
else:
    REDIS_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Celery configuration
BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_LOCATION)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', BROKER_URL)
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_SOFT_TIME_LIMIT = 2 * 60 * 60
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_BEAT_SCHEDULE = {
    # clear expired sessions, every sunday 1.01am. By default Django has 2week
    # expire date
    "clear_sessions": {
        "task": "clear_sessions",
        "schedule": crontab(hour=1, minute=1, day_of_week=6),
    },
    "get_list_of_popular_media": {
        "task": "get_list_of_popular_media",
        "schedule": crontab(minute=1, hour="*/10"),
    },
    "update_listings_thumbnails": {
        "task": "update_listings_thumbnails",
        "schedule": crontab(minute=2, hour="*/30"),
    },
}
# TODO: beat, delete chunks from media root
# chunks_dir after xx days...(also uploads_dir)


LOCAL_INSTALL = False

# this is an option to make the whole portal available to logged in users only
# it is placed here so it can be overrided on local_settings.py
GLOBAL_LOGIN_REQUIRED = False

# TODO: separate settings on production/development more properly, for now
# this should be ok
CELERY_TASK_ALWAYS_EAGER = False
if os.environ.get("TESTING"):
    CELERY_TASK_ALWAYS_EAGER = True

# if True, only show original, don't perform any action on videos
DO_NOT_TRANSCODE_VIDEO = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LANGUAGES = [
    ('ar', _('Arabic')),
    ('bn', _('Bengali')),
    ('da', _('Danish')),
    ('nl', _('Dutch')),
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
    ('hi', _('Hindi')),
    ('id', _('Indonesian')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    ('pt', _('Portuguese')),
    ('ru', _('Russian')),
    ('zh-hans', _('Simplified Chinese')),
    ('sl', _('Slovenian')),
    ('zh-hant', _('Traditional Chinese')),
    ('es', _('Spanish')),
    ('tr', _('Turkish')),
    ('el', _('Greek')),
    ('ur', _('Urdu')),
    ('he', _('Hebrew')),
]

LANGUAGE_CODE = 'zh-hans'  # 设置为简体中文

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "resize": "both",
    "menubar": "file edit view insert format tools table help",
    "menu": {
        "format": {
            "title": "Format",
            "items": "blocks | bold italic underline strikethrough superscript subscript code | " "fontfamily fontsize align lineheight | " "forecolor backcolor removeformat",
        },
    },
    "plugins": "advlist,autolink,autosave,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,directionality,"
    "code,help,wordcount,emoticons,file,image,media",
    "toolbar": "undo redo | code preview | blocks | "
    "bold italic | alignleft aligncenter "
    "alignright alignjustify ltr rtl | bullist numlist outdent indent | "
    "removeformat | restoredraft help | image media",
    "branding": False,  # remove branding
    "promotion": False,  # remove promotion
    "body_class": "page-main-inner custom-page-wrapper",  # class of the body element in tinymce
    "block_formats": "Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3;",
    "formats": {  # customize h2 to always have emphasis-large class
        "h2": {"block": "h2", "classes": "emphasis-large"},
    },
    "font_size_formats": "16px 18px 24px 32px",
    "images_upload_url": "/tinymce/upload/",
    "images_upload_handler": "tinymce.views.upload_image",
    "automatic_uploads": True,
    "file_picker_types": "image",
    "paste_data_images": True,
    "paste_as_text": False,
    "paste_enable_default_filters": True,
    "paste_word_valid_elements": "b,strong,i,em,h1,h2,h3,h4,h5,h6,p,br,a,ul,ol,li",
    "paste_retain_style_properties": "all",
    "paste_remove_styles": False,
    "paste_merge_formats": True,
    "sandbox_iframes": False,
}

SPRITE_NUM_SECS = 10
# number of seconds for sprite image.
# If you plan to change this, you must also follow the instructions on admins_docs.md
# to change the equivalent value in ./frontend/src/static/js/components/media-viewer/VideoViewer/index.js and then re-build frontend

# how many images will be shown on the slideshow
SLIDESHOW_ITEMS = 30
# this calculation is redundant most probably, setting as an option
CALCULATE_MD5SUM = False

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# allow option to override the default admin url
# keep the trailing slash
DJANGO_ADMIN_URL = "admin/"

# this are used around a number of places and will need to be well documented!!!

USE_SAML = False
USE_RBAC = False
USE_IDENTITY_PROVIDERS = False
JAZZMIN_UI_TWEAKS = {"theme": "flatly"}

USE_ROUNDED_CORNERS = True

ALLOW_VIDEO_TRIMMER = True

ALLOW_CUSTOM_MEDIA_URLS = False

# Whether to allow anonymous users to list all users
ALLOW_ANONYMOUS_USER_LISTING = True

# Who can see the members page
# valid choices are all, editors, admins
CAN_SEE_MEMBERS_PAGE = "all"

# Maximum number of media a user can upload
NUMBER_OF_MEDIA_USER_CAN_UPLOAD = 100

# ffmpeg options
FFMPEG_DEFAULT_PRESET = "medium"  # see https://trac.ffmpeg.org/wiki/Encode/H.264

# If 'all' is in the list, no check is performed
ALLOWED_MEDIA_UPLOAD_TYPES = ["video", "audio", "image", "pdf"]

# transcription options
# the mediacms-full docker image needs to be used in order to be able to use transcription
# if you are using the mediacms-full image, change USE_WHISPER_TRANSCRIBE to True
USE_WHISPER_TRANSCRIBE = False

# by default all users can request a video to be transcribed. If you want to
# allow only editors, set this to False
USER_CAN_TRANSCRIBE_VIDEO = True

# Whisper transcribe options - https://github.com/openai/whisper
WHISPER_MODEL = "base"

# show a custom text in the sidebar footer, otherwise the default will be shown if this is empty
SIDEBAR_FOOTER_TEXT = ""

try:
    # keep a local_settings.py file for local overrides
    from .local_settings import *  # noqa

    # ALLOWED_HOSTS needs a url/ip
    ALLOWED_HOSTS.append(FRONTEND_HOST.replace("http://", "").replace("https://", ""))
    
    # 在加载 local_settings.py 之后，追加 CORS 配置到 INSTALLED_APPS 和 MIDDLEWARE
    # 这样可以避免在 local_settings.py 中访问可能未定义的变量
    if 'corsheaders' not in INSTALLED_APPS:
        INSTALLED_APPS.append('corsheaders')
    
    if 'corsheaders.middleware.CorsMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
    
    # CORS 配置 - 允许前端访问
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",  # Django 开发服务器
        "http://127.0.0.1:8000",
        "http://localhost:8088",  # frontend-vue 开发服务器
        "http://127.0.0.1:8088",
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    ]
    
    # CSRF 配置 - 信任的源
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:8000",  # Django 开发服务器
        "http://127.0.0.1:8000",
        "http://localhost:8088",  # frontend-vue
        "http://127.0.0.1:8088",
    ]
except ImportError:
    # local_settings not in use
    pass

# Don't add new settings below that could be overridden in local_settings.py!!!

if "http" not in FRONTEND_HOST:
    # FRONTEND_HOST needs a http:// preffix
    FRONTEND_HOST = f"http://{FRONTEND_HOST}"  # noqa

if LOCAL_INSTALL:
    SSL_FRONTEND_HOST = FRONTEND_HOST.replace("http", "https")
else:
    SSL_FRONTEND_HOST = FRONTEND_HOST


# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

PYSUBS_COMMAND = "pysubs2"

# the following is related to local development using docker
# and docker-compose-dev.yaml
try:
    DEVELOPMENT_MODE = os.environ.get("DEVELOPMENT_MODE")
    if DEVELOPMENT_MODE:
        # keep a dev_settings.py file for local overrides
        from .dev_settings import *  # noqa
except ImportError:
    pass


if GLOBAL_LOGIN_REQUIRED:
    auth_index = MIDDLEWARE.index("django.contrib.auth.middleware.AuthenticationMiddleware")
    MIDDLEWARE.insert(auth_index + 1, "django.contrib.auth.middleware.LoginRequiredMiddleware")


if USERS_NEEDS_TO_BE_APPROVED:
    AUTHENTICATION_BACKENDS = (
        'cms.auth_backends.ApprovalBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )
    auth_index = MIDDLEWARE.index("django.contrib.auth.middleware.AuthenticationMiddleware")
    MIDDLEWARE.insert(auth_index + 1, "cms.middleware.ApprovalMiddleware")

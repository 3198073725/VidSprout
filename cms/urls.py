from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(title="MediaCMS API", default_version='v1', contact=openapi.Contact(url="https://mediacms.io"), x_logo={"url": "../../static/images/logo_dark.svg"}),
    public=True,
    permission_classes=(AllowAny,),
)

# Main URL configuration for MediaCMS

urlpatterns = [
    # Static files
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots"
    ),
    
    # Main application URLs
    re_path(r"^", include("files.urls")),
    re_path(r"^", include("users.urls")),
    
    # Authentication URLs
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^api-auth/", include("rest_framework.urls")),
    
    # Admin interface
    path(getattr(settings, 'DJANGO_ADMIN_URL', 'admin/'), admin.site.urls),
    
    # API Documentation
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'docs/api/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    
    # Third-party integrations
    path("tinymce/", include("tinymce.urls")),
]

# Add debug toolbar URLs in development
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            re_path(r"^__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
    
    # Serve static and media files in development
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "MediaCMS Admin"
admin.site.site_title = "MediaCMS"
admin.site.index_title = "Admin"

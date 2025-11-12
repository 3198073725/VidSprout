from allauth.account.views import LoginView
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path

from . import management_views, tinymce_handlers, views
from .feeds import IndexRSSFeed, SearchRSSFeed
from .views.range_media import ServeMediaWithRange
from .views.contact_api import submit_contact_form
from .views import rating_api, admin_api, user_management_api, reports_api, system_api

friendly_token = r"(?P<friendly_token>[\w\-_]*)"

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    re_path(r"^$", views.index),
    re_path(r"^about", views.about, name="about"),
    re_path(r"^setlanguage", views.setlanguage, name="setlanguage"),
    re_path(r"^add_subtitle", views.add_subtitle, name="add_subtitle"),
    re_path(r"^edit_subtitle", views.edit_subtitle, name="edit_subtitle"),
    re_path(r"^categories$", views.categories, name="categories"),
    re_path(r"^contact$", views.contact, name="contact"),
    re_path(r"^publish", views.publish_media, name="publish_media"),
    re_path(r"^edit_chapters", views.edit_chapters, name="edit_chapters"),
    re_path(r"^edit_video", views.edit_video, name="edit_video"),
    re_path(r"^edit", views.edit_media, name="edit_media"),
    re_path(r"^embed", views.embed_media, name="get_embed"),
    re_path(r"^featured$", views.featured_media),
    re_path(r"^fu/", include(("uploader.urls", "uploader"), namespace="uploader")),
    re_path(r"^history$", views.history, name="history"),
    re_path(r"^liked$", views.liked_media, name="liked_media"),
    re_path(r"^latest$", views.latest_media),
    re_path(r"^members", views.members, name="members"),
    re_path(
        rf"^playlist/{friendly_token}$",
        views.view_playlist,
        name="get_playlist",
    ),
    re_path(
        rf"^playlists/{friendly_token}$",
        views.view_playlist,
        name="get_playlist",
    ),
    re_path(r"^popular$", views.recommended_media),
    re_path(r"^recommended$", views.recommended_media),
    path("rss/", IndexRSSFeed()),
    re_path("^rss/search", SearchRSSFeed()),
    re_path(r"^record_screen", views.record_screen, name="record_screen"),
    re_path(r"^search", views.search, name="search"),
    re_path(r"^scpublisher", views.upload_media, name="upload_media"),
    re_path(r"^tags", views.tags, name="tags"),
    re_path(r"^tos$", views.tos, name="terms_of_service"),
    re_path(r"^view", views.view_media, name="get_media"),
    re_path(r"^upload", views.upload_media, name="upload_media"),
    # API VIEWS
    re_path(r"^api/v1/media/user/bulk_actions$", views.MediaBulkUserActions.as_view()),
    re_path(r"^api/v1/media/user/bulk_actions/$", views.MediaBulkUserActions.as_view()),
    re_path(r"^api/v1/media$", views.MediaList.as_view()),
    re_path(r"^api/v1/media/$", views.MediaList.as_view()),
    re_path(
        rf"^api/v1/media/{friendly_token}$",
        views.MediaDetail.as_view(),
        name="api_get_media",
    ),
    re_path(
        r"^api/v1/media/encoding/(?P<encoding_id>[\w]*)$",
        views.EncodingDetail.as_view(),
        name="api_get_encoding",
    ),
    re_path(r"^api/v1/search$", views.MediaSearch.as_view()),
    re_path(
        rf"^api/v1/media/{friendly_token}/actions$",
        views.MediaActions.as_view(),
    ),
    re_path(
        rf"^api/v1/media/{friendly_token}/chapters$",
        views.video_chapters,
    ),
    re_path(
        rf"^api/v1/media/{friendly_token}/trim_video$",
        views.trim_video,
    ),
    re_path(r"^api/v1/categories$", views.CategoryList.as_view()),
    re_path(r"^api/v1/tags$", views.TagList.as_view()),
    re_path(r"^api/v1/contact$", submit_contact_form, name="api_contact_form"),
    re_path(r"^api/v1/rating-categories$", rating_api.list_rating_categories, name="api_rating_categories"),
    re_path(rf"^api/v1/media/{friendly_token}/ratings$", rating_api.get_media_ratings, name="api_media_ratings"),
    re_path(r"^api/v1/comments$", views.CommentList.as_view()),
    re_path(
        rf"^api/v1/media/{friendly_token}/comments$",
        views.CommentDetail.as_view(),
    ),
    re_path(
        rf"^api/v1/media/{friendly_token}/comments/(?P<uid>[\w-]*)$",
        views.CommentDetail.as_view(),
    ),
    re_path(
        r"^api/v1/comments/(?P<uid>[\w-]+)/like$",
        views.CommentLike.as_view(),
        name="api_comment_like",
    ),
    re_path(r"^api/v1/playlists$", views.PlaylistList.as_view()),
    re_path(r"^api/v1/playlists/$", views.PlaylistList.as_view()),
    re_path(
        rf"^api/v1/playlists/{friendly_token}$",
        views.PlaylistDetail.as_view(),
        name="api_get_playlist",
    ),
    re_path(r"^api/v1/user/action/(?P<action>[\w]*)$", views.UserActions.as_view()),
    # ADMIN VIEWS
    re_path(r"^api/v1/encode_profiles/$", views.EncodeProfileList.as_view()),
    re_path(r"^api/v1/manage_media$", management_views.MediaList.as_view()),
    re_path(r"^api/v1/manage_comments$", management_views.CommentList.as_view()),
    re_path(r"^api/v1/manage_users$", management_views.UserList.as_view()),
    re_path(r"^api/v1/tasks$", views.TasksList.as_view()),
    re_path(r"^api/v1/tasks/$", views.TasksList.as_view()),
    re_path(r"^api/v1/tasks/(?P<friendly_token>[\w|\W]*)$", views.TaskDetail.as_view()),
    # ADMIN API (新增管理员专用接口)
    re_path(r"^api/v1/admin/dashboard/stats$", admin_api.DashboardStatsView.as_view(), name="admin_dashboard_stats"),
    re_path(r"^api/v1/admin/media/batch$", admin_api.MediaBatchActionsView.as_view(), name="admin_media_batch"),
    re_path(r"^api/v1/admin/system/monitoring$", admin_api.SystemMonitoringView.as_view(), name="admin_system_monitoring"),
    re_path(r"^api/v1/admin/categories/popular$", admin_api.get_popular_categories, name="admin_popular_categories"),
    re_path(r"^api/v1/admin/users/active$", admin_api.get_active_users, name="admin_active_users"),
    # 用户管理API (使用admin路径避免与现有API冲突)
    re_path(r"^api/v1/admin/users/batch$", user_management_api.UserBatchOperationsAPI.as_view(), name="admin_user_batch_operations"),
    re_path(r"^api/v1/admin/users/(?P<user_id>[\w-]+)/actions$", user_management_api.UserActionAPI.as_view(), name="admin_user_actions"),
    re_path(r"^api/v1/admin/users/(?P<user_id>[\w-]+)$", user_management_api.UserDetailAPI.as_view(), name="admin_user_detail"),
    # 举报管理API
    re_path(r"^api/v1/admin/reports$", reports_api.ReportListAPI.as_view(), name="admin_reports_list"),
    re_path(r"^api/v1/admin/reports/stats$", reports_api.get_report_stats, name="admin_reports_stats"),
    re_path(r"^api/v1/admin/reports/(?P<report_id>\d+)$", reports_api.ReportDetailAPI.as_view(), name="admin_report_detail"),
    # 系统管理API
    re_path(r"^api/v1/admin/settings$", system_api.SystemSettingsView.as_view(), name="admin_settings"),
    re_path(r"^api/v1/admin/monitoring$", system_api.get_system_monitoring, name="admin_monitoring"),
    re_path(r"^api/v1/admin/test-email$", system_api.test_email, name="admin_test_email"),
    re_path(r"^manage/comments$", views.manage_comments, name="manage_comments"),
    re_path(r"^manage/media$", views.manage_media, name="manage_media"),
    re_path(r"^manage/users$", views.manage_users, name="manage_users"),
    # Media uploads in ADMIN created pages
    re_path(r"^tinymce/upload/", tinymce_handlers.upload_image, name="tinymce_upload_image"),
    # 支持Range请求的媒体文件服务（必须在static()之前）
    re_path(r'^media/(?P<path>.*)$', ServeMediaWithRange.as_view(), name='serve_media_with_range'),
    re_path("^(?P<slug>[\w.-]*)$", views.get_page, name="get_page"),  # noqa: W605
]

# 注意：不再使用 static() 来服务媒体文件，因为我们使用自定义的Range支持视图
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.USERS_NEEDS_TO_BE_APPROVED:
    urlpatterns.append(re_path(r"^approval_required/", views.approval_required, name="approval_required"))

if hasattr(settings, "USE_SAML") and settings.USE_SAML:
    urlpatterns.append(re_path(r"^saml/metadata", views.saml_metadata, name="saml-metadata"))

if hasattr(settings, "USE_IDENTITY_PROVIDERS") and settings.USE_IDENTITY_PROVIDERS:
    urlpatterns.append(path('accounts/login_system', LoginView.as_view(), name='login_system'))
    urlpatterns.append(re_path(r"^accounts/login", views.custom_login_view, name='login'))
else:
    urlpatterns.append(path('accounts/login', LoginView.as_view(), name='login_system'))

if hasattr(settings, "GENERATE_SITEMAP") and settings.GENERATE_SITEMAP:
    urlpatterns.append(path("sitemap.xml", views.sitemap, name="sitemap"))

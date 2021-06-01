from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.views.static import serve
from django.conf import settings
from social_core.views import resetPassword, reset_password_confirm, check_reset_token


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("api/social/", include("social_core.urls")),
    path("api/site/", include("site_content.urls")),
    path("api/reset-password/", resetPassword),
    path("api/reset-password-confirm/", reset_password_confirm),
    path("check-token/", check_reset_token),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

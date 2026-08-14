from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from core.settings import NAMESPACE
from django.views.decorators.cache import cache_page

CACHE_DURATION = 60 * 15  # 15 minutes

urlpatterns = [
    # STATIC AND MEDIA FILES
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(rf'^{NAMESPACE}/media/(?P<path>.*)$', cache_page(CACHE_DURATION)(serve), {'document_root': settings.MEDIA_ROOT}),
    re_path(rf'^{NAMESPACE}/static/(?P<path>.*)$', cache_page(CACHE_DURATION)(serve), {'document_root': settings.STATIC_ROOT}),

    # APPS
#     path("", include("apps.cobranca.urls")),

    # HEALTH CHECK
    path("", include("health_check.urls")),

    # DJANGO ADMIN
    path('', admin.site.urls),
    
]

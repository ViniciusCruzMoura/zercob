from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # STATIC AND MEDIA FILES
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # APPS
    path("", include("apps.lgpd.urls")),

    # HEALTH CHECK
    path("", include("health_check.urls")),

    # DJANGO ADMIN
    path('', admin.site.urls),
    
]

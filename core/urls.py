from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from core.settings import NAMESPACE
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect

CACHE_DURATION = 60 * 30  # 15 minutes

urlpatterns = [
    # STATIC AND MEDIA FILES
    re_path(rf'^{NAMESPACE}/media/(?P<path>.*)$', cache_page(CACHE_DURATION)(serve), {'document_root': settings.MEDIA_ROOT}),
    re_path(rf'^{NAMESPACE}/static/(?P<path>.*)$', cache_page(CACHE_DURATION)(serve), {'document_root': settings.STATIC_ROOT}),

    # DJANGO ADMIN
    path(NAMESPACE + '/admin/', admin.site.urls),

    # HEALTH CHECK
    path('', include('health_check.urls')),

    # PAGES

    # API

    # REDIRECT TO NAMESPACE "nwadv/"
    path(NAMESPACE + "/", lambda request: redirect('admin/', permanent=False)),
    path("", lambda request: redirect(NAMESPACE + "/", permanent=False)),
]

admin.site.site_header = ''
admin.site.index_title = ''
admin.site.site_title = ''
admin.site.enable_nav_sidebar = True

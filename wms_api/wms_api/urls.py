from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.urls import path, include
from .api_root import api_root
from filebrowser.sites import site

urlpatterns = [
    path('admin/filebrowser/', site.urls),  # FileBrowser URLs
    path("admin/", admin.site.urls),
    path("api/", api_root),  # custom root
    path('api/branding/', include('branding.urls')),
    path("api/activiteiten/", include("activiteiten.urls")),
    path("api/agenda/", include("agenda.urls")),
    path("api/inbox/", include("inbox.urls")),
    path("api/knack/", include("knack.urls")),
    path("api/muziekschool/", include("muziekschool.urls")),
    path("api/stichting/", include("stichting.urls")),
    path("tinymce/", include("tinymce.urls")),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # For production, use re_path with serve view
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
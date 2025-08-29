from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.http import JsonResponse
from django.urls import path, include
from django.shortcuts import redirect
from .api_root import api_root
from filebrowser.sites import site
from . import views

def health_check(request):
    """Health check endpoint for load balancer"""
    return JsonResponse({
        "status": "healthy",
        "service": "wms_api"
    })

def tinymce_filebrowser_redirect(request):
    """Redirect TinyMCE filebrowser requests to admin filebrowser"""
    query_string = request.GET.urlencode()
    redirect_url = f'/admin/filebrowser/browse/'
    if query_string:
        redirect_url += f'?{query_string}'
    return redirect(redirect_url)

urlpatterns = [
    path('health/', health_check, name='health'),
    path('admin/filebrowser/', site.urls),
    #path('tinymce/filebrowser/', tinymce_filebrowser_redirect),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("api/", api_root),  # custom root
    path('api/branding/', include('branding.urls')),
    path("api/activiteiten/", include("activiteiten.urls")),
    path("api/agenda/", include("agenda.urls")),
    path("api/inbox/", include("inbox.urls")),
    path("api/knack/", include("knack.urls")),
    path("api/muziekschool/", include("muziekschool.urls")),
    path("api/stichting/", include("stichting.urls")),
    path('tinymce-upload/', views.tinymce_upload, name='tinymce-upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
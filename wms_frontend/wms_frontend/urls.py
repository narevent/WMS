# wms_frontend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for load balancer"""
    return JsonResponse({
        "status": "healthy",
        "service": "wms_frontend"
    })

handler404 = "main.views.custom_page_not_found_view"
handler500 = "main.views.custom_server_error_view"

urlpatterns = [
    path('health/', health_check, name='health'),
    path('', include('activiteiten.urls')),
    path('', include('agenda.urls')),
    path('', include('main.urls')),
    path('', include('muziekles.urls')),
    path('', include('stichting.urls')),
]

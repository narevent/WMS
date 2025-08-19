# wms_frontend/urls.py
from django.contrib import admin
from django.urls import path, include

handler404 = "main.views.custom_page_not_found_view"
handler500 = "main.views.custom_server_error_view"

urlpatterns = [
    path('', include('activiteiten.urls')),
    path('', include('agenda.urls')),
    path('', include('main.urls')),
    path('', include('muziekles.urls')),
    path('', include('stichting.urls')),
]

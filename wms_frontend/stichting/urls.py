# frontend/urls.py
from django.urls import path
from . import views

app_name = 'stichting'

urlpatterns = [
    path('over-ons/', views.over_ons, name='over_ons'),
    path('partners/', views.sponsors, name='sponsors'),
    path('stichting/', views.stichting, name='stichting'),
]
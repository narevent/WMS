# agenda/urls.py
from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('agenda/', views.agenda, name='agenda'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('vakanties/', views.vakanties, name='vakanties'),
]
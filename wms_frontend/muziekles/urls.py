# muziekles/urls.py
from django.urls import path
from . import views

app_name = 'muziekles'

urlpatterns = [
    path('proefles/', views.proefles, name='proefles'),
    path('inschrijven/', views.inschrijven, name='inschrijven'),
    path('instrumenten/', views.instrumenten, name='instrumenten'),
    path('tarieven/', views.tarieven, name='tarieven'),
    path('locaties/', views.locaties, name='locaties'),
    path('vacatures/', views.vacatures, name='vacatures'),
]
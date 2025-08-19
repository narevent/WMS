# frontend/urls.py
from django.urls import path
from . import views

app_name = 'activiteiten'

urlpatterns = [
    path('cursussen/', views.cursussen, name='cursussen'),
    path('cursus/<int:id>/', views.cursus_detail, name='cursus_detail'),
    path('workshops/', views.workshops, name='workshops'),
    path('workshop/<int:id>/', views.workshop_detail, name='workshop_detail'),
    path('projecten/', views.projecten, name='projecten'),
    path('project/<int:id>/', views.project_detail, name='project_detail'),
    path('groepen/', views.groepen, name='groepen'),
    path('groep/<int:id>/', views.groep_detail, name='groep_detail'),
]
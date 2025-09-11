from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_project_list, name='project_list'),
    path('<int:project_id>/', views.get_project_detail, name='project_detail'),
    ]

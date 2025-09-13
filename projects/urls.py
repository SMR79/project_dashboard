from django.urls import path
from . import views


urlpatterns = [
    path('', views.search_projects, name='project_search'),
    path('create/', views.create_project, name='project_create'),
    path('<int:project_id>/', views.get_project_detail, name='project_detail'),
    path('search/<str:id>', views.search_projects, name='project_search'),
    path('reports/', views.project_reports, name='project_reports'),  # Example additional route    
    ]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.search_projects, name='project_search'),
    path('create/', views.create_project, name='project_create'),
    path('<int:project_id>/', views.get_project_detail, name='project_detail'),
    path('search/<str:id>', views.search_projects, name='project_search'),
    path('reports/', views.project_report, name='project_report'),  # Example additional route    
    path('edit/<int:project_id>/', views.edit_project, name='edit_project'),  # Edit project route
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),  # Delete project route
    ]

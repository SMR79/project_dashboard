from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_task_list, name='task_list'),
    path('<int:task_id>/', views.get_task_detail, name='task_detail'),
    path('create/', views.create_task, name='task_create'),
    path('report/', views.generate_task_report, name='task_report'),
    ]

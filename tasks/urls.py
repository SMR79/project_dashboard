from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_task_list, name='task_list'),
    path('create/', views.create_task, name='task_create'),
    ]

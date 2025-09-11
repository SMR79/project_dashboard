from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
    ]

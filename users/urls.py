from django.urls import path
from . import views


urlpatterns = [
    path('user_list', views.get_user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.welcome, name='welocome'),
    ]

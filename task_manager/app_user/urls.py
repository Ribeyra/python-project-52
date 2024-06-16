from django.urls import path
from task_manager.app_user import views

urlpatterns = [
    path('create/', views.CreateUser.as_view(), name='create_user'),
    path('', views.users, name='users'),
]

from django.urls import path
from task_manager.user import views

urlpatterns = [
    path('create/', views.CreateUser.as_view(), name='user_create'),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name='user_delete'),
    path('', views.UserListView.as_view(), name='users'),
]

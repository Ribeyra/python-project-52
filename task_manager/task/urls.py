from django.urls import path
from task_manager.task import views

urlpatterns = [
    path('create/', views.CreateTask.as_view(), name='task_create'),
    path(
        '<int:pk>/update/',
        views.UpdateTask.as_view(),
        name='task_update'
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteTask.as_view(),
        name='task_delete'
    ),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_view'),
    path('', views.TaskListView.as_view(), name='tasks'),
]

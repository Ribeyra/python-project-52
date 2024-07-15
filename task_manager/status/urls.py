from django.urls import path
from task_manager.status import views

urlpatterns = [
    path('create/', views.CreateStatus.as_view(), name='status_create'),
    path(
        '<int:pk>/update/',
        views.UpdateStatus.as_view(),
        name='status_update'
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteStatus.as_view(),
        name='status_delete'
    ),
    path('', views.StatusListView.as_view(), name='statuses'),
]

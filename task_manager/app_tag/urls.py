from django.urls import path
from task_manager.app_tag import views

urlpatterns = [
    path('create/', views.CreateTag.as_view(), name='tag_create'),
    path(
        '<int:pk>/update/',
        views.UpdateTag.as_view(),
        name='tag_update'
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteTag.as_view(),
        name='tag_delete'
    ),
    path('', views.TagListView.as_view(), name='tags'),
]

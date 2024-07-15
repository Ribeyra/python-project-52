from django.urls import path
from task_manager.label import views

urlpatterns = [
    path('create/', views.CreateLabel.as_view(), name='label_create'),
    path(
        '<int:pk>/update/',
        views.UpdateLabel.as_view(),
        name='label_update'
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteLabel.as_view(),
        name='label_delete'
    ),
    path('', views.LabelListView.as_view(), name='labels'),
]

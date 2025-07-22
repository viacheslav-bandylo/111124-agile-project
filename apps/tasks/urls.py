from django.urls import path
from apps.tasks.views.tag_views import *
from apps.tasks.views.task_views import TaskListCreateView

urlpatterns = [
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailUpdateDeleteAPIView.as_view(), name='tag-detail-update-delete'),
    path('', TaskListCreateView.as_view(), name='task-list-create'),
]


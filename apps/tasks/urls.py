from django.urls import path
from apps.tasks.views.tag_views import *

urlpatterns = [
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailUpdateDeleteAPIView.as_view(), name='tag-detail-update-delete'),
]


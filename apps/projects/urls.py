from django.urls import path
from apps.projects.views.project_views import *

urlpatterns = [
    path('', ProjectListCreateAPIView.as_view(), name='project-list-create')  # api/v1/projects/
]

from rest_framework.generics import ListCreateAPIView

from agile_projects.paginations import TasksPagination
from apps.tasks.models import Task
from apps.tasks.serializers.task_serializers import CreateTaskSerializer, ListTaskSerializer


class TaskListCreateView(ListCreateAPIView):
    pagination_class = TasksPagination

    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListTaskSerializer
        return CreateTaskSerializer

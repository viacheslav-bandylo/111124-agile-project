from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView

from apps.projects.models import ProjectFile, Project
from apps.projects.serializers.project_file_serializers import ListProjectFileSerializer, CreateProjectFileSerializer


class ListCreateProjectFileAPIView(APIView):
    # Вспомогательный метод для получения файлов, с возможностью фильтрации по имени проекта
    def get_objects(self, project_name=None):
        if project_name: # Если имя проекта передано...
            # Фильтруем ProjectFile по имени связанного проекта
            project_files = ProjectFile.objects.filter(projects__name=project_name)
            return project_files

        return ProjectFile.objects.all()


    # Метод GET для получения списка всех файлов
    def get(self, request: Request) -> Response:
        project_name = request.query_params.get('project_name') # Получаем имя проекта из query параметров

        project_files = self.get_objects(project_name) # Получаем файлы

        if not project_files.exists(): # Если файлов нет, возвращаем 204 No Content
            return Response(data=[], status=HTTP_204_NO_CONTENT)

        # Сериализуем список файлов с помощью ListProjectFileSerializer
        serializer = ListProjectFileSerializer(project_files, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK) # Возвращаем данные и статус 200 OK

    # Метод POST для создания нового файла и привязки его к проекту
    def post(self, request: Request) -> Response:
        # Получаем сам файл из request.FILES (для обработки файлов multipart/form-data)
        file_content = request.FILES["file"]
        # Получаем ID проекта из тела запроса (из обычных полей запроса, не файлов)
        project_id = request.data["project_id"]

        # Пытаемся получить объект Project по ID, если не найден - 404
        project = get_object_or_404(Project, pk=project_id)

        # Создаем сериализатор.
        # data=request.data: данные для полей модели (file_name)
        # context={"raw_file": file_content}: передаем сам файл в контекст сериализатора,
        # чтобы он был доступен в методе `create` сериализатора для обработки.
        serializer = CreateProjectFileSerializer(
            data=request.data,
            context={
                "raw_file": file_content,
            }
        )

        if serializer.is_valid(raise_exception=True): # Проверяем валидность данных
            project_file = serializer.save() # Сохраняем объект ProjectFile в базе данных

        # Привязываем созданный файл к проекту.
        # ManyToManyField имеет метод .set() для установки связей.
        project_file.projects.set([project])

        return Response(  # Возвращаем сообщение об успехе и статус 200 OK
            data={
                "message": "File uploaded successfully"
            },
            status=HTTP_200_OK
        )


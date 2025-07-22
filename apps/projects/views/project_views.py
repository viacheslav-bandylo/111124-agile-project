from datetime import datetime # Для парсинга даты из строки

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone # Для работы с часовыми поясами

from apps.projects.models.project import Project # Импортируем модель Project
from apps.projects.serializers.project_serializers import (  # Импортируем наши сериализаторы
    ListProjectsSerializer,
    CreateProjectSerializer, DetailProjectSerializer
)

class ProjectListCreateAPIView(APIView):
    # Вспомогательный метод для получения объектов Project с возможностью фильтрации по датам
    def get_objects(self, date_from=None, date_to=None):
        if date_from and date_to: # Если обе даты переданы...
            # Конвертируем строки дат в объекты datetime, учитывая часовой пояс
            date_from = timezone.make_aware(
                datetime.strptime(date_from, '%Y-%m-%d')
            )
            date_to = timezone.make_aware(
                datetime.strptime(date_to, '%Y-%m-%d')
            )

            projects = Project.objects.filter(  # Фильтруем по диапазону дат created_at
                created_at__range=[date_from, date_to]
            )

            return projects

        return Project.objects.all()


    # Метод GET для получения списка всех проектов
    def get(self, request: Request) -> Response:
        # Получаем даты из query параметров 'date_from' и 'date_to'
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        projects = self.get_objects(date_from, date_to) # Получаем проекты с учетом фильтрации

        if not projects.exists(): # Если проектов нет, возвращаем 204 No Content
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        # Сериализуем список проектов с помощью AllProjectsSerializer
        serializer = ListProjectsSerializer(projects, many=True)

        return Response( # Возвращаем данные и статус 200 OK
            serializer.data,
            status=status.HTTP_200_OK,
        )


    # Метод POST для создания нового проекта
    def post(self, request: Request) -> Response:
        # Используем CreateProjectSerializer для валидации и создания проекта
        serializer = CreateProjectSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True): # Проверяем валидность
            serializer.save() # Сохраняем проект в базу данных

            return Response( # Возвращаем созданные данные и статус 201 Created
                serializer.validated_data,
                status=status.HTTP_201_CREATED,
            )

        # Этот блок избыточен из-за `raise_exception=True`, но оставлен по аналогии с конспектом.
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProjectDetailUpdateDeleteAPIView(APIView):
    """
    Отображение для получения, обновления и удаления ОДНОГО проекта.
    """
    def get_object(self, pk):
        """
        Вспомогательный метод для получения одного объекта Project по его pk (primary key).
        Если объект не найден, вернет ошибку 404 Not Found.
        """
        return get_object_or_404(Project, pk=pk)

    def get(self, request: Request, pk) -> Response:
        """
        Обрабатывает GET-запрос. Получает один проект по pk.
        """
        project = self.get_object(pk=pk) # 1. Находим проект
        serializer = DetailProjectSerializer(project) # 2. Передаем его в сериализатор
        return Response(serializer.data, status=status.HTTP_200_OK) # 3. Возвращаем данные

    def put(self, request: Request, pk) -> Response:
        """
        Обрабатывает PUT-запрос для полного или частичного обновления проекта.
        """
        project = self.get_object(pk=pk) # 1. Находим проект для обновления

        # Для обновления мы используем сериализатор создания/обновления
        # instance=project - указывает, какой объект мы обновляем
        # data=request.data - новые данные из запроса
        # partial=True - разрешает частичное обновление (PATCH)
        serializer = CreateProjectSerializer(
            instance=project, data=request.data, partial=True
        )

        # 2. Проверяем, корректны ли новые данные
        if serializer.is_valid(raise_exception=True):
            serializer.save() # 3. Сохраняем изменения в базе данных
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def delete(self, request, pk) -> Response:
        """
        Обрабатывает DELETE-запрос для удаления проекта.
        """
        project = self.get_object(pk=pk)# 1. Находим проект
        project.delete() # 2. Удаляем его из базы данных
        # 3. Возвращаем успешный ответ без данных
        return Response(status=status.HTTP_204_NO_CONTENT)



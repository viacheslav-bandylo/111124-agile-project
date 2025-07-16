from rest_framework.request import Request # Для типизации объекта запроса
from rest_framework.response import Response # Для формирования ответа API
from rest_framework import status # Для использования HTTP-кодов состояния
from rest_framework.views import APIView # Базовый класс для наших API-представлений
from rest_framework.generics import get_object_or_404

from apps.tasks.models.tag import Tag # Импортируем модель Tag
from apps.tasks.serializers.tag_serializers import TagSerializer # Импортируем наш сериализатор


class TagListCreateAPIView(APIView):
    # Вспомогательный метод для получения всех объектов Tag
    def get_objects(self):
        return Tag.objects.all()


    # Метод GET для получения списка всех тегов
    def get(self, request: Request) -> Response:
        tags = self.get_objects() # Получаем все теги

        if not tags.exists(): # Если тегов нет, возвращаем пустой список и статус 204 No Content
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        # Сериализуем полученные теги. many=True указывает, что это список объектов.
        serializer = TagSerializer(tags, many=True)

        # Возвращаем сериализованные данные с HTTP-статусом 200 OK
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # Метод POST для создания нового тега
    def post(self, request: Request) -> Response:
        # Создаем экземпляр сериализатора, передавая данные из запроса
        serializer = TagSerializer(data=request.data)

        # Проверяем валидность данных. raise_exception=True автоматически выбросит исключение
        # (и DRF вернет 400 Bad Request) если данные невалидны.
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Если данные валидны, сохраняем объект в базу данных

            # Возвращаем созданные данные и HTTP-статус 201 Created
            return Response(
                serializer.validated_data,  # Возвращаем данные, которые прошли валидацию
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,  # Возвращаем ошибки валидации
            status=status.HTTP_400_BAD_REQUEST
        )


class TagDetailUpdateDeleteAPIView(APIView):
    # Вспомогательный метод для получения конкретного объекта Tag по его ID (pk)
    def get_object(self, pk: int) -> Tag:
        return get_object_or_404(Tag, pk=pk) # Используем get_object_or_404

    # Метод GET для получения конкретного тега
    def get(self, request: Request, pk: int) -> Response:
        tag = self.get_object(pk=pk) # Получаем тег по ID

        serializer = TagSerializer(tag) # Сериализуем один объект

        return Response( # Возвращаем данные и статус 200 OK
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # Метод PUT для обновления тега
    def put(self, request: Request, pk: int) -> Response:
        tag = self.get_object(pk=pk)  # Получаем тег для обновления

        serializer = TagSerializer(tag, data=request.data) #, partial=True)

        if serializer.is_valid(raise_exception=True):  # Проверяем валидность
            serializer.save()  # Сохраняем изменения в базу данных

            return Response(  # Возвращаем обновленные данные и статус 200 OK
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )

        # Этот блок избыточен из-за `raise_exception=True`, но оставлен по аналогии с конспектом.
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Метод DELETE для удаления тега
    def delete(self, request: Request, pk: int) -> Response:
        tag = self.get_object(pk=pk) # Получаем тег для удаления

        tag.delete() # Удаляем объект из базы данных

        return Response( # Возвращаем сообщение об успехе и статус 204 OK
            data={
                "message": "Tag was deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

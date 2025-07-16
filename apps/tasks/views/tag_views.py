from rest_framework.request import Request # Для типизации объекта запроса
from rest_framework.response import Response # Для формирования ответа API
from rest_framework import status # Для использования HTTP-кодов состояния
from rest_framework.views import APIView # Базовый класс для наших API-представлений

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

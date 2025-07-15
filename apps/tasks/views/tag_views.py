from rest_framework.request import Request # Для типизации объекта запроса
from rest_framework.response import Response # Для формирования ответа API
from rest_framework import status # Для использования HTTP-кодов состояния
from rest_framework.views import APIView # Базовый класс для наших API-представлений

from apps.tasks.models.tag import Tag # Импортируем модель Tag
from apps.tasks.serializers.tag_serializers import TagSerializer # Импортируем наш сериализатор


class TagListAPIView(APIView):
    # Вспомогательный метод для получения всех объектов Tag
    def get_objects(self) -> Tag:
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

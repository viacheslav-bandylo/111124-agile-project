from rest_framework import serializers # Импортируем serializers из DRF
from apps.tasks.models.tag import Tag # Импортируем нашу модель Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag # Указываем, с какой моделью работает этот сериализатор
        fields = '__all__' # Указываем, что сериализатор должен включать все поля модели

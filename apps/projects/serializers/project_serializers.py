from rest_framework import serializers
from apps.projects.models.project import Project # Импортируем нашу модель Project


class ListProjectsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения краткой информации о всех проектах.
    """
    class Meta:
        model = Project
        # Отображаемые поля: id, name, created_at
        fields = ('id', 'name', 'created_at')


class CreateProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового проекта.
    """
    # created_at должно быть только для чтения, так как оно заполняется автоматически
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        # Поля, необходимые для создания: name, description. created_at будет заполнено автоматически.
        fields = ('name', 'description', 'created_at')


    def validate_description(self, value: str) -> str:
        """
        Добавляем пользовательскую валидацию для поля description:
        длина описания должна быть не менее 30 символов.
        """
        if len(value) < 30:
            raise serializers.ValidationError(
                "Description must be at least 30 characters long"
            )
        return value


class DetailProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения одного проекта.
    """
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'count_of_files')


class ProjectShortInfoSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор для отображения информации о проекте.
    Используется как вложенный сериализатор.
    """
    class Meta:
        model = Project
        fields = ('id', 'name')

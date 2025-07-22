from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from apps.projects.models import Project
from apps.projects.serializers.project_serializers import ProjectShortInfoSerializer
from apps.tasks.choices.priorities import Priorities
from apps.tasks.models import Task, Tag
from apps.tasks.serializers.tag_serializers import TagSerializer


class ListTaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения краткой информации о задачах.
    Поля project и assignee будут отображаться по их именам/email.
    """
    project = serializers.StringRelatedField(
        read_only=True,
    )

    assignee = serializers.SlugRelatedField(
        read_only=True, # Только для чтения, не ожидаем его в данных при создании/обновлении
        slug_field='email', # Отображать поле 'email' из связанной модели User
    )

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority', 'project', 'assignee', 'deadline']


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новой задачи.
    Включает валидацию и переопределенный метод create.
    """
    # Для поля project: мы ожидаем имя проекта (slug_field='name')
    # queryset указывает, какие объекты Project можно выбрать.
    project = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Project.objects.all(),
    )

    tags = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'priority', 'project', 'tags']

    def validate_name(self, value: str):
        if len(value) < 10:
            raise serializers.ValidationError(
                'The name must be at least 10 characters long.'
            )
        return value

    def validate_description(self, value: str):
        if len(value) < 50:
            raise serializers.ValidationError(
                'The description must be at least 50 characters long.'
            )
        return value

    def validate_priority(self, value: int):
        if value not in [val[0] for val in Priorities.choices()]:
            raise serializers.ValidationError(
                'The priority must be one of the choices.'
            )
        return value

    # SlugRelatedField сам делает эту валидацию, если queryset указан.
    def validate_project(self, value: str):
        if not Project.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                'The project does not exist.'
            )
        return value

    def validate_deadline(self, value: datetime):
        # Проверяем, что дедлайн не в прошлом
        if value < timezone.now():
            raise serializers.ValidationError(
                'The deadline must be in the future.'
            )

        return value

    # Переопределенный метод create для обработки ManyToManyField (tags)
    def create(self, validated_data):
        # Извлекаем теги из validated_data. Они будут списком объектов Tag (из-за SlugRelatedField).
        tags = validated_data.pop('tags', [])

        # Создаем объект Task без тегов
        task = Task.objects.create(**validated_data)

        # Добавляем теги к созданному объекту Task.
        # Метод .add() используется для ManyToManyField.
        task.tags.add(*tags)

        task.save() # Сохраняем (хотя .add() обычно сам сохраняет связь, явное save() не повредит)

        return task

    # Метод update для обработки обновления существующей задачи
    def update(self, instance: Task, validated_data) -> Task:
        # Извлекаем теги из validated_data.
        # Если теги не переданы в запросе на обновление, pop() вернет пустой список.
        tags = validated_data.pop('tags', [])

        # Обновляем все остальные поля экземпляра `Task`
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags:  # Если теги были переданы для обновления
            instance.tags.set(tags)

        instance.save()  # Сохраняем изменения в базу данных

        return instance # Возвращаем обновленный экземпляр



class DetailTaskSerializer(serializers.ModelSerializer):
    """
        Сериализатор для получения подробной информации о задаче.
        Использует вложенные сериализаторы для project и tags.
    """
    # Вложенный сериализатор для проекта. Будет отображать id и name проекта.
    project = ProjectShortInfoSerializer()
    # Вложенный сериализатор для тегов. many=True, потому что тегов может быть много.
    # read_only=True, так как мы не ожидаем, что через этот сериализатор будут меняться теги.
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        # Исключаем поля updated_at и deleted_at из вывода.
        exclude = ('updated_at', 'deleted_at')

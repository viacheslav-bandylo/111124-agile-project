from rest_framework import serializers

from apps.projects.models import ProjectFile
from apps.projects.utils.upload_file_helper import check_extension, create_file_path, check_file_size, save_file


class ListProjectFileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения краткой информации о всех файлах.
    """
    project = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # Добавим, чтобы увидеть ID связанных проектов
                                                                            # или StringRelatedField, чтобы увидеть их строковое представление.
                                                                            # По умолчанию ManyToMany не отображается так просто.
                                                                            # Если просто `project`, то DRF попытается взять `__str__` или `pk`.
                                                                            # В данном случае, ManyToManyField будет отображаться как список PK по умолчанию.
    class Meta:
        model = ProjectFile
        fields = ['id', 'file_name', 'project']


class CreateProjectFileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового файла.
    """
    # project_id - поле для связи с проектом, оно не является частью модели ProjectFile напрямую,
    # но будет передаваться в запросе.
    # Оно не указано в Meta.fields, т.к. оно используется в `create` методе.

    class Meta:
        model = ProjectFile
        # Для создания необходимо только file_name (файл сам передается через request.FILES)
        fields = ['file_name']

    def validate_file_name(self, value: str):
        """
        Валидация имени файла: проверка на ASCII символы и разрешенные расширения.
        """
        if not value.isascii(): # Проверка на наличие символов из таблицы ASCII
            raise serializers.ValidationError(
                "Please, provide a valid file name. Must be ASCII characters only"
            )

        if not check_extension(value): # Проверка на доступные расширения
            raise serializers.ValidationError(
                "Valid file extensions: ['.csv', '.doc', '.pdf', '.xlsx', '.txt']"
            )

        return value

    def create(self, validated_data):  # Переопределяем метод create для обработки загрузки файла
        # Получаем имя файла из валидированных данных
        file_name = validated_data['file_name']
        file_path = create_file_path(file_name=file_name)  # Создаем путь для сохранения файла

        # raw_file - это сам файл, переданный через request.FILES.
        # Мы передаем его в сериализатор через `context` в представлении.
        raw_file = self.context.get('raw_file')

        if raw_file is None:
            raise serializers.ValidationError("No file content provided.")

        if check_file_size(file=raw_file): # Проверяем размер файла
            save_file(file_path=file_path, file_content=raw_file) # Сохраняем файл

            validated_data['file_path'] = file_path # Добавляем путь файла в validated_data

            project_file = ProjectFile.objects.create(**validated_data)

            return project_file
        else:  # Если файл слишком большой
            raise serializers.ValidationError(  # Поднимаем исключение валидации
                "File size is too large (2 MB as maximum)."
            )

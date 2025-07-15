from django.contrib.auth.models import User # Импортируем встроенную модель User Django
from django.db import models

# Импортируем наши модели из других приложений и утилиты
from apps.projects.models.project import Project
from apps.tasks.choices.statuses import Statuses
from apps.tasks.choices.priorities import Priorities
from apps.tasks.utils.set_end_of_the_month import calculate_end_of_month
from apps.tasks.models.tag import Tag # Импортируем Tag


class Task(models.Model):
    # name: строковое поле, макс. длина 120 символов
    name = models.CharField(
        max_length=120
    )
    # description: большое текстовое поле, обязательное
    description = models.TextField()
    # status: строковое поле, макс. длина 15, выбор из Statuses, по умолчанию NEW
    status = models.CharField(
        max_length=15,
        choices=Statuses.choices(), # Используем метод choices() из нашего Enum
        default=Statuses.NEW.value # Используем .value для получения строкового значения
    )
    # priority: маленькое целое число, выбор из Priorities, по умолчанию MEDIUM
    priority = models.SmallIntegerField(
        choices=Priorities.choices(), # Используем метод choices() из нашего Enum
        default=Priorities.MEDIUM[0] # Используем [0] для получения числового значения
    )
    # project: ForeignKey к Project. При удалении проекта задачи удаляются (CASCADE).
    # related_name='tasks' позволит обращаться к задачам проекта через project_instance.tasks.all()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, # Удаление проекта удаляет все связанные задачи
        related_name='tasks'
    )
    # tags: ManyToMany к Tag.
    # related_name='tasks' позволит обращаться к задачам, связанным с тегом, через tag_instance.tasks.all()
    tags = models.ManyToManyField(Tag, related_name='tasks')
    # created_at: дата и время создания, автозаполнение при создании
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at: дата и время обновления, автозаполнение при каждом сохранении
    updated_at = models.DateTimeField(auto_now=True)
    # deleted_at: может быть пустым (для "мягкого" удаления)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # deadline: дата и время, обязательно к заполнению. По умолчанию - последний день текущего месяца
    deadline = models.DateTimeField(default=calculate_end_of_month)
    # assignee: ForeignKey к User. Защита от удаления (PROTECT). Может быть пустым.
    assignee = models.ForeignKey(
        User,
        on_delete=models.PROTECT, # Защита: нельзя удалить пользователя, если у него есть задачи
        related_name='tasks',
        null=True, # Может быть null в базе данных
        blank=True # Может быть пустым в формах Django Admin
    )


    class Meta:
        # Сортировка по дедлайн дате в порядке убывания
        ordering = ['-deadline']
        # Уникальность по комбинации полей name и project
        # Это означает, что в одном проекте не может быть двух задач с одинаковым именем.
        unique_together = ('name', 'project')


    def __str__(self):
        # Строковое отображение: "название задачи, статус"
        return f"{self.name}, status: {self.status}"

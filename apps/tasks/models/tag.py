from django.db import models
from django.core.validators import MinLengthValidator # Импортируем валидатор для минимальной длины


class Tag(models.Model):
    # Поле name: строковое, максимальная длина 20 символов, минимальная длина 4 символа.
    name = models.CharField(max_length=20, validators=[MinLengthValidator(4)])

    def __str__(self):
        # Строковое отображение объекта будет его именем
        return self.name

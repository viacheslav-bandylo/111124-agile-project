from django.db import models


class Project(models.Model):
    # name: строковое поле, макс. длина 100, должно быть уникальным
    name = models.CharField(unique=True, max_length=100)
    # description: большое текстовое поле, обязательное к заполнению
    description = models.TextField()
    # created_at: поле даты и времени, заполняется автоматически при создании
    created_at = models.DateTimeField(auto_now_add=True)
    # files: связующее поле "Многие ко Многим" к ProjectFile.
    files = models.ManyToManyField('ProjectFile', related_name='projects')

    @property
    def count_of_files(self):
        # Динамическое поле, высчитывающее количество файлов для проекта
        return self.files.count()

    def __str__(self):
        # Строковое отображение объекта будет его именем
        return self.name

    class Meta:
        ordering = ["name"]




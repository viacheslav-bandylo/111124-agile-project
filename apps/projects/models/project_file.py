from django.db import models


class ProjectFile(models.Model):
    # file_name: строковое поле, макс. длина 120 символов
    file_name = models.CharField(max_length=120)
    # file_path: поле для загрузки файлов, сохраняется в папке 'documents/'
    file_path = models.FileField(upload_to='documents/')
    # created_at: дата создания, автозаполняется при создании
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Отображение объектов по имени файла
        return self.file_name

    class Meta:
        # Сортировка записей по дате создания в порядке убывания
        ordering = ['-created_at']

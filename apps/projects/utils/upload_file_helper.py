import os
from pathlib import Path


ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.txt']


def check_extension(filename: str) -> bool:
    """
    Проверяет, соответствует ли расширение файла разрешенным.
    """
    extension = Path(filename).suffix # Получаем расширение файла, включая точку (например, '.pdf')

    if extension not in ALLOWED_EXTENSIONS:
        return False

    return True


def check_file_size(file, required_size_mb=2) -> bool:
    """
    Проверяет размер файла.
    :param file: Объект UploadedFile из request.FILES
    :param required_size_mb: Максимально допустимый размер файла в мегабайтах
    """
    file_size_mb = file.size / (1024 * 1024) # Переводим размер файла из байтов в мегабайты

    if file_size_mb > required_size_mb:
        return False

    return True


def create_file_path(file_name: str) -> str:
    """
    Создает путь для сохранения файла в папке 'documents/'.
    """
    parts = file_name.rsplit('.', 1) # Разделяем по последней точке, максимум 1 раз
    new_file_name = parts[0]
    file_ext = parts[1]

    file_path = os.path.join("documents", f"{new_file_name}.{file_ext}")

    return file_path


def save_file(file_path: str, file_content):
    """
    Сохраняет файл по частям для избежания проблем с большими файлами.
    :param file_path: Полный путь, по которому нужно сохранить файл.
    :param file_content: Объект UploadedFile из request.FILES.
    """
    # Создаем директории, если их нет. exist_ok=True предотвращает ошибку, если папка уже есть.
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb') as f: # Открываем файл в бинарном режиме для записи
        for chunk in file_content.chunks(): # Читаем файл по частям (чанками)
            f.write(chunk) # Записываем каждую часть

    return file_path

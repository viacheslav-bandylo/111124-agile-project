from enum import Enum # Импортируем класс Enum

class Priorities(Enum):
    # Для приоритета мы используем кортежи (число, строка), чтобы хранить числовое значение
    # (которое будет храниться в БД) и более понятное строковое описание.
    VERY_LOW = (1, 'Very Low')
    LOW = (2, 'Low')
    MEDIUM = (3, 'Medium')
    HIGH = (4, 'High')
    CRITICAL = (5, 'Critical')

    @classmethod
    def choices(cls):
        # Этот метод форматирует Enum-значения для использования в `choices` поля модели.
        return [(key.value[0], key.value[1]) for key in cls]

    def __getitem__(self, item):
        # Этот метод позволяет нам обращаться к значениям кортежа как к элементам списка,
        # например Priority.MEDIUM[0] для получения числа.
        return self.value[item]

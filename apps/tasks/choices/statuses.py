from enum import Enum # Импортируем класс Enum

class Statuses(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    TESTING = "TESTING"
    CLOSED = "CLOSED"

    @classmethod
    def choices(cls):
        # Этот метод позволяет использовать Enum-значения как CHOICES для поля Django модели
        return [(attr.name, attr.value) for attr in cls]

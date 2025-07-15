from datetime import datetime
import calendar

from django.utils import timezone # Используем timezone для работы с часовыми поясами


def calculate_end_of_month() -> datetime:
    current_date = timezone.now() # Получаем текущую дату и время с учетом часового пояса
    amount_of_days = calendar.monthrange( # Определяем количество дней в текущем месяце
        current_date.year,
        current_date.month
    )[1]
    date = datetime( # Создаем объект datetime для последнего дня текущего месяца
        year=current_date.year,
        month=current_date.month,
        day=amount_of_days,
    )

    return date.astimezone() # Переводим дату в текущую временную зону и возвращаем

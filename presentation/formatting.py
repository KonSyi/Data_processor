"""Форматирование сырых доменных данных в строки для UI."""
import re
@staticmethod
def axis_label(quantity: str | None, unit: str | None) -> str:
    """('time', 's') -> 'Время, с'. Если quantity неизвестен — fallback на unit.
    TODO: словарь quantity->русское имя; собрать 'имя, единица'.
    """
    ...

@staticmethod
def format_float(value: float, digits: int = 3) -> str:
    """Число с фиксированным числом знаков."""
    return f"{value:.6g}"

@staticmethod
def format_int(value: int) -> str:
    """Целое для отображения"""
    return f"{value:,}".replace(",", " ")

@staticmethod
def safe_filename(name: str) -> str:
    """Очистить строку для использования в имени файла (экспорт)."""
    cleaned = name.replace("/", "_").replace("\\", "_")
    cleaned = re.sub(r'[^0-9A-Za-zА-Яа-я._ -]+', "_", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "channel"
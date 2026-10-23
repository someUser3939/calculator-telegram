import logging  # Используем стандартные уровни логирования Python.
import os  # Читаем настройки из переменных окружения.

from dotenv import load_dotenv  # Загружаем переменные из локального файла .env.

load_dotenv()  # Поддерживаем запуск на компьютере без ручного экспорта переменных.

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()  # Читаем и очищаем токен бота.
if not BOT_TOKEN:  # Проверяем, что токен задан до запуска приложения.
    raise RuntimeError("BOT_TOKEN is not set. Copy .env.example to .env and add your Telegram bot token.")  # Показываем понятную ошибку настройки.

log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()  # Читаем уровень логирования с безопасным значением по умолчанию.
LOG_LEVEL = getattr(logging, log_level_name, None)  # Находим соответствующую константу logging.
if not isinstance(LOG_LEVEL, int):  # Отклоняем неизвестное значение вместо тихого fallback.
    raise RuntimeError(f"Invalid LOG_LEVEL: {log_level_name}")  # Показываем некорректный уровень в тексте ошибки.

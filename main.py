import asyncio  # Запускаем асинхронный цикл приложения.
import logging  # Настраиваем логи для диагностики запуска и ошибок.

from aiogram import Bot, Dispatcher  # Импортируем Telegram-клиент и диспетчер обновлений.
from aiogram.fsm.storage.memory import MemoryStorage  # Храним состояния диалога в памяти процесса.

from config.settings import BOT_TOKEN, LOG_LEVEL  # Загружаем токен бота и уровень логирования.
from handlers.user import router as user_router  # Подключаем обработчики команд и калькулятора.


async def main() -> None:  # Запускаем бота и обслуживаем входящие сообщения.
    logging.basicConfig(  # Настраиваем формат логов приложения.
        level=LOG_LEVEL,  # Показываем сообщения выбранного уровня и выше.
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",  # Добавляем время, уровень и источник лога.
    )  # Завершаем настройку логирования.
    bot = Bot(token=BOT_TOKEN)  # Создаём Telegram-клиент с секретным токеном.
    dispatcher = Dispatcher(storage=MemoryStorage())  # Создаём диспетчер и хранилище шагов диалога.
    dispatcher.include_router(user_router)  # Регистрируем пользовательские команды и обработчики.

    try:  # Запускаем long polling и гарантируем закрытие сетевой сессии.
        await dispatcher.start_polling(bot)  # Получаем обновления Telegram без публичного веб-сервера.
    finally:  # Выполняем очистку также при штатной остановке или ошибке.
        await bot.session.close()  # Закрываем HTTP-сессию бота.


if __name__ == "__main__":  # Запускаем приложение только при прямом запуске этого файла.
    asyncio.run(main())  # Создаём цикл событий и запускаем асинхронную функцию.

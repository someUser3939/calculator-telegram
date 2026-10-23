# Telegram calculator bot

Асинхронный Telegram-бот на Python и aiogram 3. Диалог предлагает ввести два числа, выбрать `+`, `-`, `*` или `/`, затем отправляет ответ. Поддерживаются десятичные числа с точкой или запятой; деление на ноль отклоняется. Команда `/cancel` отменяет текущий расчёт.

## Подготовка

1. Создайте бота через [@BotFather](https://t.me/BotFather) и скопируйте его токен.
2. Установите Python 3.10 или новее.
3. Скопируйте `.env.example` в `.env` и укажите настоящий токен в `BOT_TOKEN`.

Не публикуйте `.env` и не отправляйте токен в репозиторий.

## Запуск локально

В PowerShell из корневой папки проекта:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Бот работает через long polling: для запуска не нужны публичный IP-адрес, домен или HTTPS. Оставьте процесс работающим, чтобы бот принимал сообщения.

## Запуск через Docker Compose

Установите Docker Desktop, создайте `.env` по инструкции выше, затем в корневой папке проекта выполните:

```powershell
docker compose up --build -d
docker compose logs -f
```

Остановка:

```powershell
docker compose down
```

Для обновления кода повторно выполните `docker compose up --build -d`. Запускайте только один экземпляр polling-бота с данным токеном одновременно.

## Тесты

```powershell
python -m unittest discover -s tests -v
```

Состояния диалога хранятся в памяти процесса. После перезапуска незавершённый расчёт потребуется начать снова командой `/start`.

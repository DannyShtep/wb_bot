# Используем конкретную версию Python, совместимую с aiogram 2.x и aiohttp 3.9.x
FROM python:3.11-slim-buster

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt из папки wb_bot
COPY wb_bot/requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код из папки wb_bot в рабочую директорию контейнера (/app)
COPY wb_bot/ .

# Команда для запуска бота
CMD ["python", "bot.py"]

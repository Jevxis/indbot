# Указываем базовый образ
FROM python:3.8-slim-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Указываем, какие файлы скопировать в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду, которая будет запускаться при старте контейнера
CMD ["python", "bot_telegram.py"]
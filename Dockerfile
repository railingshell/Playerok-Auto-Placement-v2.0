# syntax=docker/dockerfile:1
FROM python:3.12-slim

LABEL org.opencontainers.image.title="Playerok Auto Placement" \
      org.opencontainers.image.description="Многофункциональный бот-помощник для Playerok" \
      org.opencontainers.image.source="https://github.com/railingshell/Playerok-Auto-Placement-v2.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Системные зависимости для сборки некоторых Python-пакетов (curl-cffi, lxml)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала зависимости — для эффективного кеширования слоёв
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Затем исходники
COPY . .

# Данные, настройки и логи выносим в тома, чтобы они переживали пересоздание контейнера
VOLUME ["/app/bot_settings", "/app/bot_data", "/app/logs"]

CMD ["python", "bot.py"]

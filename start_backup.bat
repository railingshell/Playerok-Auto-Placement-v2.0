@echo off
chcp 65001 >nul
title PAP — Playerok Auto Placement

echo.
echo =========================================
echo   Playerok Auto Placement v2.0
echo =========================================
echo.

echo [1/2] Проверка обновлений...
python updater.py
if errorlevel 1 (
    echo [!] Не удалось проверить обновления, запускаю бота всё равно...
)

echo.
echo [2/2] Запуск Telegram-бота...
python bot.py

pause

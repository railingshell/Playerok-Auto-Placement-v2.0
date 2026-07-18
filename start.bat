@echo off
title PAP — Playerok Auto Placement

echo.
echo =========================================
echo   Playerok Auto Placement v2.0
echo =========================================
echo.

echo [1/2] Checking for updates...
python updater.py
if errorlevel 1 (
    echo [WARNING] Update check failed, starting bot anyway...
)

echo.
echo [2/2] Starting Telegram bot...
python bot.py

pause

@echo off
chcp 1251 >nul
TITLE Playerok Auto Placement v2.0
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0menu.ps1" -Action menu

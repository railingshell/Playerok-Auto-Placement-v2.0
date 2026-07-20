@echo off
chcp 65001 >nul
TITLE Playerok Auto Placement v2.0
powershell -NoProfile -File "%~dp0menu.ps1" -Action menu

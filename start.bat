@echo off
chcp 65001 >nul
TITLE Playerok Auto Placement v2.0
powershell -NoProfile -ExecutionPolicy Bypass -Command "$OutputEncoding=[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; & '%~dp0menu.ps1' -Action menu"

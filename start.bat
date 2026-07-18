@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul

:: Window title
TITLE Playerok Auto Placement v2.0

:: Clear screen
cls

call :draw_header

call :draw_line
call :draw_progress "Loading system" 20
call :draw_progress "Connecting modules" 45
call :draw_progress "Checking GitHub API" 70
call :draw_progress "Ready to launch" 100

echo.
echo.

:menu
cls
call :draw_header

call :box "MAIN MENU"
echo    [1]  Start Telegram Bot
echo    [2]  Check for Updates
echo    [3]  Push to GitHub
echo    [4]  Create Release
echo    [5]  Open Project Folder
echo    [6]  Exit
echo.
call :draw_line
set /p choice=Select option [1-6]: 

if "%choice%"=="1" goto start_bot
if "%choice%"=="2" goto check_updates
if "%choice%"=="3" goto push_github
if "%choice%"=="4" goto create_release
if "%choice%"=="5" goto open_folder
if "%choice%"=="6" goto exit_menu

echo [ERROR] Invalid option. Press any key...
pause >nul
goto menu

:start_bot
cls
call :draw_header
echo.
echo [1/2] Checking for updates...
python updater.py
if errorlevel 1 (
    echo [WARNING] Update check failed, starting bot anyway...
)
echo.
echo [2/2] Starting Telegram bot...
python bot.py
echo.
echo [INFO] Bot stopped. Press any key to return to menu...
pause >nul
goto menu

:check_updates
cls
call :draw_header
echo.
echo [>] Checking for updates...
python updater.py
echo.
echo [INFO] Done. Press any key...
pause >nul
goto menu

:push_github
cls
call :draw_header
echo.
set /p msg=Enter commit message: 
if "%msg%"=="" set msg=Auto update
git add -A
git commit -m "%msg%"
git push origin main
echo.
echo [INFO] Done. Press any key...
pause >nul
goto menu

:create_release
cls
call :draw_header
echo.
echo [>] Creating GitHub release...
python create_release.py
echo.
echo [INFO] Done. Press any key...
pause >nul
goto menu

:open_folder
cls
call :draw_header
echo.
echo [>] Opening project folder...
explorer "%CD%"
echo [INFO] Done. Press any key...
pause >nul
goto menu

:exit_menu
cls
call :draw_header
echo.
echo [OK] Goodbye!
timeout /t 2 >nul
exit /b 0

:draw_header
echo.
echo +---------------------------------------------+
echo ^|        Playerok Auto Placement v2.0         ^|
echo ^|             by @lovesort (rogart)           ^|
echo +---------------------------------------------+
echo ^|  Telegram: @rogartproduction                ^|
echo ^|  Plugins:  t.me/lovesort                    ^|
echo +---------------------------------------------+
echo.
goto :eof

:draw_line
echo -------------------------------------------------
goto :eof

:box
set "text=%~1"
echo +---------------------------------------------+
echo ^|  %text%
echo +---------------------------------------------+
goto :eof

:draw_progress
set "label=%~1"
set "percent=%~2"
set /a filled=%percent% / 5
set /a empty=20 - %filled%
set "bar="
for /l %%i in (1,1,%filled%) do set "bar=!bar!#"
for /l %%i in (1,1,%empty%) do set "bar=!bar!-"
echo    [ %bar% ] %percent%%  %label%
timeout /t 1 >nul
goto :eof

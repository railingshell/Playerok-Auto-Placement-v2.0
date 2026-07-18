@echo off
setlocal EnableDelayedExpansion
chcp 1251 >nul

:: === COLORS ===
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
    set "ESC=%%b"
)
set "RST=%ESC%[0m"
set "BOLD=%ESC%[1m"
set "DIM=%ESC%[2m"
set "UNDERLINE=%ESC%[4m"
set "BLINK=%ESC%[5m"
set "CYAN=%ESC%[36m"
set "LCYAN=%ESC%[96m"
set "GREEN=%ESC%[32m"
set "LGREEN=%ESC%[92m"
set "YELLOW=%ESC%[33m"
set "LYELLOW=%ESC%[93m"
set "RED=%ESC%[31m"
set "LRED=%ESC%[91m"
set "MAGENTA=%ESC%[35m"
set "LMAGENTA=%ESC%[95m"
set "BLUE=%ESC%[34m"
set "LBLUE=%ESC%[94m"
set "WHITE=%ESC%[37m"
set "LWHITE=%ESC%[97m"
set "GRAY=%ESC%[90m"
set "DGRAY=%ESC%[30;1m"
set "BG_BLUE=%ESC%[44m"
set "BG_CYAN=%ESC%[46m"
set "BG_GREEN=%ESC%[42m"

:: === TITLE ===
TITLE Playerok Auto Placement v2.0

:: === CLEAR ===
cls

:: === INTRO ===
call :draw_header

echo %LCYAN%  [ PRE-BOOT ]%RST% Inicializaciya sistemy...%RST%
echo.

set /a step=0
for %%a in ("Zagruzka yadra" "Podklyuchenie moduley" "Proverka GitHub API" "Sinhronizaciya dannyh") do (
    set /a step+=25
    call :draw_progress %%~a !step!
)

echo.
echo %BG_GREEN%%LWHITE% [ OK ] %RST% %LGREEN%Sistema gotova k rabote%RST%
timeout /t 1 >nul

:: === MAIN MENU ===
:menu
cls
call :draw_header

call :box "GLAVNOE MENYU"
echo.
echo  %LGREEN%[1]%RST%  ->  Zapustit Telegram bota
echo  %LCYAN%[2]%RST%  ->  Proverit obnovleniya
echo  %LBLUE%[3]%RST%  ->  Zapushit izmeneniya na GitHub
echo  %LMAGENTA%[4]%RST%  ->  Sozdat novyj reliz
echo  %LYELLOW%[5]%RST%  ->  Otkryt papku proekta
echo  %LRED%[6]%RST%  ->  Vyjti
.
echo.
call :draw_line
set /p choice=%LWHITE%  Vyberite dejstvie [1-6]: %RST%

if "%choice%"=="1" goto start_bot
if "%choice%"=="2" goto check_updates
if "%choice%"=="3" goto push_github
if "%choice%"=="4" goto create_release
if "%choice%"=="5" goto open_folder
if "%choice%"=="6" goto exit_menu

echo.
echo %BG_RED%%LWHITE% [ OSIBKA ] %RST% %LRED%Nevernyj punkt menyu. Poprobujte eshche raz.%RST%
timeout /t 2 >nul
goto menu

:start_bot
cls
call :draw_header
echo.
echo %LCYAN%[ SHAG 1 / 2 ]%RST% Proverka obnovlenij...%RST%
echo.
python updater.py
if errorlevel 1 (
    echo.
    echo %LYELLOW%[ VNIMANIE ] Ne udalos proverit obnovleniya. Zapusk bota vse ravno...%RST%
)
echo.
echo %LGREEN%[ SHAG 2 / 2 ]%RST% Zapusk Telegram bota...%RST%
echo.
python bot.py
echo.
echo %GRAY%[ INFO ] Bot ostanovlen. Najmite lyubuyu klavishu dlya vozvrata v menyu.%RST%
pause >nul
goto menu

:check_updates
cls
call :draw_header
echo.
echo %LCYAN%[ PROVERKA ]%RST% Otpravka zaprosa k GitHub API...%RST%
echo.
python updater.py
echo.
echo %GRAY%[ INFO ] Proverka zavershena. Najmite lyubuyu klavishu.%RST%
pause >nul
goto menu

:push_github
cls
call :draw_header
echo.
set /p msg=%LWHITE%  Vvedite soobshenie kommita: %RST%
if "%msg%"=="" set msg=Avtoobnovlenie ot %date%

echo.
echo %LBLUE%[1/3]%RST% Dobavlenie fajlov v indeks...
git add -A

echo %LBLUE%[2/3]%RST% Sozdanie kommita...
git commit -m "%msg%"

echo %LBLUE%[3/3]%RST% Otpravka na GitHub...
git push origin main

echo.
echo %BG_GREEN%%LWHITE% [ GOTOWO ] %RST% %LGREEN%Izmeneniya otpravleny.%RST%
echo %GRAY%Najmite lyubuyu klavishu dlya vozvrata.%RST%
pause >nul
goto menu

:create_release
cls
call :draw_header
echo.
echo %LMAGENTA%[ RELIZ ]%RST% Sozdanie novogo reliza na GitHub...%RST%
echo.
python create_release.py
echo.
echo %GRAY%[ INFO ] Operaciya zavershena. Najmite lyubuyu klavishu.%RST%
pause >nul
goto menu

:open_folder
cls
call :draw_header
echo.
echo %LYELLOW%[ PAPKA ]%RST% Otkrytie direktorii proekta...%RST%
explorer "%CD%"
echo.
echo %GRAY%[ INFO ] Gotovo. Najmite lyubuyu klavishu.%RST%
pause >nul
goto menu

:exit_menu
cls
call :draw_header
echo.
echo %BG_GREEN%%LWHITE% [ DO SVIDANIYA ] %RST% %LGREEN%Spasibo za ispolzovanie!%RST%
timeout /t 2 >nul
exit /b 0

:draw_header
echo.
echo %LCYAN%+============================================================+%RST%
echo %LCYAN%|%RST%              %BOLD%Playerok Auto Placement v2.0%RST%                    %LCYAN%|%RST%
echo %LCYAN%|%RST%                  %GRAY%by%RST% %LMAGENTA%@lovesort%RST% %GRAY%(rogart)%RST%                       %LCYAN%|%RST%
echo %LCYAN%+============================================================+%RST%
echo %LCYAN%|%RST%  %LBLUE%Telegram:%RST% @rogartproduction                              %LCYAN%|%RST%
echo %LCYAN%|%RST%  %LBLUE%Plaginy: %RST% t.me/lovesort                                 %LCYAN%|%RST%
echo %LCYAN%+============================================================+%RST%
echo.
goto :eof

:draw_line
echo %DGRAY%--------------------------------------------------------------%RST%
goto :eof

:box
set "text=%~1"
echo %LCYAN%+============================================================+%RST%
echo %LCYAN%|%RST%  %BOLD%%LWHITE%%text%%RST%                                            %LCYAN%|%RST%
echo %LCYAN%+============================================================+%RST%
goto :eof

:draw_progress
set "label=%~1"
set /a percent=%~2
set /a filled=%percent% / 2
set /a empty=50 - %filled%
set "bar="
for /l %%i in (1,1,%filled%) do set "bar=!bar!#"
for /l %%i in (1,1,%empty%) do set "bar=!bar!-"
set /a num=%percent%
if %num% lss 10 set "num=  %num%"
if %num% lss 100 if %num% gtr 9 set "num= %num%"
echo %LCYAN%  [ %LGREEN%%bar%%LCYAN% ] %LWHITE%%num%%%RST% %GRAY%- %label%%RST%
timeout /t 1 >nul
goto :eof

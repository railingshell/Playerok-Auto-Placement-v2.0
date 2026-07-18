@echo off

set REPO_URL=https://github.com/railingshell/Playerok-Auto-Placement-v2.0.git
set GIT_USER=railingshell
set GIT_EMAIL=railingshell@gmail.com

echo.
echo =========================================
echo   Push Playerok Auto Placement v2.0
echo   to GitHub
echo =========================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found. Download from https://git-scm.com/download/win
    pause
    exit /b 1
)

git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [1/7] Init git...
    git init
) else (
    echo [1/7] Git already inited.
)

echo [2/7] Set branch name...
git branch -M main

echo [3/7] Set user identity...
git config user.name "%GIT_USER%"
git config user.email "%GIT_EMAIL%"
git config credential.helper ""

echo [4/7] Add files...
git add .

echo [5/7] Commit...
git commit -m "Initial commit: Playerok Auto Placement v2.0"

echo [6/7] Add remote...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo [7/7] Push to GitHub...
git push -u origin main --force

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Check URL and token.
) else (
    echo.
    echo [OK] Repository uploaded!
)

pause

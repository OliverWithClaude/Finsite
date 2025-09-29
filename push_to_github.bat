@echo off
echo ========================================
echo    Finsite - Push to GitHub
echo ========================================
echo.

REM Check if remote exists
git remote -v > nul 2>&1
if %errorlevel% neq 0 (
    echo No remote repository configured.
    echo.
    set /p github_url="Enter your GitHub repository URL (e.g., https://github.com/yourusername/Finsite.git): "
    git remote add origin %github_url%
    echo Remote repository added.
) else (
    echo Remote repository already configured.
    git remote -v
)

echo.
echo Pushing to GitHub...

REM Rename branch to main if necessary
git branch -M main

REM Push to GitHub
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    Successfully pushed to GitHub!
    echo ========================================
    echo.
    echo Your code is now on GitHub!
) else (
    echo.
    echo ========================================
    echo    Push failed!
    echo ========================================
    echo.
    echo Please check:
    echo 1. You've created the repository on GitHub
    echo 2. The repository URL is correct
    echo 3. You're logged in to Git (try: git config --global user.name)
)

echo.
pause

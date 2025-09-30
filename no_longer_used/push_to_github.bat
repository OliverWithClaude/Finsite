@echo off
echo ========================================
echo    Finsite - Push to GitHub
echo ========================================
echo.

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo Adding GitHub remote repository...
    git remote add origin https://github.com/OliverWithClaude/Finsite.git
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
    echo Your code is now live at:
    echo https://github.com/OliverWithClaude/Finsite
    echo.
) else (
    echo.
    echo ========================================
    echo    Push failed!
    echo ========================================
    echo.
    echo Troubleshooting:
    echo.
    echo 1. Make sure you're logged in to Git:
    echo    git config --global user.name "YourGitHubUsername"
    echo    git config --global user.email "your.email@example.com"
    echo.
    echo 2. If authentication fails, you may need a Personal Access Token:
    echo    - Go to GitHub Settings > Developer settings > Personal access tokens
    echo    - Generate a new token with 'repo' scope
    echo    - Use the token as your password when prompted
    echo.
    echo 3. Try pushing manually:
    echo    git remote add origin https://github.com/OliverWithClaude/Finsite.git
    echo    git branch -M main
    echo    git push -u origin main
)

echo.
pause

@echo off
echo ========================================
echo    Finsite - Commit Changes
echo ========================================
echo.

REM Check for changes
git status

echo.
set /p commit_message="Enter commit message: "

REM Add all changes
git add .

REM Commit changes
git commit -m "%commit_message%"

if %errorlevel% equ 0 (
    echo.
    echo Changes committed successfully!
    echo.
    set /p push_changes="Push to GitHub? (y/n): "
    if /i "%push_changes%"=="y" (
        git push origin main
        echo Changes pushed to GitHub!
    )
) else (
    echo.
    echo No changes to commit or commit failed.
)

echo.
pause

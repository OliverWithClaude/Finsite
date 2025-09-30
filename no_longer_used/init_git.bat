@echo off
echo ========================================
echo    Finsite - Git Repository Setup
echo ========================================
echo.

REM Initialize git repository
echo Initializing Git repository...
git init

REM Add all files
echo Adding files to Git...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: Finsite - Investment Intelligence with Grit"

echo.
echo ========================================
echo    Git repository initialized!
echo ========================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub named 'Finsite'
echo 2. Run 'push_to_github.bat' to push your code
echo.
pause

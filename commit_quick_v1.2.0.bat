@echo off
echo ================================================
echo Finsite v1.2.0 - Quick Commit (Review Before Push)
echo ================================================
echo.

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not in a git repository!
    pause
    exit /b 1
)

echo Adding all changes...
git add .

echo.
echo Creating commit...
git commit -m "Release v1.2.0: Complete Visual Analytics Platform" ^
    -m "" ^
    -m "Features:" ^
    -m "- Interactive charts for all positions (open + closed)" ^
    -m "- Persistent sidebar layout" ^
    -m "- Price data caching" ^
    -m "- Mobile responsive design" ^
    -m "" ^
    -m "See RELEASE_NOTES_v1.2.0.md for details"

echo.
echo Creating tag...
git tag -a v1.2.0 -m "Version 1.2.0 - Visual Insight Plus"

echo.
echo ================================================
echo Commit created successfully!
echo ================================================
echo.
echo To push to GitHub, run:
echo   git push origin main
echo   git push origin --tags
echo.
echo Or use commit_v1.2.0.bat for guided push.
echo.

pause

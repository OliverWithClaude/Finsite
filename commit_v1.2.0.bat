@echo off
echo ================================================
echo Finsite v1.2.0 - Git Commit and Push
echo ================================================
echo.

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not in a git repository!
    echo Please run 'git init' first or navigate to your git repository.
    pause
    exit /b 1
)

echo Step 1: Checking git status...
echo ================================================
git status
echo.

echo Step 2: Adding all changes...
echo ================================================
git add .
echo All changes staged.
echo.

echo Step 3: Creating commit...
echo ================================================
git commit -m "Release v1.2.0: Complete Visual Analytics Platform" -m "Major Features:" -m "- Interactive price charts for closed positions (v1.1.0)" -m "- Interactive price charts for open positions (v1.1.1)" -m "- Persistent sidebar layout with dynamic content (v1.1.2)" -m "" -m "New Features:" -m "- Plotly-powered interactive charts with zoom, pan, hover" -m "- Entry/Exit/Current price markers on charts" -m "- Smart date ranges (recent vs historical positions)" -m "- Price data caching for fast subsequent loads" -m "- Persistent left sidebar with watchlist always visible" -m "- Dynamic right content area (Company Info / Open Positions / Closed Positions)" -m "" -m "Technical Improvements:" -m "- New PriceHistoryService with intelligent caching" -m "- New price_history database table" -m "- New API endpoint: /api/positions/{id}/chart-data" -m "- Improved layout structure with fixed sidebar + flexible content" -m "- Mobile responsive design" -m "" -m "Performance:" -m "- Chart first load: 2-4 seconds" -m "- Chart cached load: <1 second" -m "- Minimized API calls through caching" -m "" -m "Files Changed:" -m "- Backend: position_service.py, price_history_service.py (NEW), database.py, models.py, main.py" -m "- Frontend: index.html, main.js, style.css" -m "- Config: version.py (v1.2.0), requirements.txt (added plotly)" -m "- Docs: Multiple implementation and release docs" -m "" -m "Breaking Changes: None - Fully backward compatible" -m "" -m "Dependencies Added:" -m "- plotly==5.24.1" -m "" -m "See RELEASE_NOTES_v1.2.0.md for complete details."
echo.

if errorlevel 1 (
    echo ERROR: Commit failed!
    pause
    exit /b 1
)

echo Commit created successfully!
echo.

echo Step 4: Creating git tag...
echo ================================================
git tag -a v1.2.0 -m "Version 1.2.0 - Visual Insight Plus" -m "Complete visual analytics platform with interactive charts for all positions and improved layout."
echo Tag v1.2.0 created.
echo.

echo Step 5: Pushing to GitHub...
echo ================================================
echo.
echo Ready to push to GitHub!
echo This will push:
echo   - All commits
echo   - Tag v1.2.0
echo.
set /p CONFIRM="Do you want to push now? (Y/N): "

if /i "%CONFIRM%"=="Y" (
    echo.
    echo Pushing commits...
    git push origin main
    
    if errorlevel 1 (
        echo.
        echo WARNING: Push failed. You might need to specify the correct branch name.
        echo Common branch names: main, master
        echo.
        echo Try manually with:
        echo   git push origin [your-branch-name]
        echo   git push origin --tags
        pause
        exit /b 1
    )
    
    echo.
    echo Pushing tags...
    git push origin --tags
    
    echo.
    echo ================================================
    echo SUCCESS! Version 1.2.0 pushed to GitHub
    echo ================================================
    echo.
    echo Next steps:
    echo 1. Visit your GitHub repository
    echo 2. Go to Releases section
    echo 3. Click "Draft a new release"
    echo 4. Select tag v1.2.0
    echo 5. Copy content from RELEASE_NOTES_v1.2.0.md
    echo 6. Publish release
    echo.
) else (
    echo.
    echo Push cancelled. You can push manually later with:
    echo   git push origin main
    echo   git push origin --tags
    echo.
)

echo.
echo ================================================
echo Git Summary
echo ================================================
git log --oneline -1
echo.
git tag -l v1.2.0
echo.

echo Done!
pause

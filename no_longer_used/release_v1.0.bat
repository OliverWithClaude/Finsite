@echo off
echo ========================================
echo Finsite v1.0.0 Release Process
echo ========================================
echo.

:menu
echo What would you like to do?
echo.
echo [1] Commit all changes
echo [2] Create and push tag v1.0.0
echo [3] Push everything to GitHub
echo [4] View current tags
echo [5] View git status
echo [6] Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto commit
if "%choice%"=="2" goto tag
if "%choice%"=="3" goto push
if "%choice%"=="4" goto viewtags
if "%choice%"=="5" goto status
if "%choice%"=="6" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:commit
echo.
echo ========================================
echo Committing Changes
echo ========================================
cd /d C:\Claude\Finsite
git add .
git status
echo.
set /p confirm="Commit these changes? (y/n): "
if /i "%confirm%"=="y" (
    git commit -m "Release v1.0.0 - Foundation - Complete position tracking system - Open/closed position management - Live market data integration - Delete functionality for closed positions - Simplified close workflow - Full documentation and release notes"
    echo.
    echo ✓ Changes committed!
) else (
    echo Commit cancelled.
)
echo.
pause
goto menu

:tag
echo.
echo ========================================
echo Creating Tag v1.0.0
echo ========================================
cd /d C:\Claude\Finsite
echo Checking if tag exists...
git tag -l v1.0.0
echo.
set /p proceed="Create tag v1.0.0? (y/n): "
if /i "%proceed%"=="y" (
    git tag -a v1.0.0 -m "Finsite v1.0.0 - Foundation Release - First official release of Finsite investment workbench - Watchlist management with live market data - Open position tracking with real-time valuations - Closed position history with P/L analysis - SQLite database for local storage - Clean, responsive UI with Optimistic Grit design"
    echo.
    echo ✓ Tag v1.0.0 created!
    echo.
    echo Push tag to GitHub? (y/n)
    set /p pushtag="Push tag? (y/n): "
    if /i "%pushtag%"=="y" (
        git push origin v1.0.0
        echo ✓ Tag pushed to GitHub!
    )
) else (
    echo Tag creation cancelled.
)
echo.
pause
goto menu

:push
echo.
echo ========================================
echo Pushing to GitHub
echo ========================================
cd /d C:\Claude\Finsite
echo This will push commits and tags to GitHub.
echo.
set /p pushconfirm="Continue? (y/n): "
if /i "%pushconfirm%"=="y" (
    echo Pushing commits...
    git push origin main
    echo.
    echo Pushing tags...
    git push origin --tags
    echo.
    echo ✓ Everything pushed to GitHub!
    echo.
    echo Next steps:
    echo 1. Go to https://github.com/yourusername/finsite/releases
    echo 2. Click "Draft a new release"
    echo 3. Select tag v1.0.0
    echo 4. Copy content from RELEASE_NOTES_v1.0.md
    echo 5. Publish release
) else (
    echo Push cancelled.
)
echo.
pause
goto menu

:viewtags
echo.
echo ========================================
echo Git Tags
echo ========================================
cd /d C:\Claude\Finsite
git tag -l
echo.
echo To see tag details:
git show v1.0.0 --quiet
echo.
pause
goto menu

:status
echo.
echo ========================================
echo Git Status
echo ========================================
cd /d C:\Claude\Finsite
git status
echo.
echo Recent commits:
git log --oneline -5
echo.
pause
goto menu

:end
echo.
echo ========================================
echo Release process ended.
echo.
echo To complete the release:
echo 1. Visit https://github.com/yourusername/finsite/releases
echo 2. Create a new release from tag v1.0.0
echo 3. Use RELEASE_NOTES_v1.0.md for description
echo.
echo Thank you for using Finsite!
echo ========================================
pause

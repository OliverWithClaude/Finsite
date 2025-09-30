@echo off
echo ========================================
echo    Finsite - Quick Branch Fix
echo ========================================
echo.

echo This script will consolidate everything into the 'main' branch
echo and remove the empty 'master' branch.
echo.

rem Make sure we're on main
echo Step 1: Switching to main branch...
git checkout main

rem Push main to remote if not already
echo.
echo Step 2: Ensuring main is up to date...
git push origin main

rem Force push main content to master (overwrites master)
echo.
echo Step 3: Copying main content to master...
git push origin main:master --force

rem Now both branches have the same content
echo.
echo ========================================
echo    MANUAL STEP REQUIRED
echo ========================================
echo.
echo NOW you need to:
echo.
echo 1. Open: https://github.com/OliverWithClaude/Finsite/settings/branches
echo.
echo 2. Change default branch from 'master' to 'main':
echo    - Click on the two-arrow switch button
echo    - Select 'main' from the dropdown
echo    - Click 'Update'
echo    - Click 'I understand, update the default branch'
echo.
echo 3. After changing the default branch, press any key here...
echo.
pause

rem Now delete the master branch
echo.
echo Step 4: Deleting the old master branch...
git push origin --delete master

echo.
echo ========================================
echo    ✓ COMPLETE!
echo ========================================
echo.
echo Your repository now uses 'main' as the only branch.
echo.
echo Verifying...
git branch -a
echo.
echo Your code is live at:
echo https://github.com/OliverWithClaude/Finsite
echo.
pause

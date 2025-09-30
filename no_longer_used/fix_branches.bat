@echo off
echo ========================================
echo    Finsite - Fix Branch Structure
echo ========================================
echo.

echo Current branch status:
git branch -a
echo.

echo ========================================
echo Choose your preferred approach:
echo ========================================
echo.
echo 1. Keep 'main' as default (recommended - modern standard)
echo 2. Keep 'master' as default (traditional)
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Fixing branches - keeping 'main' as default...
    echo.
    
    rem Make sure we're on main
    git checkout main
    
    rem Force push main to master (overwrites master with main's content)
    git push origin main:master --force
    
    rem Push main as well
    git push origin main
    
    rem Set main as default branch
    echo.
    echo ========================================
    echo    IMPORTANT: Manual GitHub Step Required
    echo ========================================
    echo.
    echo 1. Go to: https://github.com/OliverWithClaude/Finsite/settings
    echo 2. Scroll to "Default branch" section
    echo 3. Click the switch branch button (two arrows)
    echo 4. Select "main" from dropdown
    echo 5. Click "Update"
    echo 6. Confirm the change
    echo.
    echo After doing this, press any key to continue...
    pause >nul
    
    rem Delete the master branch on remote
    git push origin --delete master
    
    rem Make sure we're tracking the right branch
    git branch --set-upstream-to=origin/main main
    
    echo.
    echo ✓ Successfully consolidated to 'main' branch!
    echo.
    
) else if "%choice%"=="2" (
    echo.
    echo Fixing branches - keeping 'master' as default...
    echo.
    
    rem Make sure we're on main first to get the code
    git checkout main
    
    rem Switch to master
    git checkout master
    
    rem Merge main into master (gets all the code)
    git merge main --allow-unrelated-histories
    
    rem Push the updated master
    git push origin master --force
    
    rem Delete main branch locally and remotely
    git branch -d main
    git push origin --delete main
    
    echo.
    echo ✓ Successfully consolidated to 'master' branch!
    echo.
    
) else (
    echo Invalid choice. Exiting...
    goto end
)

echo.
echo ========================================
echo    Branch Structure Fixed!
echo ========================================
echo.
echo Your repository now has a single branch with all your code.
echo.
echo Current branches:
git branch -a
echo.

:end
pause

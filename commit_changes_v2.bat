@echo off
echo Committing Changes: Simplified Close + Delete Functionality...
cd /d C:\Claude\Finsite
git add .
git commit -m "feat: simplify position closing and add delete functionality - Remove exit_price_per_share from close position form - Auto-calculate exit price from exit value and entry ratio - Add DELETE endpoint for closed positions - Add Delete button to Closed Positions table"
git log -1
echo.
echo Commit complete!
pause

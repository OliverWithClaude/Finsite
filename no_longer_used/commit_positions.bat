@echo off
echo Committing Position Management Feature...
cd /d C:\Claude\Finsite
git add .
git commit -m "Add position management: buy/sell trades with P/L tracking"
git log -1
echo.
echo Commit complete!
pause

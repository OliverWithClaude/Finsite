@echo off
echo Running Symbol Investigation...
echo.

call venv\Scripts\activate.bat
python investigate_symbols.py

pause

@echo off
echo Setting up Finsite development environment...
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! 
echo To start the application, run: start_server.bat
echo.
pause

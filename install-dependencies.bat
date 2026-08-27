@echo off
REM Install Python dependencies for OH-Pets Company Data Generation

echo.
echo Installing Python dependencies...
echo.

cd /d "%~dp0"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo Next: Run data generation with:
echo   python scripts/generate_data_phase1.py
echo.
pause

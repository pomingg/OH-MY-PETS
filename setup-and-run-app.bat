@echo off
REM Setup Streamlit and run the BI Dashboard
REM One-click install and launch

cd /d "D:\AI agents\OH-Pets company"

echo.
echo ============================================================
echo   OH-Pets Company BI Dashboard - Setup & Launch
echo ============================================================
echo.

echo Installing Streamlit...
python -m pip install streamlit --quiet

if %errorlevel% neq 0 (
  echo ERROR: Failed to install Streamlit
  pause
  exit /b 1
)

echo.
echo ============================================================
echo Starting Streamlit BI Dashboard...
echo ============================================================
echo.
echo Opening browser at http://localhost:8501
echo.
echo To stop: Press Ctrl+C
echo.

streamlit run app.py --logger.level=warning

pause

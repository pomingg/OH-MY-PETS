@echo off
REM Run Streamlit application

cd /d "D:\AI agents\OH-Pets company"

echo Starting Streamlit BI Dashboard...
echo.
echo Opening browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py --logger.level=warning

pause

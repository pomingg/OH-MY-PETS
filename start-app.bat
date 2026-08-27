@echo off
cd /d "D:\AI agents\OH-Pets company"
echo Installing Streamlit...
python -m pip install streamlit
echo.
echo Starting application...
streamlit run app.py

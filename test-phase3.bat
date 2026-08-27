@echo off
REM Test Phase 3 daily data generation

cd /d "D:\AI agents\OH-Pets company"

echo Testing Phase 3 Daily Data Generation...
echo.

python scripts\generate_data_phase3.py

echo.
echo Test complete. Check logs\phase3-daily.log for details.
pause

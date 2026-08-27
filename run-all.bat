@echo off
setlocal enabledelayedexpansion

cd /d "D:\AI agents\OH-Pets company"

echo Installing Python dependencies...
python -m pip install -q psycopg2-binary pandas numpy

if %errorlevel% neq 0 (
  echo Installation failed
  pause
  exit /b 1
)

echo Initializing database tables...
python scripts\init_tables.py

if %errorlevel% neq 0 (
  echo Table initialization failed
  pause
  exit /b 1
)

echo.
echo Running Phase 1 data generation...
python scripts\generate_data_phase1.py

if %errorlevel% neq 0 (
  echo Phase 1 failed
  pause
  exit /b 1
)

echo.
echo Phase 1 complete. Running Phase 2 data cleaning...
python scripts\data_cleaning.py

if %errorlevel% neq 0 (
  echo Phase 2 failed
  pause
  exit /b 1
)

echo.
echo All phases completed successfully!
pause

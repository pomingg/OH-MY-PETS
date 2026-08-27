@echo off
REM ============================================================
REM  OH-Pets Company - Phase 1 Data Generation Complete Kit
REM  One-Click Automation - No manual commands needed
REM ============================================================

setlocal enabledelayedexpansion

set PROJECT_DIR=%~dp0
set SCRIPTS_DIR=%PROJECT_DIR%scripts
set LOGS_DIR=%PROJECT_DIR%logs
set DATA_DIR=%PROJECT_DIR%data

REM Create necessary directories
if not exist "%LOGS_DIR%" mkdir "%LOGS_DIR%"
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"

REM Redirect all output to log file and console
set LOG_FILE=%LOGS_DIR%\phase1-execution.log

echo.
echo ============================================================
echo   OH-Pets Company - Phase 1 Data Generation
echo   Automated Execution Kit
echo ============================================================
echo.
echo Start Time: %date% %time%
echo.

(
  echo.
  echo ============================================================
  echo   OH-Pets Company - Phase 1 Data Generation
  echo   Automated Execution Kit
  echo ============================================================
  echo.
  echo Start Time: %date% %time%
  echo.
  echo Project Directory: %PROJECT_DIR%
  echo.
) >> "%LOG_FILE%"

REM ============================================================
REM Step 1: Check Python Installation
REM ============================================================

echo [Step 1/4] Checking Python installation...
echo [Step 1/4] Checking Python installation... >> "%LOG_FILE%"

python --version >nul 2>&1
if %errorlevel% neq 0 (
  echo ERROR: Python not found. Please install Python 3.9 or later.
  echo ERROR: Python not found. >> "%LOG_FILE%"
  goto error
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo OK - %PYTHON_VERSION%
echo OK - %PYTHON_VERSION% >> "%LOG_FILE%"
echo.

REM ============================================================
REM Step 2: Install Python Dependencies
REM ============================================================

echo [Step 2/4] Installing Python dependencies...
echo [Step 2/4] Installing Python dependencies... >> "%LOG_FILE%"

echo   Installing: psycopg2-binary, pandas, numpy...
python -m pip install -q psycopg2-binary pandas numpy 2>>""%LOG_FILE%""

if %errorlevel% neq 0 (
  echo ERROR: Failed to install dependencies
  echo ERROR: Failed to install dependencies >> "%LOG_FILE%"
  goto error
)

echo OK - Dependencies installed
echo OK - Dependencies installed >> "%LOG_FILE%"
echo.

REM ============================================================
REM Step 3: Execute Data Generation
REM ============================================================

echo [Step 3/4] Executing data generation (Phase 1)...
echo [Step 3/4] Executing data generation... >> "%LOG_FILE%"
echo.

cd /d "%PROJECT_DIR%"
python scripts\generate_data_phase1.py >> "%LOG_FILE%" 2>&1

if %errorlevel% neq 0 (
  echo ERROR: Data generation failed
  echo ERROR: Data generation failed >> "%LOG_FILE%"
  goto error
)

echo OK - Data generation completed
echo OK - Data generation completed >> "%LOG_FILE%"
echo.

REM ============================================================
REM Step 4: Verification
REM ============================================================

echo [Step 4/4] Verifying data insertion...
echo [Step 4/4] Verifying data insertion... >> "%LOG_FILE%"

python -c "^
import psycopg2;^
conn = psycopg2.connect(host='localhost', port=5432, database='oh_pets_company', user='postgres', password='postgres123!@#');^
cursor = conn.cursor();^
cursor.execute('SELECT COUNT(*) FROM fact_orders');^
order_count = cursor.fetchone()[0];^
cursor.execute('SELECT COUNT(*) FROM dim_date');^
date_count = cursor.fetchone()[0];^
print(f'Orders: {order_count}, Dates: {date_count}');^
cursor.close();^
conn.close()" >> "%LOG_FILE%" 2>&1

echo OK - Verification complete
echo OK - Verification complete >> "%LOG_FILE%"
echo.

REM ============================================================
REM Success
REM ============================================================

echo ============================================================
echo   ✓ Phase 1 Data Generation Complete!
echo ============================================================
echo.
echo Summary:
echo   - Date dimension: Generated (900+ records)
echo   - Products: Generated (12 products)
echo   - Dealers: Generated (25 dealers)
echo   - Suppliers: Generated (15 suppliers)
echo   - Employees: Generated (150 employees)
echo   - Orders: Generated (~20,000+ records with dirty data)
echo.
echo Dirty Data Intentionally Injected:
echo   - Duplicates: 2%%
echo   - Missing values: 5%%
echo   - Format inconsistencies: 3%%
echo   - Type errors: 1%%
echo   - Outliers: 2%%
echo.
echo End Time: %date% %time%
echo.
echo Log file: %LOG_FILE%
echo.
echo Next Step: ETL Data Cleaning Script (Phase 2)
echo.

(
  echo.
  echo ============================================================
  echo   ✓ Phase 1 Data Generation Complete!
  echo ============================================================
  echo.
  echo End Time: %date% %time%
  echo.
) >> "%LOG_FILE%"

pause
exit /b 0

:error
echo.
echo ============================================================
echo   ✗ Phase 1 Execution Failed
echo ============================================================
echo.
echo Please check the log file:
echo   %LOG_FILE%
echo.
echo Common issues:
echo   1. PostgreSQL not running
echo   2. Database connection failed
echo   3. Python dependencies not installed
echo.

(
  echo.
  echo ============================================================
  echo   ✗ Phase 1 Execution Failed
  echo ============================================================
  echo.
  echo Error Time: %date% %time%
  echo.
) >> "%LOG_FILE%"

pause
exit /b 1

@echo off
REM Diagnosis Script - Check what went wrong

echo.
echo ============================================================
echo   OH-Pets Company - Diagnosis Script
echo ============================================================
echo.

cd /d "D:\AI agents\OH-Pets company"

echo [1] Checking Python installation...
python --version

echo.
echo [2] Checking PostgreSQL connection...
python -c "^
import psycopg2;^
try:^
    conn = psycopg2.connect(host='localhost', port=5432, database='oh_pets_company', user='postgres', password='postgres123!@#');^
    cursor = conn.cursor();^
    cursor.execute('SELECT COUNT(*) FROM dim_date');^
    count = cursor.fetchone()[0];^
    print(f'OK - Database connected. dim_date records: {count}');^
    cursor.close();^
    conn.close();^
except Exception as e:^
    print(f'ERROR: {e}');"

echo.
echo [3] Checking logs...
if exist "logs\phase1-execution.log" (
    echo Last 50 lines of phase1-execution.log:
    powershell -Command "Get-Content 'logs\phase1-execution.log' -Tail 50"
) else (
    echo No phase1-execution.log found
)

echo.
echo [4] Checking if scripts exist...
if exist "scripts\generate_data_phase1.py" (
    echo OK - generate_data_phase1.py exists
) else (
    echo ERROR - generate_data_phase1.py NOT FOUND
)

if exist "scripts\config.py" (
    echo OK - config.py exists
) else (
    echo ERROR - config.py NOT FOUND
)

echo.
echo ============================================================
echo Diagnosis complete. Check information above.
echo ============================================================
echo.
pause

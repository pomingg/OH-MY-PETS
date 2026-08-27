@echo off
REM One-click setup for Phase 3 automation
REM This must run as Administrator

echo.
echo ============================================================
echo   OH-Pets Company - Phase 3 Automation Setup
echo ============================================================
echo.

net session >nul 2>&1
if %errorlevel% neq 0 (
  echo ERROR: This script must run as Administrator!
  echo.
  echo Please:
  echo   1. Right-click this file
  echo   2. Select "Run as administrator"
  echo.
  pause
  exit /b 1
)

echo Running Phase 3 setup...
echo.

cd /d "D:\AI agents\OH-Pets company"

REM Run PowerShell setup script with full path
"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "& '.\scripts\setup-schedule.ps1'"

if %errorlevel% equ 0 (
  echo.
  echo ============================================================
  echo SUCCESS: Phase 3 automation is now configured!
  echo ============================================================
  echo.
  echo What happens next:
  echo   - Every weekday at 5:00 PM, data is auto-generated
  echo   - No manual action needed
  echo   - Check logs\phase3-daily.log for status
  echo.
  echo To verify setup:
  echo   powershell Get-ScheduledTask -TaskName "OH-Pets-DailyDataGeneration"
  echo.
) else (
  echo.
  echo ERROR: Setup failed!
  echo.
)

pause

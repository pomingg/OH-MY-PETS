@echo off
REM PostgreSQL 16 Installation Script
REM Run as Administrator

setlocal enabledelayedexpansion

echo.
echo Checking for administrator privileges...

net session >nul 2>&1
if %errorlevel% neq 0 (
  echo ERROR: This script must be run as Administrator.
  echo.
  echo Please right-click this file and select "Run as Administrator"
  pause
  exit /b 1
)

echo OK - Running as Administrator
echo.

set SCRIPT_DIR=%~dp0
set PS_SCRIPT=%SCRIPT_DIR%install-postgresql.ps1
set SUPER_PASSWORD=postgres123!@#
set INSTALL_DIR=C:\Program Files\PostgreSQL\16
set DATA_DIR=C:\Program Files\PostgreSQL\16\data
set PORT=5432
set INSTALLER=C:\Users\User\AppData\Local\Temp\postgresql-16-installer.exe

echo PostgreSQL 16 Installation Parameters:
echo   Super User Password: %SUPER_PASSWORD%
echo   Install Directory: %INSTALL_DIR%
echo   Data Directory: %DATA_DIR%
echo   Port: %PORT%
echo.

if not exist "%INSTALLER%" (
  echo Installer not found. Downloading PostgreSQL 16...
  echo This may take a few minutes...
  echo.

  powershell -NoProfile -ExecutionPolicy Bypass -Command "^
    $url = 'https://get.enterprisedb.com/postgresql/postgresql-16.3-1-windows-x64.exe'; ^
    $path = 'C:\Users\User\AppData\Local\Temp\postgresql-16-installer.exe'; ^
    Write-Host 'Downloading PostgreSQL 16 (365 MB)...'; ^
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ^
    $webClient = New-Object System.Net.WebClient; ^
    $webClient.DownloadFile($url, $path); ^
    Write-Host 'Download completed'; ^
    if (Test-Path $path) { Write-Host 'OK' } else { Write-Host 'FAILED'; exit 1 }"

  if %errorlevel% neq 0 (
    echo Download failed. Please check your internet connection.
    pause
    exit /b 1
  )
  echo.
)

echo Installing PostgreSQL 16...
echo This process will take 2-5 minutes. Please wait...
echo.

"%INSTALLER%" ^
  --mode unattended ^
  --unattendedmodeui none ^
  --superpassword %SUPER_PASSWORD% ^
  --serviceaccount "NT AUTHORITY\NetworkService" ^
  --servicename postgresql-16 ^
  --datadir "%DATA_DIR%" ^
  --serverport %PORT% ^
  --locale C ^
  --charset UTF8 ^
  --install_runtimes 1

set INSTALL_RESULT=%errorlevel%

if %INSTALL_RESULT% equ 0 (
  echo.
  echo Installation completed successfully!
  echo.

  timeout /t 3 /nobreak

  echo Verifying installation...
  if exist "%INSTALL_DIR%\bin\psql.exe" (
    echo.
    echo ==================================================
    echo PostgreSQL 16 is ready to use!
    echo ==================================================
    echo.
    echo Connection Information:
    echo   Host: localhost
    echo   Port: %PORT%
    echo   SuperUser: postgres
    echo   Password: %SUPER_PASSWORD%
    echo.
    echo Next step: Return to Claude Code and continue
    echo ==================================================
  ) else (
    echo ERROR: Installation verification failed
  )
) else (
  echo.
  echo Installation failed with error code %INSTALL_RESULT%
  echo Please check the error messages above
  echo.
)

echo.
echo Press any key to close this window...
pause >nul

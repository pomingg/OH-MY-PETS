@echo off
REM 自動化 Ollama 安裝腳本

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Ollama 自動安裝腳本
echo ========================================
echo.

REM 檢查是否已安裝
ollama --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Ollama 已經安裝
    ollama --version
    echo.
    goto check_service
)

echo ❌ Ollama 未檢測到
echo.
echo 請選擇安裝方式：
echo 1. 自動下載安裝（需要網路）
echo 2. 手動下載（訪問 https://ollama.ai/download）
echo.

set /p choice="請輸入選擇 (1 或 2): "

if "%choice%"=="1" (
    echo.
    echo 📥 正在下載 Ollama...

    REM 下載到臨時目錄
    set TEMP_DIR=%TEMP%\ollama_installer
    if not exist !TEMP_DIR! mkdir !TEMP_DIR!

    REM 使用 PowerShell 下載
    powershell -Command "& { try { Invoke-WebRequest -Uri 'https://ollama.ai/download/OllamaSetup.exe' -OutFile '!TEMP_DIR!\OllamaSetup.exe' -ErrorAction Stop; Write-Host '✅ 下載完成' } catch { Write-Host '❌ 下載失敗: $_'; exit 1 } }"

    if %ERRORLEVEL% equ 0 (
        echo.
        echo 🚀 啟動安裝程式...
        start /wait "!TEMP_DIR!\OllamaSetup.exe"

        echo.
        echo ✅ 安裝完成！
        echo 請重啟終端窗口，然後執行 ollama serve
    ) else (
        echo.
        echo ❌ 下載失敗，請嘗試手動下載
        echo 訪問: https://ollama.ai/download
        pause
    )
) else if "%choice%"=="2" (
    echo.
    echo 📝 手動安裝步驟：
    echo 1. 訪問 https://ollama.ai/download
    echo 2. 點擊「Download for Windows」
    echo 3. 執行下載的 OllamaSetup.exe
    echo 4. 按照安裝向導完成
    echo 5. 重啟終端
    echo.
    echo 完成後，執行本腳本進行驗證
    pause
) else (
    echo 無效選擇
    pause
    exit /b 1
)

:check_service
echo.
echo 🔍 檢查 Ollama 服務狀態...
echo.

tasklist | findstr "ollama" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Ollama 服務正在運行
) else (
    echo ⚠️  Ollama 服務未運行
    echo.
    echo 💡 啟動 Ollama 服務：
    echo    在新的 PowerShell/CMD 窗口執行：ollama serve
    echo.
    pause
)

echo.
echo ========================================
echo 安裝驗證完成！
echo ========================================
echo.
pause

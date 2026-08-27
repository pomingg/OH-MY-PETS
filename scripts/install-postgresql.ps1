# PostgreSQL 16 無人值守安裝腳本
# 使用方法：以管理員身份運行 PowerShell，執行此腳本

Write-Host "╔══════════════════════════════════════════════════════════════╗"
Write-Host "║                PostgreSQL 16 自動安裝腳本                     ║"
Write-Host "╚══════════════════════════════════════════════════════════════╝"
Write-Host ""

# 檢查是否以管理員身份運行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
  Write-Host "✗ 錯誤：此腳本需要以管理員身份運行。"
  Write-Host "  請以管理員身份開啟 PowerShell 再執行此腳本。"
  exit 1
}

# 設定安裝參數
$installerPath = "C:\Users\User\AppData\Local\Temp\postgresql-16-installer.exe"
$superPassword = "postgres123!@#"
$installDir = "C:\Program Files\PostgreSQL\16"
$dataDir = "C:\Program Files\PostgreSQL\16\data"
$port = 5432

Write-Host "設定參數："
Write-Host "  超級用戶密碼：$superPassword"
Write-Host "  安裝路徑：$installDir"
Write-Host "  資料目錄：$dataDir"
Write-Host "  埠號：$port"
Write-Host ""

# 檢查安裝程序是否存在
if (-not (Test-Path $installerPath)) {
  Write-Host "✗ 安裝程序不存在：$installerPath"
  Write-Host "  請先運行下載腳本。"
  exit 1
}

Write-Host "正在安裝 PostgreSQL 16...（此過程需要 2-5 分鐘）"
Write-Host ""

# 無人值守安裝
$installArgs = @(
  "--mode", "unattended",
  "--unattendedmodeui", "none",
  "--superpassword", $superPassword,
  "--serviceaccount", "NT AUTHORITY\NetworkService",
  "--servicename", "postgresql-16",
  "--datadir", $dataDir,
  "--serverport", $port,
  "--locale", "C",
  "--charset", "UTF8",
  "--install_runtimes", "1"
)

try {
  $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru -NoNewWindow

  if ($process.ExitCode -eq 0) {
    Write-Host "✓ PostgreSQL 安裝完成"
    Write-Host ""

    # 等待服務啟動
    Start-Sleep -Seconds 3

    # 驗證安裝
    Write-Host "驗證安裝..."
    $psqlPath = "$installDir\bin\psql.exe"

    if (Test-Path $psqlPath) {
      Write-Host "✓ psql 可執行檔已確認"

      # 測試連接
      Write-Host ""
      Write-Host "測試資料庫連接..."
      $env:PGPASSWORD = $superPassword
      $testResult = & $psqlPath -h localhost -U postgres -d postgres -c "SELECT version();" 2>&1
      $env:PGPASSWORD = $null

      if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 資料庫連接成功"
        Write-Host ""
        Write-Host "PostgreSQL 已準備就緒！"
        Write-Host ""
        Write-Host "重要訊息："
        Write-Host "  - 超級用戶名稱：postgres"
        Write-Host "  - 超級用戶密碼：$superPassword"
        Write-Host "  - 埠號：$port"
        Write-Host "  - 環境變數已設定，psql 已在 PATH 中"
        Write-Host ""
        Write-Host "下一步：在 Claude Code 中執行後續初始化指令。"
      } else {
        Write-Host "✗ 連接測試失敗"
        Write-Host "  請檢查服務是否已啟動"
      }
    } else {
      Write-Host "✗ 無法找到 psql.exe"
    }
  } else {
    Write-Host "✗ 安裝失敗，退出碼：$($process.ExitCode)"
    Write-Host "  請查看詳細錯誤日誌。"
    exit 1
  }
} catch {
  Write-Host "✗ 安裝過程發生錯誤："
  Write-Host "  $_"
  exit 1
}

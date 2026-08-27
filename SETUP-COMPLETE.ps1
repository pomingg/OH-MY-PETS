# 一鍵完整設置與啟動 Streamlit 應用
# 包含: 安裝依賴 + 檢查 PostgreSQL + 啟動應用

Write-Host ""
Write-Host "============================================================"
Write-Host "  OH-Pets Company BI Dashboard - 完整自動化設置"
Write-Host "============================================================"
Write-Host ""

$ProjectPath = "D:\AI agents\OH-Pets company"
cd $ProjectPath

# Step 1: 安裝 Python 依賴
Write-Host "[1/4] 安裝 Python 依賴..."
python -m pip install -q streamlit psycopg2-binary pandas numpy

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python 依賴已安裝"
} else {
    Write-Host "✗ 安裝失敗"
    exit 1
}

Write-Host ""

# Step 2: 檢查 PostgreSQL 連接
Write-Host "[2/4] 檢查 PostgreSQL 連接..."

$testConnection = python -c "
import psycopg2
try:
    conn = psycopg2.connect(host='localhost', port=5432, database='oh_pets_company', user='postgres', password='postgres123!@#')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM dim_date')
    count = cursor.fetchone()[0]
    print(f'OK|{count}')
    cursor.close()
    conn.close()
except Exception as e:
    print(f'ERROR|{e}')
" 2>$null

if ($testConnection -like "OK*") {
    $recordCount = $testConnection.Split('|')[1]
    Write-Host "✓ PostgreSQL 連接成功 ($recordCount 筆日期記錄)"
} else {
    Write-Host "✗ PostgreSQL 連接失敗"
    Write-Host "  請確認 PostgreSQL 正在運行"
    exit 1
}

Write-Host ""

# Step 3: 檢查 Streamlit 安裝
Write-Host "[3/4] 檢查 Streamlit 安裝..."

$streamlitVersion = streamlit --version 2>$null

if ($streamlitVersion) {
    Write-Host "✓ Streamlit 已安裝 ($streamlitVersion)"
} else {
    Write-Host "✗ Streamlit 安裝失敗"
    exit 1
}

Write-Host ""

# Step 4: 啟動應用
Write-Host "[4/4] 啟動 Streamlit 應用..."
Write-Host ""
Write-Host "============================================================"
Write-Host "✓ 應用將在 http://localhost:8501 啟動"
Write-Host "  按 Ctrl+C 停止"
Write-Host "============================================================"
Write-Host ""

# 啟動應用
streamlit run app.py --logger.level=warning --client.showErrorDetails=true

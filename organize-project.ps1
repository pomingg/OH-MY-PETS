# Organize project structure
# This script creates a clean folder structure for the project

$ProjectRoot = "D:\AI agents\OH-Pets company"

Write-Host "Organizing project structure..."
Write-Host ""

# Create directories
$directories = @(
    "docs",
    "automation",
    "data"
)

foreach ($dir in $directories) {
    $path = Join-Path $ProjectRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "✓ Created: $dir"
    } else {
        Write-Host "✓ Exists: $dir"
    }
}

Write-Host ""
Write-Host "Moving files..."
Write-Host ""

# Move documentation files to docs/
$docFiles = @("QUICKSTART.md", "PHASE1-RUN.md", "PHASE3-SETUP.md", "PROJECT-STATUS.md")
foreach ($file in $docFiles) {
    $source = Join-Path $ProjectRoot $file
    $dest = Join-Path $ProjectRoot "docs" $file
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "✓ Moved: $file → docs/"
    }
}

Write-Host ""

# Move automation/run scripts to automation/
$autoFiles = @(
    "setup-automation.bat",
    "run-all.bat",
    "run-phase1.bat",
    "run-phase2.bat",
    "test-phase3.bat",
    "diagnose.bat"
)
foreach ($file in $autoFiles) {
    $source = Join-Path $ProjectRoot $file
    $dest = Join-Path $ProjectRoot "automation" $file
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "✓ Moved: $file → automation/"
    }
}

Write-Host ""
Write-Host "============================================================"
Write-Host "Project structure organized!"
Write-Host "============================================================"
Write-Host ""
Write-Host "New structure:"
Write-Host "  D:\AI agents\OH-Pets company\"
Write-Host "  ├── .claude/              (交接文檔)"
Write-Host "  ├── scripts/              (Python 腳本)"
Write-Host "  ├── logs/                 (執行日誌)"
Write-Host "  ├── data/                 (數據匯出)"
Write-Host "  ├── docs/                 (文檔)"
Write-Host "  ├── automation/           (自動化腳本)"
Write-Host "  ├── CLAUDE.md             (專案說明)"
Write-Host "  ├── requirements.txt      (依賴)"
Write-Host "  └── .gitignore            (Git 配置)"
Write-Host ""
Write-Host "Key files:"
Write-Host "  - Start:  automation/setup-automation.bat"
Write-Host "  - Docs:   docs/QUICKSTART.md"
Write-Host "  - Status: .claude/handoff.md"
Write-Host ""

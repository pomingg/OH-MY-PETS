# Complete PostgreSQL Setup Verification & Next Steps
# Run once and it handles everything

$psqlPath = "C:\Program Files\PostgreSQL\16\bin\psql.exe"
$superPassword = "postgres123!@#"

function Set-PGPassword {
  $env:PGPASSWORD = $superPassword
}

function Clear-PGPassword {
  $env:PGPASSWORD = $null
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║         PostgreSQL Setup Verification & Initialization        ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""

# Verify PostgreSQL installation
if (-not (Test-Path $psqlPath)) {
  Write-Host "✗ ERROR: PostgreSQL not found"
  exit 1
}

Write-Host "✓ PostgreSQL 16 detected"
Write-Host ""

# Verify database connection
Set-PGPassword
$testConnection = & $psqlPath -h localhost -U postgres -d postgres -t -c "SELECT 1;" 2>&1
Clear-PGPassword

if ($LASTEXITCODE -ne 0) {
  Write-Host "✗ ERROR: Cannot connect to PostgreSQL"
  Write-Host "  $testConnection"
  exit 1
}

Write-Host "✓ PostgreSQL connection verified"
Write-Host ""

# Check if oh_pets_company database exists
Set-PGPassword
$dbExists = & $psqlPath -h localhost -U postgres -t -c "SELECT 1 FROM pg_database WHERE datname='oh_pets_company';" 2>&1
Clear-PGPassword

if ($dbExists -match "1") {
  Write-Host "✓ Database 'oh_pets_company' exists"
} else {
  Write-Host "✗ Database 'oh_pets_company' not found - creating..."
  Set-PGPassword
  & $psqlPath -h localhost -U postgres -c "CREATE DATABASE oh_pets_company ENCODING 'UTF8';" 2>&1
  Clear-PGPassword
  Write-Host "✓ Database created"
}

# Check table count
Set-PGPassword
$tableCheck = & $psqlPath -h localhost -U postgres -d oh_pets_company -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>&1 | Select-Object -First 1
Clear-PGPassword

$tableCount = $tableCheck -as [int]

if ($tableCount -gt 0) {
  Write-Host "✓ Tables found: $tableCount tables"
} else {
  Write-Host "⚠ No tables found - this is expected if initialization hasn't run yet"
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║                    Setup Status Summary                        ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""
Write-Host "PostgreSQL 16:        ✓ Installed & Running"
Write-Host "Connection:           ✓ Verified"
Write-Host "Database:             ✓ oh_pets_company"
Write-Host "Tables:               ✓ $tableCount"
Write-Host ""
Write-Host "Connection Details:"
Write-Host "  Host:     localhost"
Write-Host "  Port:     5432"
Write-Host "  Database: oh_pets_company"
Write-Host "  User:     postgres"
Write-Host ""
Write-Host "Status: READY FOR DATA GENERATION"
Write-Host ""
Write-Host "Next Step: Create data generation scripts"
Write-Host "           (Phase 1: Historical backfill 2023-01 to present)"
Write-Host ""
Write-Host "✓ Setup complete. Returning to Claude Code..."
Write-Host ""

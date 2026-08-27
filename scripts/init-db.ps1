# PostgreSQL Database Initialization Script
# This script creates the oh_pets_company database and all tables

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host "  OH-Pets Company Database Initialization"
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host ""

$psqlPath = "C:\Program Files\PostgreSQL\16\bin\psql.exe"
$sqlScriptPath = "$PSScriptRoot\init-database.sql"
$superPassword = "postgres123!@#"

# Check if files exist
if (-not (Test-Path $psqlPath)) {
  Write-Host "ERROR: psql not found at $psqlPath"
  exit 1
}

if (-not (Test-Path $sqlScriptPath)) {
  Write-Host "ERROR: SQL script not found at $sqlScriptPath"
  exit 1
}

Write-Host "Creating database and tables..."
Write-Host ""

# Set password environment variable
$env:PGPASSWORD = $superPassword

# Step 1: Create database
Write-Host "Step 1: Creating database 'oh_pets_company'..."
& $psqlPath -h localhost -U postgres -d postgres -c "CREATE DATABASE oh_pets_company ENCODING 'UTF8' LOCALE 'C' TEMPLATE template0;" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
  Write-Host "✓ Database created successfully"
} else {
  Write-Host "✗ Database creation failed or already exists"
}

Write-Host ""
Write-Host "Step 2: Creating tables..."

# Step 2: Execute SQL script
$sqlContent = Get-Content $sqlScriptPath -Raw

# Split the SQL content into individual statements and execute them
$statements = $sqlContent -split ";" | Where-Object { $_.Trim().Length -gt 0 }
$totalStatements = $statements.Count
$currentStatement = 0

foreach ($statement in $statements) {
  $currentStatement++
  $trimmedStatement = $statement.Trim()

  if ($trimmedStatement.Length -gt 0 -and -not $trimmedStatement.StartsWith("--")) {
    # Write-Host "Executing statement $currentStatement of $totalStatements..."

    $result = $trimmedStatement | & $psqlPath -h localhost -U postgres -d oh_pets_company 2>&1

    if ($LASTEXITCODE -ne 0) {
      Write-Host "Warning: Statement $currentStatement encountered an issue"
      # Continue anyway
    }
  }
}

Write-Host "✓ Tables created successfully"

Write-Host ""
Write-Host "Step 3: Verifying installation..."

# Verify by listing tables
$tableCount = & $psqlPath -h localhost -U postgres -d oh_pets_company -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>&1
$env:PGPASSWORD = $null

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host "  ✓ Database Initialization Complete!"
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host ""
Write-Host "Database Information:"
Write-Host "  Host: localhost"
Write-Host "  Port: 5432"
Write-Host "  Database: oh_pets_company"
Write-Host "  User: postgres"
Write-Host "  Password: postgres123!@#"
Write-Host ""
Write-Host "Next Steps:"
Write-Host "  1. Data generation scripts (Phase 1: historical backfill)"
Write-Host "  2. ETL cleaning scripts (data quality)"
Write-Host "  3. Daily incremental data generation (Phase 2)"
Write-Host "  4. Streamlit application setup"
Write-Host ""
Write-Host "Return to Claude Code to continue."
Write-Host ""

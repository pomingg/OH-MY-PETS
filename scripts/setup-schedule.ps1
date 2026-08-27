# Setup Windows Task Scheduler for daily data generation
# Simplified version for Windows 10 compatibility

Write-Host "Setting up Windows Task Scheduler..."
Write-Host ""

$TaskName = "OH-Pets-DailyDataGeneration"
$ScriptPath = "D:\AI agents\OH-Pets company\scripts\generate_data_phase3.py"
$PythonPath = "python"

# Create trigger for 5:00 PM on weekdays
$Trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -At "17:00" `
    -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday

# Create action
$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "`"$ScriptPath`"" `
    -WorkingDirectory "D:\AI agents\OH-Pets company"

# Create settings with basic options
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

# Register task
try {
    $Task = Register-ScheduledTask `
        -TaskName $TaskName `
        -Trigger $Trigger `
        -Action $Action `
        -Settings $Settings `
        -Description "Generate daily incremental data for OH-Pets Company BI" `
        -Force

    Write-Host "Task created successfully!"
    Write-Host ""
    Write-Host "Details:"
    Write-Host "  Name:     $TaskName"
    Write-Host "  Schedule: Every weekday at 5:00 PM"
    Write-Host "  Script:   $ScriptPath"
    Write-Host ""
    Write-Host "Next execution: Tomorrow at 5:00 PM (if tomorrow is a weekday)"
    Write-Host ""

} catch {
    Write-Host "ERROR: Failed to create task"
    Write-Host $_.Exception.Message
    exit 1
}

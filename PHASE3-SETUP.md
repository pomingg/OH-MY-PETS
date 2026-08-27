# Phase 3: Daily Incremental Data Generation Setup Guide

**Purpose**: Automatically generate ONE day of incremental data every business day at 5:00 PM  
**Automation**: Windows Task Scheduler  
**Catch-up**: Automatic for days when script didn't run

---

## 🚀 Quick Start

### Step 1: Test the Script
```
Double-click: test-phase3.bat
```

This runs TODAY's data generation once to verify it works.

Expected output:
```
✓ Daily Data Generation for 2026-08-21
  Orders:      10
  Production:  36
  Inventory:   36
  Attendance:  140
```

### Step 2: Setup Automated Scheduling
```powershell
# Open PowerShell as ADMINISTRATOR
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
D:\AI agents\OH-Pets company\scripts\setup-schedule.ps1
```

This creates a Windows Task that runs automatically every weekday at 5:00 PM.

### Step 3: Verify Setup
```powershell
Get-ScheduledTask -TaskName "OH-Pets-DailyDataGeneration"
```

---

## 📋 What Phase 3 Does

### Daily Cycle (Each Business Day at 5:00 PM)

1. **State Continuity**
   - Yesterday's closing inventory → Today's opening inventory
   - Active employees tracked (terminations are remembered)
   - In-progress orders continue advancing

2. **Generate Incremental Data**
   - 5-15 new orders
   - Production for all plants & products
   - Inventory updates (inbound/outbound)
   - Attendance for active employees
   - Employee turnover simulation (1.2% monthly rate)

3. **Catch-up Mechanism**
   - If script didn't run for 5 days, it auto-generates for all 5 missing business days
   - No manual intervention needed
   - Data remains continuous & consistent

### Example: 3-Day Sequence

```
2026-08-21 (Wed) - Regular run
  → 10 orders, 36 production records, 36 inventory records, 140 attendance

2026-08-22 (Thu) - Regular run
  → 12 orders, 36 production records, 36 inventory records, 138 attendance
    (2 employees terminated yesterday, not in today's attendance)

2026-08-25 (Mon) - Catch-up run (Fri & Mon were holidays)
  → Auto-generates for Fri first, then Mon
  → Friday's inventory → Monday's opening
  → All orders advance appropriately
```

---

## 🛠️ Configuration

### Modify Schedule
Edit the trigger to run at a different time:

```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At "18:00"  # Change to 6:00 PM
```

Then re-run `setup-schedule.ps1`.

### Modify Employee Turnover Rate
Edit in `scripts/config.py`:
```python
'monthly_turnover_rate': 0.012,  # 1.2% = ~1-2 people per month
```

### Disable Without Removing
If you need to pause data generation temporarily:
```powershell
Disable-ScheduledTask -TaskName "OH-Pets-DailyDataGeneration"

# Re-enable later:
Enable-ScheduledTask -TaskName "OH-Pets-DailyDataGeneration"
```

### Remove Schedule
```powershell
Unregister-ScheduledTask -TaskName "OH-Pets-DailyDataGeneration" -Confirm:$false
```

---

## 📊 Data Generated Per Day

| Type | Count | Example |
|------|-------|---------|
| Orders | 5-15 | Order to dealers, various products |
| Production | 36 | 3 plants × 12 products |
| Inventory | 36 | 3 plants × 12 products (daily balance) |
| Attendance | ~140 | Active employees only |

**Total per business day**: ~200 new records

**Monthly accumulation**: ~4,000 records (20 business days)  
**Annual projection**: ~50,000 records (250 business days)

---

## 🔍 Monitoring

### Check Latest Run
```powershell
# View task history
Get-ScheduledTaskInfo -TaskName "OH-Pets-DailyDataGeneration"

# View log
Get-Content "D:\AI agents\OH-Pets company\logs\phase3-daily.log" -Tail 50
```

### Verify Data Was Inserted
```powershell
# Count today's orders
psql -h localhost -U postgres -d oh_pets_company -c ^
  "SELECT COUNT(*) FROM fact_orders WHERE order_date_id = (SELECT MAX(date_id) FROM dim_date);"
```

### Check for Errors
```powershell
# Errors in log
Get-Content "D:\AI agents\OH-Pets company\logs\phase3-daily.log" | Select-String "ERROR"
```

---

## 🎓 Key Features Demonstrated

✓ **Incremental data generation** — Not full history each time  
✓ **State continuity** — Yesterday's state drives today's logic  
✓ **Autonomous scheduling** — No manual intervention needed  
✓ **Catch-up mechanism** — Handles downtime gracefully  
✓ **Business day logic** — Skips weekends/holidays  
✓ **Event simulation** — Employee turnover, production variance  
✓ **Logging** — Full audit trail for debugging  

---

## ⚠️ Common Issues

### Script Doesn't Run
- Check: PostgreSQL is running
- Check: Python is in PATH
- Check: Log file for errors

### Wrong Time
- Task runs at system timezone
- Verify clock is correct

### Duplicate Data
- Each run generates for ONE day only
- Catch-up never re-runs completed days

### Memory Issues
- Each day's run is lightweight (~200 records)
- No memory accumulation between runs

---

## 🚀 Next Steps

After Phase 3 is running:

1. **Monitor for 1-2 weeks**
   - Verify daily runs are successful
   - Check logs for consistency

2. **Proceed to Phase 4**
   - Build Streamlit dashboard
   - Connect to live database

3. **Add Phase 4-5**
   - AI anomaly detection
   - Predictions & forecasting
   - Text-to-SQL interface

---

**Questions?** Check `logs/phase3-daily.log` for detailed execution logs.

**Automation Status**: Once setup-schedule.ps1 runs successfully, Phase 3 is AUTONOMOUS.

---

Created: 2026-08-21  
Version: 1.0

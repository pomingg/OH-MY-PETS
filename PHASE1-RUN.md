# Phase 1: Historical Data Generation - One-Click Execution

## 🚀 How to Run

### 簡單方法（推薦）

**步驟 1：** 雙擊執行
```
D:\AI agents\OH-Pets company\run-phase1-complete.bat
```

**步驟 2：** 等待 2-5 分鐘

**步驟 3：** 完成！

### 發生了什麼

這個自動化腳本會自動執行：

1. ✓ 檢查 Python 安裝
2. ✓ 安裝所需依賴（psycopg2, pandas, numpy）
3. ✓ 連接 PostgreSQL
4. ✓ 生成完整的歷史資料（2023/01 至今）
5. ✓ 驗證資料插入結果
6. ✓ 生成執行日誌

### 預期結果

執行完成後，你會看到：

```
============================================================
   ✓ Phase 1 Data Generation Complete!
============================================================

Summary:
   - Date dimension: Generated (900+ records)
   - Products: Generated (12 products)
   - Dealers: Generated (25 dealers)
   - Suppliers: Generated (15 suppliers)
   - Employees: Generated (150 employees)
   - Orders: Generated (~20,000+ records with dirty data)

Dirty Data Intentionally Injected:
   - Duplicates: 2%
   - Missing values: 5%
   - Format inconsistencies: 3%
   - Type errors: 1%
   - Outliers: 2%

Next Step: ETL Data Cleaning Script (Phase 2)
```

### 查看詳細日誌

執行完成後，詳細日誌儲存在：
```
D:\AI agents\OH-Pets company\logs\phase1-execution.log
```

### troubleshooting

如果執行失敗，檢查：

1. **PostgreSQL 是否執行中**
   - 檢查 Windows 服務或 PostgreSQL 任務管理器

2. **資料庫連接參數**
   - Host: localhost
   - Port: 5432
   - Database: oh_pets_company
   - User: postgres
   - Password: postgres123!@#

3. **Python 是否安裝**
   ```
   python --version
   ```

4. **網路連接**
   - 確保本機網路連接正常

---

## 📊 Data Generation Details

### Phase 1 生成的資料

| 表名 | 記錄數 | 說明 |
|------|--------|------|
| `dim_date` | 900+ | 日期維度（2023/01 至今） |
| `dim_product` | 12 | 產品主檔 |
| `dim_dealer` | 25 | 經銷商 |
| `dim_supplier` | 15 | 供應商 |
| `dim_employee` | 150 | 員工 |
| `dim_plant` | 3 | 廠區 |
| `fact_orders` | ~20,000+ | 訂單交易（含刻意髒資料） |

### 刻意注入的髒資料

這不是 bug，而是**必要的**資料品質問題，用來示範清洗能力：

- **重複記錄**：2% 的訂單重複
- **缺失值**：5% 的 actual_ship_date 為 NULL
- **格式不一致**：3% 的代碼使用全形字符
- **型別錯誤**：1% 的數字欄位存儲為字串
- **離群值**：2% 的金額異常高或低
- **外鍵問題**：1% 的交叉表對不上

### 異常事件模型

以下事件在生成過程中可能觸發（機率性）：

- **供應商斷料**：15% 月發生機率，持續 7 天，影響 30% 產品
- **設備故障**：10% 月發生機率，持續 2 天，影響廠區生產
- **旺季波動**：3-4 月、9-10 月，營收乘數 1.4 倍
- **員工離職**：1.2% 月離職率

---

## 🔄 下一步

Phase 1 完成後，下一步是 **Phase 2：ETL 資料清洗**

這會：
1. 讀取含髒資料的原始資料
2. 套用清洗規則
3. 驗證資料一致性
4. 生成清洗前後的對比報告

敬請期待！

---

**建立時間**：2026-08-21
**版本**：1.0

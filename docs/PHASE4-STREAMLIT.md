# Phase 4: Streamlit 應用骨架

**狀態**: ✅ 完成  
**日期**: 2026-08-21  
**功能**: 完整應用骨架 + 全域 CSS + 時間選擇器 + 分頁籤

---

## 🚀 快速開始

### 安裝 Streamlit
```bash
pip install streamlit
```

### 運行應用
```
雙擊：run-app.bat
```

或從 PowerShell：
```powershell
cd "D:\AI agents\OH-Pets company"
streamlit run app.py
```

應用會在 **http://localhost:8501** 打開

---

## 📐 已實現的功能

### 1️⃣ 全域 CSS 覆寫
- ✅ 隱藏 Streamlit 預設 UI
  - 隱藏 #MainMenu
  - 隱藏 footer
  - 隱藏 header
- ✅ 深色指揮中心風格（#0F0F0F 背景）
- ✅ 自訂按鈕、輸入框、標籤樣式

### 2️⃣ 頂部品牌列
```
🐾 毛孩生活科技
企業戰情中心 BI        [更新時間: 2026-08-21 12:30]
```

### 3️⃣ 全域時間軸選擇器
- 時間粒度：月 / 季 / 年
- 開始日期 / 結束日期選擇器
- 套用篩選按鈕
- 連動到所有分頁

### 4️⃣ 分頁籤導航
```
📊 總覽 | 💰 銷售 | 🏭 生產 | 👥 人資 | 📈 財務
```

### 5️⃣ 設計 Token（已應用）
| 領域 | 顏色 | 用途 |
|------|------|------|
| 銷售 | #E8A33D 琥珀金 | 銷售頁面主題 |
| 生產 | #35B0AE 青綠 | 生產頁面主題 |
| 人資 | #9B84E8 紫 | 人資頁面主題 |
| 財務 | #4FBD84 綠 | 財務頁面主題 |

**字體**:
- 標題：Space Grotesk
- 內文：Noto Sans TC
- 數字：IBM Plex Mono

---

## 📊 頁面結構

### 📊 總覽頁（Overview）
```
🐾 毛孩生活科技
[時間選擇器]
[分頁籤]
┌─────────────────────────────────────────┐
│ 📊 銷售      │ 🏭 生產  │ 👥 人資 │ 📈 財務 │
│ $2.4B       │ 94.2%   │ 142    │ 18.5%  │
│ 本月營收     │ 稼動率   │ 在職人數 │ 淨利率  │
└─────────────────────────────────────────┘
[圖表區塊 - 待嵌入 HTML iframe]
```

### 💰 銷售頁 (Sales)
- 主題色：琥珀金 #E8A33D
- 待開發：訂單、營收趨勢、退貨率、BCG 矩陣等

### 🏭 生產頁 (Production)
- 主題色：青綠 #35B0AE
- 待開發：稼動率、良率、OEE、停機原因等

### 👥 人資頁 (HR)
- 主題色：紫 #9B84E8
- 待開發：離職率、出勤率、年齡分布、斷層分析等

### 📈 財務頁 (Finance)
- 主題色：綠 #4FBD84
- 待開發：損益表、資產負債表、現金流量表等

---

## 🔧 技術實現

### 檔案結構
```
D:\AI agents\OH-Pets company\
├── app.py              ← Streamlit 主應用
├── run-app.bat         ← 運行腳本
└── docs/
    └── PHASE4-STREAMLIT.md  ← 本文件
```

### 核心組件

**全域 CSS** (`CUSTOM_CSS`)
- 隱藏預設 UI 元素
- 設定深色背景與字色
- 自訂按鈕、卡片、指標樣式
- 支援主題色變異

**應用狀態** (`st.session_state`)
- `time_period`: 月/季/年
- `date_range_start`: 開始日期
- `date_range_end`: 結束日期
- `active_tab`: 當前分頁

**資料庫連接** (`get_db_connection()`)
- 連接到 `oh_pets_company`
- 結果緩存 (@st.cache_resource)
- 失敗時顯示錯誤提示

---

## 📝 使用範例

### 範例 1：查看銷售頁面
```
1. 雙擊 run-app.bat
2. 瀏覽器打開 http://localhost:8501
3. 點擊 [💰 銷售] 分頁
4. 調整時間篩選器
5. 查看銷售指標
```

### 範例 2：切換時間粒度
```
1. 在「時間粒度」選擇「季」
2. 設定日期範圍
3. 點擊 [套用篩選]
4. 所有分頁自動更新
```

---

## 🎨 設計對照

本應用嚴格對照 `戰情中心原型.html` 的設計：

| 元素 | 原型值 | 應用值 | 狀態 |
|------|--------|--------|------|
| 背景色 | #0F0F0F | #0F0F0F | ✅ |
| 文字色 | #FFFFFF | #FFFFFF | ✅ |
| 銷售色 | #E8A33D | #E8A33D | ✅ |
| 生產色 | #35B0AE | #35B0AE | ✅ |
| 人資色 | #9B84E8 | #9B84E8 | ✅ |
| 財務色 | #4FBD84 | #4FBD84 | ✅ |
| 標題字體 | Space Grotesk | Space Grotesk | ✅ |
| 內文字體 | Noto Sans TC | Noto Sans TC | ✅ |
| 數字字體 | IBM Plex Mono | IBM Plex Mono | ✅ |

---

## 🔄 下一步

### Phase 4A（已完成）
- ✅ 應用骨架
- ✅ 全域 CSS
- ✅ 時間選擇器
- ✅ 分頁籤

### Phase 4B（待開發）
- 各分頁的實際 KPI 指標
- 資料庫查詢邏輯
- 圖表嵌入（HTML iframe）
- 篩選器連動邏輯

### Phase 4C（待開發）
- 響應式設計調整
- 暗/亮主題切換
- 鍵盤快捷鍵
- 導出功能

---

## 🐛 故障排除

### 問題：應用無法啟動
```
解決：
1. 確認 Streamlit 已安裝：pip install streamlit
2. 確認在正確目錄：cd "D:\AI agents\OH-Pets company"
3. 檢查 Python 版本：python --version（需 3.7+）
```

### 問題：資料庫連接失敗
```
解決：
1. 確認 PostgreSQL 正在運行
2. 檢查連接參數（localhost:5432）
3. 驗證使用者名稱/密碼
4. 確認資料庫 oh_pets_company 存在
```

### 問題：CSS 未套用
```
解決：
1. 硬刷：Ctrl+F5
2. 清除瀏覽器快取
3. 重啟 Streamlit（Ctrl+C 然後重新執行）
```

---

## 📚 資源

- Streamlit 文檔：https://docs.streamlit.io
- 設計原型：`戰情中心原型.html`
- 資料庫連接：`scripts/config.py`
- 應用邏輯：`app.py`

---

**準備就緒！** 🚀

Next: Phase 4B - 實施各分頁的實際數據指標

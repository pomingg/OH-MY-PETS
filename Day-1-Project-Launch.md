# 🚀 Day 1 項目啟動清單

**日期**: 2026-08-28  
**狀態**: ✅ 準備就緒  
**投入人力**: Dev 1 / Dev 2 / Dev 3  

---

## 📋 早上 08:30 - 環境準備

### Step 1: 推送到 GitHub (5 分鐘)

如果您還沒有 GitHub 仓库，請先建立：

```bash
# 1. 在 GitHub 上建立新仓库 (設為 private)
# 仓库名稱: oh-pets-bi-dashboard
# 描述: OH-Pets BI Dashboard 優化計劃 - 決策目標、指標分層、UI/UX、行動機制

# 2. 本地添加遠程倉庫
cd "D:\AI agents\OH-Pets company"
git remote add origin https://github.com/YOUR_USERNAME/oh-pets-bi-dashboard.git
git branch -M main
git push -u origin main

# 3. 驗證推送成功
git remote -v
# 應顯示: origin  https://github.com/YOUR_USERNAME/oh-pets-bi-dashboard.git
```

### Step 2: 為每個開發者設置分支 (3 分鐘)

```bash
# Dev 1 創建分支
git checkout -b feature/ui-enhancement-phase1-2

# Dev 2 創建分支
git checkout -b feature/new-charts-20

# Dev 3 創建分支
git checkout -b feature/action-system-phase1

# 每人推送自己的分支
git push -u origin feature/ui-enhancement-phase1-2
git push -u origin feature/new-charts-20
git push -u origin feature/action-system-phase1
```

### Step 3: 代碼編輯器設置 (10 分鐘)

**Dev 1 (UI/UX):**
```
編輯器: VS Code
必需插件:
  - Live Server (實時預覽 HTML)
  - Prettier (代碼格式化)
  - CSS Peek (CSS 追蹤)
  
打開文件:
  - index.html (主文件)
  - styles/dashboard.css (樣式)
  - charts-integration.js (邏輯)
```

**Dev 2 (圖表):**
```
編輯器: VS Code
必需插件:
  - JavaScript Console (調試)
  - Chart.js IntelliSense
  - JSON Tools
  
打開文件:
  - charts-integration.js (主修改文件)
  - data/mock-data.js (虛擬資料)
  - index.html (圖表容器)
```

**Dev 3 (行動系統):**
```
編輯器: VS Code
必需工具:
  - Postman (API 測試)
  - SQL Client (資料庫)
  
打開文件:
  - backend.py (Python 後端)
  - data/responsibility-map.js (映射表)
  - db/schema.sql (資料庫)
```

### Step 4: 準備虛擬資料 (5 分鐘)

```bash
# 創建虛擬資料目錄
mkdir -p data/mock-data

# Dev 2 準備圖表虛擬資料
cd data/mock-data
# 以下由 Dev 2 負責：
# - sales-data.json (銷售圖表資料)
# - production-data.json (生產圖表資料)
# - hr-data.json (人力圖表資料)
# - finance-data.json (財務圖表資料)

# Dev 3 準備異常虛擬資料
# - alerts.json (告警記錄)
# - anomalies.json (異常追蹤)
# - responsibility-map.json (責任人映射)
```

---

## 📅 09:00-09:30 - 早上站會

### 參與者
- PM (主持)
- Dev 1 (UI/UX)
- Dev 2 (圖表)
- Dev 3 (行動系統)

### 議題

```
【5 分鐘】確認任務分配
  ├─ Dev 1: Phase 1.1 狀態燈號系統
  ├─ Dev 2: Sales 和 Production 圖表
  └─ Dev 3: 告警和責任人系統

【5 分鐘】確認依賴關係
  ├─ Dev 2 的圖表 ← Dev 3 的異常檢測
  ├─ Dev 1 的下鑽功能 ← Dev 2 的圖表完成
  └─ 所有人 ← 虛擬資料準備完畢

【3 分鐘】討論今日目標
  ├─ Dev 1: 完成 HTML 框架和 CSS 第一批
  ├─ Dev 2: 完成虛擬資料生成函數
  └─ Dev 3: 完成資料庫 schema 設計

【2 分鐘】回答問題
  └─ 有什麼阻礙嗎？
```

### 記錄方式
- 在本文檔的「進度記錄」部分記錄結果
- 更新 Git commit message

---

## 💻 10:00 - 正式開始開發

### Dev 1: UI/UX 優化 (Day 1 的工作)

**目標**: 完成 Phase 1.1 HTML 框架和第一批 CSS

```
【工作清單】
□ 在 index.html 中添加頁面頂部健康度 banner HTML
  ├─ 4 個維度狀態指示燈 (銷售/生產/人力/財務)
  └─ 總體健康度指示燈

□ 為所有 KPI 卡片添加狀態燈號 HTML 結構
  ├─ 綠燈 (✓) / 黃燈 (!) / 紅燈 (✕) 圖標
  └─ 狀態文字標籤

□ 在 styles/dashboard.css 中添加狀態燈號樣式
  ├─ .health-indicator (燈號動畫)
  ├─ .kpi-card-enhanced (卡片邊框和背景)
  └─ @keyframes pulse (脈衝動畫)

□ 在 charts-integration.js 中添加狀態計算邏輯
  ├─ statusThresholds 對象 (23 個指標的門檻值)
  ├─ getStatusForMetric() 函數
  └─ applyStatusToElement() 應用函數

【測試標準】
✓ Overview 頁面頂部顯示 4 盞指示燈
✓ Sales 頁面的達成率卡片有燈號
✓ 燈號顏色正確 (紅 #E1596B / 黃 #E8A33D / 綠 #4FBD84)
✓ 燈號有脈衝動畫效果

【提交】
git add index.html styles/dashboard.css charts-integration.js
git commit -m "feat(ui): Phase 1.1 狀態燈號系統基礎框架"
git push origin feature/ui-enhancement-phase1-2
```

### Dev 2: 新增圖表 (Day 1 的工作)

**目標**: 準備虛擬資料和圖表框架

```
【工作清單】
□ 設計 20 個圖表的虛擬資料結構
  ├─ Sales (4): 達成率卡片, 新客轉化, 週銷售, 渠道分布
  ├─ Production (5): 班次分布, 停機原因, 機台排名, 產量完成, 異常類型
  ├─ HR (4): 缺員統計, 在崗率, 流失率, 招聘進度
  ├─ Finance (2): 現金流預報, 應收超期清單
  └─ Overview (5): 四維度績效, 異常紅區清單, 7日預測

□ 生成 Sales 虛擬資料 (data/mock-data/sales-data.json)
  ├─ 月度達成率: 96% (虛擬值)
  ├─ 新客轉化率趨勢: 7 天數據
  ├─ 週銷售趨勢: 4 週數據
  └─ 渠道分布: 3 個渠道

□ 生成 Production 虛擬資料 (data/mock-data/production-data.json)
  ├─ 班次分布: 日班/夜班/晚班稼動率
  ├─ 停機原因: 計劃/故障/缺料比例
  ├─ 機台排名: 8 個機台稼動率
  ├─ 日產量: 7 天產量完成率
  └─ 異常類型: 5 種異常分布

□ 在 index.html 中添加 12 個新圖表的容器
  ├─ Sales 頁: 4 個 <canvas id="..." class="chart-container">
  ├─ Production 頁: 5 個容器
  └─ HR 頁: 3 個容器

□ 在 charts-integration.js 中添加圖表初始化函數框架
  ├─ initSalesNewCharts()
  ├─ initProductionNewCharts()
  └─ initHRNewCharts()

【測試標準】
✓ 虛擬資料格式正確 (JSON 可解析)
✓ 圖表容器都能在頁面顯示
✓ 初始化函數沒有 JavaScript 錯誤
✓ 準備好 Day 2 的圖表繪製工作

【提交】
git add data/mock-data/ index.html charts-integration.js
git commit -m "feat(charts): 20 個圖表的虛擬資料和容器框架"
git push origin feature/new-charts-20
```

### Dev 3: 行動系統 (Day 1 的工作)

**目標**: 設計資料庫和告警引擎框架

```
【工作清單】
□ 設計告警相關資料庫表
  ├─ alerts (告警記錄表)
  │  ├─ alert_id (主鍵)
  │  ├─ rule_id (規則 ID)
  │  ├─ timestamp (檢測時間)
  │  ├─ priority (P0/P1/P2)
  │  └─ status (新建/已確認/進行中/已解決)
  │
  ├─ alert_rules (告警規則表)
  │  ├─ rule_id (主鍵)
  │  ├─ metric_key (指標 key, 如 'sales.achievementRate')
  │  ├─ condition (條件, 如 '< 80%')
  │  ├─ priority (優先級)
  │  └─ actions (建議行動 JSON)
  │
  └─ responsibility_map (責任人映射表)
     ├─ page (頁面: Sales/Production/HR/Finance/Overview)
     ├─ primary_owner (一級負責人)
     ├─ deputy (副手)
     └─ escalate_to (升級給)

□ 生成虛擬責任人映射 (data/responsibility-map.json)
  ├─ Sales → 王經理 (Deputy: 李副理, Escalate: 林CEO)
  ├─ Production → 李廠長 (Deputy: 張主任, Escalate: 林CEO)
  ├─ HR → 陳總監 (Deputy: 吳經理, Escalate: 林CEO)
  ├─ Finance → 王CFO (Deputy: 劉經理, Escalate: 林CEO)
  └─ Overview → 林CEO (Deputy: 王CFO)

□ 設計告警規則 (data/alert-rules.json)
  ├─ Sales.achievementRate < 80% → P0
  ├─ Production.utilization < 75% → P0
  ├─ HR.vacancyRate > 10% → P1
  ├─ Finance.cashAdequacy < 30days → P0
  └─ ... (更多規則)

□ 在 backend.py 中添加告警引擎基礎
  ├─ def create_alert_rule(metric_key, condition, priority)
  ├─ def check_alert_triggered(metric_key, current_value)
  └─ def get_alert_rules()

□ 在 charts-integration.js 中添加虛擬告警檢測
  ├─ function detectAnomalies()
  ├─ function generateAlerts()
  └─ 模擬異常檢測和告警生成

【測試標準】
✓ 所有責任人映射正確
✓ 告警規則 JSON 格式正確
✓ 後端函數可以執行無錯誤
✓ 虛擬告警可以生成並返回

【提交】
git add data/responsibility-map.json data/alert-rules.json backend.py charts-integration.js
git commit -m "feat(action): 告警系統資料庫設計和規則框架"
git push origin feature/action-system-phase1
```

---

## 📊 進度記錄

### Day 1 EOD 檢查清單

```
【Dev 1 - UI/UX】
□ HTML 框架完成
□ CSS 樣式完成
□ 狀態計算邏輯完成
□ 代碼推送到 feature/ui-enhancement-phase1-2
□ 無 ESLint 錯誤

【Dev 2 - 圖表】
□ 虛擬資料完成
□ 圖表容器添加完成
□ 初始化函數框架完成
□ 代碼推送到 feature/new-charts-20
□ 無 ESLint 錯誤

【Dev 3 - 行動系統】
□ 資料庫 schema 完成
□ 責任人映射完成
□ 告警規則完成
□ 後端基礎函數完成
□ 代碼推送到 feature/action-system-phase1
□ 無錯誤

【團隊】
□ 所有人代碼都推送到 GitHub
□ 所有人的分支都能正常合併
□ 文檔已更新
```

### 實際進度 (待填寫)

```
【09:30】站會完成 - 
【10:00】開始開發 - 
【12:00】中午進度 - 
【15:00】下午進度 - 
【17:00】EOD 檢查 - 
【EOD】  提交狀態 - ✅ / ⚠️ / ❌
```

---

## 🎯 如果遇到問題

### Dev 1 常見問題

```
Q: CSS 如何預覽？
A: 在 VS Code 安裝 Live Server 插件，右鍵 index.html → "Open with Live Server"

Q: 如何檢查 JavaScript 錯誤？
A: F12 打開開發者工具 → Console 選項卡

Q: 如何同步最新代碼？
A: git fetch origin && git rebase origin/main
```

### Dev 2 常見問題

```
Q: 如何確認圖表會顯示？
A: 打開 HTML → F12 → Console 檢查是否有錯誤 → 檢查 canvas 元素是否存在

Q: 虛擬資料格式如何驗證？
A: 使用 JSON 在線驗證工具，或在 Node.js 中執行 JSON.parse()

Q: 如何測試圖表初始化？
A: 在 Console 中執行 window.charts 查看是否有圖表實例
```

### Dev 3 常見問題

```
Q: 如何測試 API？
A: 使用 Postman 發送 HTTP 請求測試 API 端點

Q: 資料庫表如何建立？
A: 執行 .sql 腳本或在 Python 中使用 SQLAlchemy

Q: 如何模擬異常檢測？
A: 在虛擬資料中設置超出門檻的值，確認告警被觸發
```

---

## 📞 每日同步節奏

```
09:30  ← 站會（15分鐘）
10:00  ← 開發開始
12:00  ← 午餐
13:00  ← 下午開發
15:00  ← 快速同步（5分鐘）檢查依賴
16:30  ← 代碼提交和文檔更新
17:00  ← EOD 記錄進度和明日計劃
```

---

## ✅ 成功標誌

**Day 1 成功 = 所有人代碼都推送到 GitHub + 無重大錯誤**

```
✓ Dev 1: Phase 1.1 狀態燈號 HTML/CSS/JS 框架完成
✓ Dev 2: 20 個圖表虛擬資料 + 容器框架完成
✓ Dev 3: 告警系統資料庫 + 規則框架完成
✓ 所有代碼通過 Code Review
✓ 明日有明確的工作計劃
```

---

**文檔狀態**: ✅ 就緒  
**下一步**: 09:00 早上站會準時開始


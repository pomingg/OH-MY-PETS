# LLM 推理引擎 - 地端 + 雲端混合架構

## 📋 概覽

本目錄包含「毛孩生活科技」企業戰情中心的 LLM Text-to-SQL 引擎，採用**地端優先、雲端兜底**的混合策略。

## 🏗️ 目錄結構

```
llm/
├── config/              # 配置文件（config.yaml）
├── engine/              # Text-to-SQL 引擎核心代碼
│   ├── __init__.py
│   ├── local_inference.py    # 本地推理（Ollama API）
│   ├── cloud_fallback.py     # Claude API 兜底
│   └── smart_generator.py    # 混合邏輯協調器
├── safety/              # 五層安全防護
│   ├── __init__.py
│   ├── sql_validator.py      # SQL 驗證
│   ├── whitelist.py          # 表/操作白名單
│   ├── rls.py                # 行級安全性
│   └── audit_logger.py       # 審計日誌
├── schema/              # Schema 精簡文檔
│   ├── schema-for-llm.md     # LLM 可見的 Schema 描述
│   └── examples.sql          # Few-shot 示例
├── prompts/             # Prompt 模板
│   ├── text_to_sql.prompt
│   └── weekly_report.prompt
├── models/              # 模型文件存放位置（由 Ollama 自動管理）
├── logs/                # 運行日誌和審計日誌
├── tests/               # 單元測試
│   ├── test_engine.py
│   ├── test_safety.py
│   └── test_integration.py
├── requirements.txt     # Python 依賴
├── __init__.py
└── README.md           # 本文件
```

## 🚀 快速開始

### 1. 環境設置

```bash
# 建立虛擬環境
python -m venv venv
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 複製環境變數模板
copy .env.example .env
# 編輯 .env 文件，填入 Claude API Key 等
```

### 2. 安裝推理框架

#### Ollama（推薦）
```bash
# 安裝 Ollama
# 從 https://ollama.ai/download 下載

# 啟動 Ollama 服務
ollama serve

# 在另一個終端，拉取模型
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# 驗證
curl -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "qwen2.5-coder:14b-instruct-q4_K_M",
    "prompt": "SELECT * FROM",
    "stream": false
  }'
```

### 3. 配置

編輯 `config/config.yaml`：
- 設置 CLAUDE_API_KEY（用於兜底）
- 配置資料庫連線參數
- 調整推理參數

### 4. 運行

```bash
# 測試 Text-to-SQL 引擎
python -m engine.smart_generator test

# 運行單元測試
pytest tests/ -v

# 集成測試（需要 Streamlit 應用配合）
pytest tests/test_integration.py -v
```

## 🔄 工作流程

### 查詢流程

```
用戶查詢（自然語言）
    ↓
【第一層 - 地端推理】(Qwen2.5-Coder-14B)
    ↓
├─ 成功 (88-92%) → 進入安全檢驗
│                  ↓
│              【安全防護層】(五層驗證)
│                  ↓
│              ├─ 通過 → 執行 SQL → 結果展示 ✅
│              └─ 失敗 → 拒絕 + 記錄 🛑
│
└─ 失敗或低信心 (8-12%) → 轉向第二層
                  ↓
          【第二層 - Claude API】
                  ↓
              生成 SQL → 安全檢驗 → 執行 → 結果展示
```

### 周報生成流程

```
觸發周報生成
    ↓
【數據提取】- 從資料庫抓取本週關鍵指標
    ↓
【異常偵測】- 識別警示和異常值
    ↓
【Claude API 調用】- 生成業務洞察和建議
    ↓
【組織成 Markdown】- 格式化輸出
    ↓
Streamlit 展示 + 導出選項
```

## 📊 效能目標

| 指標 | 目標 | 備註 |
|------|------|------|
| 地端成功率 | 88-92% | Qwen2.5-Coder-14B 準確率 |
| 平均延遲 | 2-5 秒 | 不包括 DB 查詢時間 |
| 並發請求 | 1-2 個 | VRAM 限制 |
| API Fallback 頻率 | < 15% | 月均統計 |
| 可用性 | > 99% | 包括雲端兜底 |

## 🔒 安全防護

### 五層架構

1. **SQL 語法驗證** - 檢查 SQL 是否合法
2. **操作白名單** - 只允許 SELECT 等讀操作
3. **表白名單** - 只允許訪問核心 7 張表
4. **行級安全 (RLS)** - 根據使用者角色過濾數據
5. **審計日誌** - 記錄所有查詢操作

### 禁止操作

```
❌ INSERT, UPDATE, DELETE
❌ DROP, ALTER, TRUNCATE
❌ EXEC, EXECUTE
```

## 📝 環境變數

`.env` 文件示例：

```bash
# Claude API（兜底用）
CLAUDE_API_KEY=sk-...

# 資料庫
DB_HOST=localhost
DB_PORT=5432
DB_NAME=oh_pets_company
DB_USER=postgres
DB_PASSWORD=...

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:14b-instruct-q4_K_M

# Redis（快取，可選）
REDIS_URL=redis://localhost:6379

# 日誌
LOG_LEVEL=INFO
```

## 🧪 測試

```bash
# 運行所有測試
pytest tests/ -v

# 運行特定測試
pytest tests/test_engine.py::test_sql_generation -v

# 生成覆蓋率報告
pytest tests/ --cov=engine --cov=safety --cov-report=html
```

## 📚 相關文件

- `../CLAUDE.md` - 長期技術決策說明
- `../.claude/handoff-llm.md` - LLM 部署詳細規格
- `schema/schema-for-llm.md` - Schema 精簡描述（待編寫）

## 🔧 配置調整

### 模型選擇

若 Qwen2.5-Coder-14B 無法滿足需求，可考慮：

- **Qwen2.5-Coder-7B** - 更輕量，準確率 78-82%
- **Qwen2.5-Coder-32B** - 更精準，但需更多 VRAM（需升級硬體）
- **CodeLlama** - 純代碼優化

### 量化版本

- `q4_K_M` （當前）- 平衡效能與精度
- `q6_K` - 更高精度，但需更多 VRAM
- `q3_K_M` - 更輕量，但精度下降

## 📞 支援

遇到問題？查看：
1. `logs/llm_engine.log` - 引擎日誌
2. `logs/audit.log` - 安全日誌
3. 本項目的 [handoff-llm.md](../.claude/handoff-llm.md) - 詳細設計文件

---

**版本**: 1.0.0  
**最後更新**: 2025年12月  
**維護者**: 毛孩生活科技 AI 小組

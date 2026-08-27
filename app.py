"""
OH-Pets Company BI Dashboard - Streamlit Application
企業戰情中心 - 完全優化版（對標原型.html設計）
"""

import streamlit as st
import psycopg2
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ============================================================
# 配置
# ============================================================

st.set_page_config(
    page_title="毛孩生活 BI 戰情中心",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'oh_pets_company',
    'user': 'postgres',
    'password': 'postgres123!@#'
}

COLORS = {
    'sales': '#E8A33D',
    'production': '#35B0AE',
    'hr': '#9B84E8',
    'finance': '#4FBD84',
}

# ============================================================
# 完整優化版 CSS
# ============================================================

CUSTOM_CSS = """
<style>
  :root {
    --bg: #0B0F20;
    --bg-elevated: #10142A;
    --surface: #161C3A;
    --surface-hover: #1D2448;
    --border: #262E58;
    --border-soft: #1C2346;
    --text-primary: #EEF0FA;
    --text-secondary: #9BA3CC;
    --text-muted: #666E9C;

    --sales: #E8A33D;
    --sales-soft: rgba(232, 163, 61, .13);
    --production: #35B0AE;
    --production-soft: rgba(53, 176, 174, .13);
    --hr: #9B84E8;
    --hr-soft: rgba(155, 132, 232, .13);
    --finance: #4FBD84;
    --finance-soft: rgba(79, 189, 132, .13);

    --good: #4FBD84;
    --warn: #E8A33D;
    --bad: #E1596B;

    --font-display: 'Space Grotesk', 'Noto Sans TC', sans-serif;
    --font-body: 'Noto Sans TC', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
  }

  * { box-sizing: border-box; }

  body {
    background: var(--bg) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  #MainMenu { display: none; }
  footer { display: none; }
  header { display: none; }

  .stApp {
    background: var(--bg) !important;
  }

  [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    padding: 0 !important;
  }

  /* ========== 頂部品牌列 ========== */
  .topbar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: linear-gradient(180deg, var(--bg-elevated) 0%, rgba(16, 20, 42, .98) 100%);
    border-bottom: 2px solid var(--border);
    backdrop-filter: blur(12px);
    padding: 16px 32px;
  }

  .topbar-inner {
    max-width: 1440px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 28px;
    flex-wrap: wrap;
  }

  .brand {
    display: flex;
    align-items: baseline;
    gap: 12px;
  }

  .brand-mark {
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 18px;
    letter-spacing: .08em;
    color: var(--bg);
    background: linear-gradient(135deg, #E8A33D, #D9922F);
    padding: 6px 11px;
    border-radius: 8px;
    box-shadow: 0 6px 16px rgba(232, 163, 61, 0.25);
    min-width: 45px;
    text-align: center;
  }

  .brand-name {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 18px;
    letter-spacing: .01em;
    background: linear-gradient(90deg, #EEF0FA, #9BA3CC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .brand-sub {
    font-size: 10px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    letter-spacing: .05em;
    font-weight: 600;
  }

  .meta-strip {
    display: flex;
    align-items: center;
    gap: 28px;
    font-size: 12px;
    color: var(--text-secondary);
  }

  .meta-strip .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4FBD84;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 10px rgba(79, 189, 132, 0.6);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 10px rgba(79, 189, 132, 0.6); }
    50% { opacity: 0.5; box-shadow: 0 0 20px rgba(79, 189, 132, 0.3); }
  }

  .meta-strip b {
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-weight: 700;
  }

  /* ========== 標簽頁導航 ========== */
  .tabs-container {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 32px;
    display: flex;
    gap: 2px;
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
  }

  .tab-btn {
    appearance: none;
    border: none;
    background: transparent;
    color: var(--text-muted);
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 15px;
    padding: 14px 18px;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    white-space: nowrap;
    transition: all .25s ease;
    letter-spacing: .01em;
  }

  .tab-btn:hover {
    color: var(--text-primary);
    background: rgba(155, 132, 232, 0.05);
  }

  .tab-btn.active {
    color: var(--text-primary);
    border-bottom-color: currentColor;
  }

  /* ========== 頁面容器 ========== */
  .page-wrapper {
    max-width: 1440px;
    margin: 0 auto;
    padding: 36px 32px;
  }

  /* ========== 分段頭部 ========== */
  .section-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin: 0 0 28px;
    flex-wrap: wrap;
    gap: 12px;
    padding-bottom: 18px;
    border-bottom: 3px solid var(--border-soft);
  }

  .section-title {
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 800;
    margin: 0;
    color: var(--text-primary);
    letter-spacing: -.01em;
  }

  .section-sub {
    font-size: 12px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    letter-spacing: .04em;
    text-transform: uppercase;
    font-weight: 600;
  }

  /* ========== 篩選欄 ========== */
  .filter-bar {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    background: linear-gradient(135deg, rgba(22, 28, 58, 0.8), rgba(29, 36, 72, 0.8));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 28px;
    backdrop-filter: blur(8px);
  }

  .filter-label-icon {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .02em;
  }

  .filter-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .filter-item label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 600;
  }

  .filter-item select {
    appearance: none;
    background: var(--bg-elevated);
    color: var(--text-primary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 7px 28px 7px 12px;
    font-family: var(--font-body);
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%239BA3CC'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    padding-right: 30px;
  }

  .filter-item select:hover {
    border-color: var(--text-secondary);
  }

  .filter-item select:focus {
    outline: none;
    border-color: var(--text-primary);
  }

  .filter-reset {
    margin-left: auto;
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 12px;
    padding: 7px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-family: var(--font-body);
    font-weight: 600;
    transition: all .2s ease;
  }

  .filter-reset:hover {
    color: var(--text-primary);
    border-color: var(--text-primary);
    background: rgba(155, 132, 232, 0.1);
  }

  /* ========== KPI 環形卡片 ========== */
  .ring-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 18px;
    margin-bottom: 36px;
  }

  .ring-card {
    background: linear-gradient(135deg, rgba(22, 28, 58, 0.8), rgba(29, 36, 72, 0.6));
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    transition: all .3s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .ring-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--sales), var(--production), var(--hr), var(--finance));
    opacity: 0;
    transition: opacity .3s ease;
  }

  .ring-card:hover {
    border-color: var(--text-secondary);
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
    background: linear-gradient(135deg, rgba(22, 28, 58, 1), rgba(29, 36, 72, 0.8));
  }

  .ring-card:hover::before {
    opacity: 1;
  }

  .ring-label {
    font-weight: 700;
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: .06em;
  }

  .ring-score {
    font-family: var(--font-mono);
    font-size: 36px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -.02em;
  }

  .ring-delta {
    font-size: 12px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-weight: 600;
  }

  .ring-delta.up {
    color: var(--good);
  }

  .ring-delta.down {
    color: var(--bad);
  }

  /* ========== 警示區優化 ========== */
  .alerts {
    background: linear-gradient(135deg, rgba(232, 163, 61, 0.08), rgba(225, 89, 107, 0.04));
    border: 1.5px solid var(--warn);
    border-radius: 14px;
    padding: 0;
    margin-bottom: 36px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(232, 163, 61, 0.1);
  }

  .alerts-head {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(232, 163, 61, 0.2);
    background: rgba(232, 163, 61, 0.06);
  }

  .alerts-head h3 {
    margin: 0;
    font-size: 15px;
    font-family: var(--font-display);
    font-weight: 800;
    color: var(--text-primary);
  }

  .alert-row {
    display: grid;
    grid-template-columns: 90px 110px 1fr 160px;
    gap: 16px;
    align-items: center;
    padding: 16px 24px;
    border-bottom: 1px solid var(--border-soft);
    font-size: 13px;
    transition: background .2s ease;
  }

  .alert-row:hover {
    background: rgba(155, 132, 232, 0.08);
  }

  .alert-row:last-child {
    border-bottom: none;
  }

  .sev {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    padding: 5px 11px;
    border-radius: 20px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: .05em;
  }

  .sev.high {
    background: rgba(225, 89, 107, 0.25);
    color: var(--bad);
  }

  .sev.mid {
    background: rgba(232, 163, 61, 0.25);
    color: var(--warn);
  }

  .sev.low {
    background: rgba(79, 189, 132, 0.15);
    color: var(--good);
  }

  .domain-tag {
    font-size: 11px;
    font-weight: 800;
    padding: 5px 11px;
    border-radius: 8px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: .03em;
  }

  .alert-desc {
    color: var(--text-secondary);
    line-height: 1.6;
  }

  .alert-desc b {
    color: var(--text-primary);
    font-weight: 700;
  }

  .alert-metric {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-secondary);
    text-align: right;
    font-weight: 700;
  }

  /* ========== 領域網格 ========== */
  .domain-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
    gap: 20px;
    margin-bottom: 36px;
  }

  .domain-block {
    background: linear-gradient(135deg, rgba(22, 28, 58, 0.9), rgba(29, 36, 72, 0.7));
    border: 1.5px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    transition: all .3s ease;
  }

  .domain-block:hover {
    border-color: var(--text-secondary);
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
  }

  .domain-block-head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 18px 22px;
    border-bottom: 2px solid var(--border-soft);
    background: rgba(53, 176, 174, 0.04);
  }

  .domain-dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    box-shadow: 0 0 12px currentColor;
  }

  .domain-block-head h4 {
    margin: 0;
    font-size: 15px;
    font-family: var(--font-display);
    font-weight: 800;
    color: var(--text-primary);
  }

  .kpi-mini-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    background: var(--border-soft);
  }

  .kpi-mini {
    background: var(--surface);
    padding: 16px 18px;
    transition: all .2s ease;
  }

  .kpi-mini:hover {
    background: var(--surface-hover);
  }

  .kpi-mini .lbl {
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: .03em;
    font-weight: 700;
  }

  .kpi-mini .val {
    font-family: var(--font-mono);
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
  }

  .kpi-mini .delta {
    font-size: 11px;
    margin-top: 6px;
    font-family: var(--font-mono);
    color: var(--text-muted);
    font-weight: 700;
  }

  .kpi-mini .delta.up { color: var(--good); }
  .kpi-mini .delta.down { color: var(--bad); }

  /* ========== KPI 卡片條帶 ========== */
  .kpi-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
  }

  .kpi-card {
    background: linear-gradient(135deg, rgba(22, 28, 58, 0.9), rgba(29, 36, 72, 0.7));
    border: 1.5px solid var(--border);
    border-left: 5px solid var(--accent);
    border-radius: 12px;
    padding: 20px 22px;
    transition: all .3s ease;
  }

  .kpi-card:hover {
    border-color: var(--accent);
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
    background: linear-gradient(135deg, rgba(22, 28, 58, 1), rgba(29, 36, 72, 0.85));
  }

  .kpi-card .lbl {
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: .03em;
    font-weight: 700;
  }

  .kpi-card .val {
    font-family: var(--font-mono);
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
    color: var(--text-primary);
  }

  .kpi-card .sub {
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 8px;
    line-height: 1.5;
    font-weight: 600;
  }

  .kpi-card .sub.up { color: var(--good); }
  .kpi-card .sub.down { color: var(--bad); }

  /* ========== 圖表容器 ========== */
  .chart-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 28px;
  }

  .chart-grid.full {
    grid-template-columns: 1fr;
  }

  @media(max-width: 1100px) {
    .chart-grid { grid-template-columns: 1fr; }
  }

  .panel {
    background: linear-gradient(135deg, rgba(22, 28, 58, 0.9), rgba(29, 36, 72, 0.7));
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    transition: all .3s ease;
  }

  .panel:hover {
    border-color: var(--text-secondary);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
  }

  .panel h4 {
    margin: 0 0 4px;
    font-size: 15px;
    font-family: var(--font-display);
    font-weight: 800;
    color: var(--text-primary);
  }

  .panel .cap {
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 16px;
  }

  /* ========== 表格 ========== */
  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    color: var(--text-secondary);
    background: linear-gradient(135deg, rgba(22, 28, 58, 0.9), rgba(29, 36, 72, 0.7));
    border: 1.5px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    margin-top: 20px;
  }

  .data-table th {
    text-align: left;
    color: var(--text-muted);
    font-weight: 800;
    font-size: 12px;
    padding: 14px 16px;
    border-bottom: 2px solid var(--border);
    text-transform: uppercase;
    letter-spacing: .02em;
    background: rgba(155, 132, 232, 0.06);
  }

  .data-table td {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border-soft);
  }

  .data-table tr:hover td {
    background: rgba(155, 132, 232, 0.06);
  }

  .data-table td.strong {
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-weight: 700;
  }

  .risk-badge {
    font-size: 11px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 20px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: .03em;
  }

  .risk-badge.high { background: rgba(225, 89, 107, 0.25); color: var(--bad); }
  .risk-badge.mid { background: rgba(232, 163, 61, 0.25); color: var(--warn); }
  .risk-badge.low { background: rgba(79, 189, 132, 0.15); color: var(--good); }

  /* ========== 圖例 ========== */
  .legend-row {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 12px;
    font-size: 12px;
    color: var(--text-secondary);
  }

  .legend-row span {
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }

  .legend-row i {
    width: 10px;
    height: 10px;
    border-radius: 3px;
    display: inline-block;
  }

  /* ========== 頁腳 ========== */
  .footnote {
    font-size: 11px;
    color: var(--text-muted);
    text-align: center;
    padding: 40px 0 60px;
    border-top: 1px dashed var(--border-soft);
    margin-top: 40px;
    line-height: 1.8;
  }

  /* ========== 滾動條 ========== */
  ::-webkit-scrollbar {
    height: 10px;
    width: 10px;
  }

  ::-webkit-scrollbar-track {
    background: var(--bg);
  }

  ::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 5px;
    transition: background .2s ease;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
  }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# 資料庫連接
# ============================================================

@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"資料庫連接失敗: {e}")
        return None

@st.cache_data
def query_database(sql):
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql_query(sql, conn)
            return df
        except Exception as e:
            st.error(f"查詢失敗: {e}")
            return None
    return None

# ============================================================
# 全域狀態
# ============================================================

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'overview'

# ============================================================
# 圖表樣式函數
# ============================================================

def get_chart_layout(title="", height=320, color_scheme='default'):
    """統一的圖表佈局"""
    return dict(
        template='plotly_dark',
        plot_bgcolor='#161C3A',
        paper_bgcolor='#161C3A',
        font=dict(
            family="'Noto Sans TC', sans-serif",
            size=11,
            color='#9BA3CC'
        ),
        showlegend=True,
        hovermode='x unified',
        height=height,
        margin=dict(l=50, r=20, t=30, b=50),
        title=dict(
            text=title,
            font=dict(size=14, color='#EEF0FA', family="'Space Grotesk', sans-serif"),
            x=0.02,
            xanchor='left'
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(38, 46, 88, 0.4)',
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='var(--border)',
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(38, 46, 88, 0.4)',
            zeroline=False,
        )
    )

# ============================================================
# 頂部 + 導航
# ============================================================

def render_header():
    """頂部品牌列和導航"""
    st.markdown("""
    <div class="topbar">
      <div class="topbar-inner">
        <div class="brand">
          <span class="brand-mark">🐾</span>
          <div>
            <div class="brand-name">毛孩生活科技｜企業戰情中心</div>
            <div class="brand-sub">MAOHAI PET LIFE TECH — COMMAND CENTER</div>
          </div>
        </div>
        <div class="meta-strip">
          <span><span class="dot"></span>即時資料連接</span>
          <span>快照期間：<b>FY2025 / Q4</b></span>
          <span>更新於：<b>""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</b></span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("📊 總覽", key="tab_ov", use_container_width=True):
            st.session_state.active_tab = "overview"
            st.rerun()
    with col2:
        if st.button("💰 銷售指標", key="tab_sa", use_container_width=True):
            st.session_state.active_tab = "sales"
            st.rerun()
    with col3:
        if st.button("🏭 生產與庫存", key="tab_pr", use_container_width=True):
            st.session_state.active_tab = "production"
            st.rerun()
    with col4:
        if st.button("👥 人力資源", key="tab_hr", use_container_width=True):
            st.session_state.active_tab = "hr"
            st.rerun()
    with col5:
        if st.button("📈 財務指標", key="tab_fi", use_container_width=True):
            st.session_state.active_tab = "finance"
            st.rerun()

    st.divider()

# ============================================================
# 總覽頁面
# ============================================================

def render_overview():
    """總覽頁面"""
    st.markdown("""
    <div class="section-head">
      <h2 class="section-title">企業戰情中心總覽</h2>
      <span class="section-sub">DOMAIN HEALTH SNAPSHOT</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    sales_sql = "SELECT COALESCE(SUM(order_amount), 0) as total FROM fact_orders"
    production_sql = "SELECT COALESCE(AVG(yield_rate), 0) as avg_yield FROM fact_production WHERE yield_rate > 0"
    employee_sql = "SELECT COUNT(*) as count FROM dim_employee WHERE is_active = TRUE"
    finance_sql = "SELECT COALESCE(SUM(revenue), 0) as total_rev FROM fact_finance"

    sales_data = query_database(sales_sql)
    production_data = query_database(production_sql)
    employee_data = query_database(employee_sql)
    finance_data = query_database(finance_sql)

    with col1:
        total_sales = sales_data['total'].values[0] if sales_data is not None else 0
        st.markdown(f"""
        <div class="ring-card">
          <div class="ring-label">💰 銷售營收</div>
          <div class="ring-score">NT${total_sales/1e8:.2f}B</div>
          <div class="ring-delta up">▲ YoY +8.4%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_yield = production_data['avg_yield'].values[0] if production_data is not None else 0
        st.markdown(f"""
        <div class="ring-card">
          <div class="ring-label">🏭 生產良率</div>
          <div class="ring-score">{avg_yield:.1f}%</div>
          <div class="ring-delta up">▲ 0.3pt</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        emp_count = employee_data['count'].values[0] if employee_data is not None else 0
        st.markdown(f"""
        <div class="ring-card">
          <div class="ring-label">👥 在職人數</div>
          <div class="ring-score">{int(emp_count)}</div>
          <div class="ring-delta">人</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        total_rev = finance_data['total_rev'].values[0] if finance_data is not None else 0
        st.markdown(f"""
        <div class="ring-card">
          <div class="ring-label">📈 財務總收入</div>
          <div class="ring-score">NT${total_rev/1e8:.2f}B</div>
          <div class="ring-delta down">▼ 流動比 149%</div>
        </div>
        """, unsafe_allow_html=True)

    # 警示區
    st.markdown("""
    <div class="alerts">
      <div class="alerts-head">
        <span style="font-size: 20px;">⚠️</span>
        <h3>追蹤警示 — 未達標 / 異常項目</h3>
      </div>
      <div class="alert-row">
        <span class="sev high">高風險</span>
        <span class="domain-tag" style="background:var(--hr-soft);color:var(--hr);">人資</span>
        <span class="alert-desc"><b>生產部接班梯隊風險</b>：經理級平均年齡 54 歲，下一階梯（副理級）僅 2 人</span>
        <span class="alert-metric">梯隊比 1:2</span>
      </div>
      <div class="alert-row">
        <span class="sev mid">中風險</span>
        <span class="domain-tag" style="background:var(--production-soft);color:var(--production);">生產</span>
        <span class="alert-desc"><b>B 廠稼動率未達標</b>：78%（目標 85%），缺料與換模停機比重增加</span>
        <span class="alert-metric">78% / 85%</span>
      </div>
      <div class="alert-row">
        <span class="sev mid">中風險</span>
        <span class="domain-tag" style="background:var(--sales-soft);color:var(--sales);">銷售</span>
        <span class="alert-desc"><b>保暖寵物窩退貨率異常</b>：12.4%（全品項均值 4.1%），品質問題佔比逾六成</span>
        <span class="alert-metric">12.4% ▲</span>
      </div>
      <div class="alert-row">
        <span class="sev low">低風險</span>
        <span class="domain-tag" style="background:var(--finance-soft);color:var(--finance);">財務</span>
        <span class="alert-desc"><b>流動比率下滑</b>至 149%（上季 171%），應付帳款增加壓縮短期償債空間</span>
        <span class="alert-metric">149% ▼</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 四大領域
    st.markdown("""
    <div class="section-head">
      <h2 class="section-title" style="font-size:20px;">四大領域關鍵指標</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="domain-block">
          <div class="domain-block-head">
            <span class="domain-dot" style="background:var(--sales);"></span>
            <h4>銷售指標</h4>
          </div>
          <div class="kpi-mini-grid">
            <div class="kpi-mini"><div class="lbl">營收達成率</div><div class="val">96%</div><div class="delta down">▼ 目標 100%</div></div>
            <div class="kpi-mini"><div class="lbl">年增率 YoY</div><div class="val">+8.4%</div><div class="delta up">▲ 較去年</div></div>
            <div class="kpi-mini"><div class="lbl">毛利率</div><div class="val">34.2%</div><div class="delta up">▲ 0.6pt</div></div>
            <div class="kpi-mini"><div class="lbl">退貨率</div><div class="val">5.1%</div><div class="delta down">▲ 0.4pt</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="domain-block">
          <div class="domain-block-head">
            <span class="domain-dot" style="background:var(--production);"></span>
            <h4>生產與庫存</h4>
          </div>
          <div class="kpi-mini-grid">
            <div class="kpi-mini"><div class="lbl">OEE 綜合效率</div><div class="val">71.3%</div><div class="delta down">▼ 目標 78%</div></div>
            <div class="kpi-mini"><div class="lbl">良率</div><div class="val">97.2%</div><div class="delta up">▲ 0.3pt</div></div>
            <div class="kpi-mini"><div class="lbl">庫存周轉天數</div><div class="val">46天</div><div class="delta down">▲ 3天</div></div>
            <div class="kpi-mini"><div class="lbl">供應商準時率</div><div class="val">89%</div><div class="delta up">▲ 1.2pt</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="domain-block">
          <div class="domain-block-head">
            <span class="domain-dot" style="background:var(--hr);"></span>
            <h4>人力資源</h4>
          </div>
          <div class="kpi-mini-grid">
            <div class="kpi-mini"><div class="lbl">年化離職率</div><div class="val">14.2%</div><div class="delta down">▲ 1.1pt</div></div>
            <div class="kpi-mini"><div class="lbl">出勤率</div><div class="val">97.8%</div><div class="delta">持平</div></div>
            <div class="kpi-mini"><div class="lbl">人均產值</div><div class="val">218萬</div><div class="delta up">▲ 4.5%</div></div>
            <div class="kpi-mini"><div class="lbl">人力成本佔營收比</div><div class="val">18.6%</div><div class="delta down">▲ 0.5pt</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="domain-block">
          <div class="domain-block-head">
            <span class="domain-dot" style="background:var(--finance);"></span>
            <h4>財務指標</h4>
          </div>
          <div class="kpi-mini-grid">
            <div class="kpi-mini"><div class="lbl">毛利率</div><div class="val">38.4%</div><div class="delta up">▲ 1.2pt</div></div>
            <div class="kpi-mini"><div class="lbl">淨利率</div><div class="val">18.5%</div><div class="delta down">▼ 0.3pt</div></div>
            <div class="kpi-mini"><div class="lbl">流動比率</div><div class="val">149%</div><div class="delta down">▼ 22pt</div></div>
            <div class="kpi-mini"><div class="lbl">應收帳款周轉天數</div><div class="val">52天</div><div class="delta up">▲ 4天</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 趨勢圖
    st.markdown("""<div class="section-head"><h2 class="section-title" style="font-size:20px;">業務趨勢分析</h2></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        trend_sql = """
        SELECT dd.date, COUNT(*) as order_count
        FROM fact_orders fo
        JOIN dim_date dd ON fo.order_date_id = dd.date_id
        WHERE dd.date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY dd.date
        ORDER BY dd.date
        """
        trend_data = query_database(trend_sql)

        if trend_data is not None and len(trend_data) > 0:
            fig = px.line(trend_data, x='date', y='order_count',
                         labels={'order_count': '訂單數', 'date': '日期'})
            fig.update_traces(
                line=dict(color=COLORS['sales'], width=3),
                fill='tozeroy',
                fillcolor=f"rgba(232, 163, 61, 0.12)"
            )
            fig.update_layout(**get_chart_layout("訂單趨勢（最近 30 天）", 340))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        sales_dist_sql = """
        SELECT dp.product_line, COUNT(*) as cnt
        FROM fact_orders fo
        JOIN dim_product dp ON fo.product_id = dp.product_id
        GROUP BY dp.product_line
        """
        sales_dist = query_database(sales_dist_sql)
        if sales_dist is not None and len(sales_dist) > 0:
            fig = px.pie(sales_dist, values='cnt', names='product_line',
                        color_discrete_sequence=[COLORS['sales'], COLORS['production'], COLORS['hr'], COLORS['finance']])
            fig.update_traces(
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>訂單數: %{value}<br>佔比: %{percent}<extra></extra>'
            )
            fig.update_layout(**get_chart_layout("銷售分布（按產品線）", 340))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="footnote">
      ＊本頁所有數據均為模擬資料，用於展示戰情中心資訊架構與分析設計邏輯，不代表任何真實企業經營狀況。
    </div>
    """, unsafe_allow_html=True)

def render_sales():
    """銷售頁面"""
    st.markdown("""
    <div class="section-head">
      <h2 class="section-title" style="color: #E8A33D;">銷售指標</h2>
      <span class="section-sub">SALES &amp; CHANNEL PERFORMANCE</span>
    </div>
    """, unsafe_allow_html=True)

    # 篩選欄
    st.markdown("""
    <div class="filter-bar">
      <span class="filter-label-icon">篩選檢視</span>
      <div class="filter-item">
        <label>產品線</label>
        <select id="salesLineFilter">
          <option>全部</option>
          <option>自有品牌成品</option>
          <option>零售代工</option>
        </select>
      </div>
      <div class="filter-item">
        <label>通路</label>
        <select id="salesChannelFilter">
          <option>全部</option>
          <option>電商 DTC</option>
          <option>實體經銷</option>
          <option>零售代工</option>
        </select>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI 條帶
    cols = st.columns(6)
    kpis_sales = [
        ("營收達成率", "96%", "目標 2,138 萬 ／ 實際 2,050 萬", False),
        ("年增率 YoY", "+8.4%", "連續4季正成長", True),
        ("毛利率", "34.2%", "較上季 +0.6pt", True),
        ("整體退貨率", "5.1%", "1項產品異常偏高", False),
        ("新品活力指數", "18.6%", "近12月新品營收佔比", True),
        ("平均動銷率", "76%", "出貨量／(期初庫存+進貨)", True),
    ]

    for idx, (col, (lbl, val, sub, is_up)) in enumerate(zip(cols, kpis_sales)):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent: var(--sales);">
              <div class="lbl">{lbl}</div>
              <div class="val">{val}</div>
              <div class="sub {'up' if is_up else 'down'}">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    # 圖表
    col1, col2 = st.columns(2)

    with col1:
        sql = """
        SELECT dp.product_line, COUNT(*) as cnt
        FROM fact_orders fo
        JOIN dim_product dp ON fo.product_id = dp.product_id
        GROUP BY dp.product_line
        """
        data = query_database(sql)
        if data is not None and len(data) > 0:
            fig = px.bar(data, x='product_line', y='cnt',
                        color_discrete_sequence=[COLORS['sales']],
                        labels={'cnt': '訂單數', 'product_line': '產品線'})
            fig.update_traces(marker_line_color='rgba(0,0,0,0)')
            fig.update_layout(**get_chart_layout("月度營收趨勢", 340))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        sql = """
        SELECT dp.product_line, SUM(fo.order_amount) as amt
        FROM fact_orders fo
        JOIN dim_product dp ON fo.product_id = dp.product_id
        GROUP BY dp.product_line
        """
        data = query_database(sql)
        if data is not None and len(data) > 0:
            fig = px.pie(data, values='amt', names='product_line',
                        color_discrete_sequence=[COLORS['sales'], '#D9922F', '#E8B33D', '#D8932D'])
            fig.update_traces(textinfo='label+percent')
            fig.update_layout(**get_chart_layout("通路貢獻佔比", 340))
            st.plotly_chart(fig, use_container_width=True)

    # 產品矩陣和退貨率
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4>產品組合 BCG 矩陣（公司內部貢獻版）</h4>", unsafe_allow_html=True)
        st.info("📊 X軸：年增率　Y軸：營收佔比　泡泡大小：營收規模")

        # 生成虛擬的BCG數據
        bcg_data = pd.DataFrame({
            'product': ['產品A', '產品B', '產品C', '產品D', '產品E'],
            'growth': [15, 8, -3, 12, 5],
            'revenue': [1200, 900, 600, 800, 500],
            'category': ['明星', '金牛', '瘦狗', '明星', '問題']
        })

        color_map = {'明星': COLORS['sales'], '金牛': COLORS['finance'],
                    '問題': COLORS['production'], '瘦狗': '#E1596B'}

        fig = px.scatter(bcg_data, x='growth', y='revenue', size='revenue',
                        color='category', text='product',
                        color_discrete_map=color_map)
        fig.update_traces(textposition='top center')
        fig.update_layout(**get_chart_layout("", 340))
        st.plotly_chart(fig, use_container_width=True)

        # 圖例
        st.markdown("""
        <div class="legend-row">
          <span><i style="background:#E8A33D;"></i>明星商品</span>
          <span><i style="background:#4FBD84;"></i>金牛商品</span>
          <span><i style="background:#35B0AE;"></i>問題商品</span>
          <span><i style="background:#E1596B;"></i>瘦狗商品</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h4>分產品退貨率</h4>", unsafe_allow_html=True)
        st.info("📊 紅色標示為異常偏高品項（>8%）")

        return_data = pd.DataFrame({
            'product': ['產品A', '產品B', '產品C', '產品D', '產品E'],
            'return_rate': [3.2, 12.4, 4.1, 2.8, 15.6]
        })

        fig = px.bar(return_data, x='product', y='return_rate',
                    color_discrete_sequence=[COLORS['sales']])
        fig.update_traces(marker_line_color='rgba(0,0,0,0)')
        fig.update_layout(**get_chart_layout("", 340))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="footnote">
      ＊模擬資料，僅供分析架構展示
    </div>
    """, unsafe_allow_html=True)

def render_production():
    """生產頁面"""
    st.markdown("""
    <div class="section-head">
      <h2 class="section-title" style="color: #35B0AE;">生產與庫存指標</h2>
      <span class="section-sub">MANUFACTURING &amp; SUPPLY CHAIN</span>
    </div>
    """, unsafe_allow_html=True)

    # 篩選欄
    st.markdown("""
    <div class="filter-bar">
      <span class="filter-label-icon">篩選檢視</span>
      <div class="filter-item">
        <label>廠區</label>
        <select id="plantFilter">
          <option>全部廠區</option>
          <option>A廠（主力組裝）</option>
          <option>B廠（零組件）</option>
          <option>C廠（衛星廠）</option>
        </select>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    kpis_prod = [
        ("OEE 綜合設備效率", "71.3%", "目標 78%", False),
        ("稼動率", "82.5%", "B廠偏低，詳見下圖", False),
        ("良率", "97.2%", "較上季 +0.3pt", True),
        ("庫存周轉天數", "46 天", "較上季 +3天", False),
    ]

    for col, (lbl, val, sub, is_up) in zip(cols, kpis_prod):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent: var(--production);">
              <div class="lbl">{lbl}</div>
              <div class="val">{val}</div>
              <div class="sub {'up' if is_up else 'down'}">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sql = """
        SELECT dp.plant_name, AVG(fp.yield_rate) as yield
        FROM fact_production fp
        JOIN dim_plant dp ON fp.plant_id = dp.plant_id
        WHERE fp.yield_rate > 0
        GROUP BY dp.plant_id, dp.plant_name
        """
        data = query_database(sql)
        if data is not None and len(data) > 0:
            fig = px.bar(data, x='plant_name', y='yield',
                        color_discrete_sequence=[COLORS['production']],
                        labels={'yield': '良率 (%)', 'plant_name': '廠區'})
            fig.update_traces(marker_line_color='rgba(0,0,0,0)')
            fig.update_layout(**get_chart_layout("OEE 趨勢（分廠區）", 340))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        downtime_data = pd.DataFrame({
            'reason': ['缺料停機', '換模停機', '設備故障', '其他'],
            'hours': [120, 90, 45, 30]
        })
        fig = px.pie(downtime_data, values='hours', names='reason',
                    color_discrete_sequence=[COLORS['production'], '#2A9D8F', '#E76F51', '#F4A261'])
        fig.update_layout(**get_chart_layout("停機原因分布", 340))
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4>呆滯庫存比例（分倉）</h4>", unsafe_allow_html=True)
        obsolete_data = pd.DataFrame({
            'warehouse': ['倉庫A', '倉庫B', '倉庫C'],
            'ratio': [15, 22, 8]
        })
        fig = px.bar(obsolete_data, x='warehouse', y='ratio',
                    color_discrete_sequence=[COLORS['production']])
        fig.update_layout(**get_chart_layout("", 340))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<h4>供應商準時交貨率排行</h4>", unsafe_allow_html=True)
        supplier_data = pd.DataFrame({
            'supplier': ['供應商A', '供應商B', '供應商C', '供應商D'],
            'ontime_rate': [92, 78, 88, 95]
        })
        fig = px.bar(supplier_data, x='supplier', y='ontime_rate',
                    color_discrete_sequence=[COLORS['production']])
        fig.update_layout(**get_chart_layout("", 340))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="footnote">
      ＊模擬資料，僅供分析架構展示
    </div>
    """, unsafe_allow_html=True)

def render_hr():
    """人資頁面"""
    st.markdown("""
    <div class="section-head">
      <h2 class="section-title" style="color: #9B84E8;">人力資源指標</h2>
      <span class="section-sub">WORKFORCE STRUCTURE &amp; HEALTH</span>
    </div>
    """, unsafe_allow_html=True)

    # 篩選欄
    st.markdown("""
    <div class="filter-bar">
      <span class="filter-label-icon">篩選檢視</span>
      <div class="filter-item">
        <label>部門</label>
        <select id="deptFilter">
          <option>全部部門</option>
          <option>生產部</option>
          <option>品保部</option>
          <option>供應鏈部</option>
          <option>業務部</option>
          <option>研發部</option>
        </select>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    kpis_hr = [
        ("年化離職率", "14.2%", "較上季 +1.1pt", False),
        ("出勤率", "97.8%", "持平", True),
        ("人均產值", "218 萬", "較上季 +4.5%", True),
        ("人力成本佔營收比", "18.6%", "較上季 +0.5pt", False),
    ]

    for col, (lbl, val, sub, is_up) in zip(cols, kpis_hr):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent: var(--hr);">
              <div class="lbl">{lbl}</div>
              <div class="val">{val}</div>
              <div class="sub {'up' if is_up else 'down'}">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age_data = pd.DataFrame({
            'age_group': ['20-30', '30-40', '40-50', '50-60', '60+'],
            'count': [45, 32, 68, 54, 12]
        })
        fig = px.bar(age_data, x='age_group', y='count',
                    color_discrete_sequence=[COLORS['hr']],
                    labels={'count': '人數', 'age_group': '年齡區間'})
        fig.update_layout(**get_chart_layout("年齡結構分布", 340))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        tenure_data = pd.DataFrame({
            'tenure': ['0-2年', '2-5年', '5-10年', '10-15年', '15+年'],
            'count': [38, 52, 61, 48, 12]
        })
        fig = px.bar(tenure_data, x='tenure', y='count',
                    color_discrete_sequence=[COLORS['hr']],
                    labels={'count': '人數', 'tenure': '年資'})
        fig.update_layout(**get_chart_layout("年資結構分布", 340))
        st.plotly_chart(fig, use_container_width=True)

    # 職等結構
    st.markdown("<h4>職等結構分布</h4>", unsafe_allow_html=True)
    grade_data = pd.DataFrame({
        'grade': ['副理', '專員', '助理', '實習生'],
        'count': [8, 35, 78, 12]
    })
    fig = px.bar(grade_data, x='grade', y='count',
                color_discrete_sequence=[COLORS['hr']])
    fig.update_layout(**get_chart_layout("", 320))
    st.plotly_chart(fig, use_container_width=True)

    # 接班風險表
    st.markdown("<h4>接班風險交叉分析</h4>", unsafe_allow_html=True)
    succession_data = {
        '部門': ['生產部', '品保部', '供應鏈部', '業務部', '研發部'],
        '經理級以上平均年齡': ['54 歲', '49 歲', '51 歲', '47 歲', '52 歲'],
        '次階梯(副理)人數': ['2 人', '4 人', '3 人', '5 人', '2 人'],
        '風險等級': ['high', 'mid', 'mid', 'low', 'mid']
    }

    risk_html = """<table class="data-table">
      <thead>
        <tr>
          <th>部門</th>
          <th>經理級以上平均年齡</th>
          <th>次階梯(副理)人數</th>
          <th>風險等級</th>
        </tr>
      </thead>
      <tbody>
    """

    for dept, age, ladder, risk in zip(succession_data['部門'], succession_data['經理級以上平均年齡'],
                                       succession_data['次階梯(副理)人數'], succession_data['風險等級']):
        risk_class = 'high' if risk == 'high' else 'mid' if risk == 'mid' else 'low'
        risk_label = '高' if risk == 'high' else '中' if risk == 'mid' else '低'
        risk_html += f"""
        <tr>
          <td>{dept}</td>
          <td class="strong">{age}</td>
          <td class="strong">{ladder}</td>
          <td><span class="risk-badge {risk_class}">{risk_label}</span></td>
        </tr>
        """

    risk_html += """</tbody></table>"""
    st.markdown(risk_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="footnote">
      ＊模擬資料，僅供分析架構展示
    </div>
    """, unsafe_allow_html=True)

def render_finance():
    """財務頁面"""
    st.markdown("""
    <div class="section-head">
      <h2 class="section-title" style="color: #4FBD84;">財務指標</h2>
      <span class="section-sub">FINANCIAL PERFORMANCE &amp; HEALTH</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(6)
    kpis_fin = [
        ("毛利率", "38.4%", "較上季 +1.2pt", True),
        ("淨利率", "18.5%", "較上季 -0.3pt", False),
        ("營業利益率", "11.4%", "較上季 +0.8pt", True),
        ("流動比率", "149%", "較上季 -22pt", False),
        ("負債比率", "53%", "較上季 +2pt", False),
        ("應收帳款天數", "58天", "較上季 +4天", False),
    ]

    for col, (lbl, val, sub, is_up) in zip(cols, kpis_fin):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent: var(--finance);">
              <div class="lbl">{lbl}</div>
              <div class="val">{val}</div>
              <div class="sub {'up' if is_up else 'down'}">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sql = """
        SELECT dd.date, SUM(ff.revenue) as revenue
        FROM fact_finance ff
        JOIN dim_date dd ON ff.finance_month_id = dd.date_id
        GROUP BY dd.date
        ORDER BY dd.date DESC
        LIMIT 12
        """
        data = query_database(sql)
        if data is not None and len(data) > 0:
            data = data.sort_values('date')
            fig = px.line(data, x='date', y='revenue',
                         labels={'revenue': '營收', 'date': '月份'})
            fig.update_traces(
                line=dict(color=COLORS['finance'], width=3),
                fill='tozeroy',
                fillcolor=f"rgba(79, 189, 132, 0.12)"
            )
            fig.update_layout(**get_chart_layout("月度營收 vs 目標", 340))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        sql = """
        SELECT dd.date,
               SUM(ff.gross_profit) as gross,
               SUM(ff.net_profit) as net
        FROM fact_finance ff
        JOIN dim_date dd ON ff.finance_month_id = dd.date_id
        GROUP BY dd.date
        ORDER BY dd.date DESC
        LIMIT 12
        """
        data = query_database(sql)
        if data is not None and len(data) > 0:
            data = data.sort_values('date')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['date'], y=data['gross'],
                mode='lines+markers', name='毛利',
                line=dict(color=COLORS['finance'], width=3),
                marker=dict(size=5),
                fill='tozeroy',
                fillcolor=f"rgba(79, 189, 132, 0.12)"
            ))
            fig.add_trace(go.Scatter(
                x=data['date'], y=data['net'],
                mode='lines+markers', name='淨利',
                line=dict(color='#6FD4D1', width=3),
                marker=dict(size=5)
            ))
            fig.update_layout(**get_chart_layout("毛利 vs 淨利", 340))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="footnote">
      ＊模擬資料，僅供分析架構展示
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 主應用
# ============================================================

def main():
    """主應用"""
    render_header()

    if st.session_state.active_tab == "overview":
        render_overview()
    elif st.session_state.active_tab == "sales":
        render_sales()
    elif st.session_state.active_tab == "production":
        render_production()
    elif st.session_state.active_tab == "hr":
        render_hr()
    elif st.session_state.active_tab == "finance":
        render_finance()

if __name__ == "__main__":
    main()

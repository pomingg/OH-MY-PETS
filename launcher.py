#!/usr/bin/env python3
"""
OH-Pets Company BI Dashboard - 一鍵啟動器
自動完成所有設置並啟動 Streamlit 應用
"""

import subprocess
import sys
import os

def print_header(text):
    """列印標題"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(cmd, description):
    """執行命令並報告結果"""
    print(f"[*] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} 成功\n")
            return True
        else:
            print(f"✗ {description} 失敗")
            print(f"  錯誤: {result.stderr}\n")
            return False
    except Exception as e:
        print(f"✗ {description} 失敗: {e}\n")
        return False

def main():
    print_header("OH-Pets Company BI Dashboard - 一鍵啟動")

    # 變更到專案目錄
    project_path = r"D:\AI agents\OH-Pets company"
    os.chdir(project_path)

    # Step 1: 安裝依賴
    print("[1/5] 安裝 Python 依賴...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "streamlit", "psycopg2-binary", "pandas", "numpy", "plotly"],
        capture_output=True
    )
    print("✓ Python 依賴已安裝\n")

    # Step 2: 檢查 PostgreSQL
    print("[2/5] 檢查 PostgreSQL 連接...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='oh_pets_company',
            user='postgres',
            password='postgres123!@#'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dim_date")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✓ PostgreSQL 連接成功 ({count} 筆日期記錄)\n")
    except Exception as e:
        print(f"✗ PostgreSQL 連接失敗: {e}")
        print("  請確認 PostgreSQL 正在運行\n")
        input("按 Enter 繼續...")
        return

    # Step 3: 檢查 Streamlit
    print("[3/5] 檢查 Streamlit...")
    try:
        import streamlit
        print(f"✓ Streamlit 已安裝\n")
    except ImportError:
        print("✗ Streamlit 安裝失敗\n")
        input("按 Enter 繼續...")
        return

    # Step 4: 檢查應用檔案
    print("[4/5] 檢查應用檔案...")
    if os.path.exists("app.py"):
        print("✓ app.py 已找到\n")
    else:
        print("✗ app.py 未找到\n")
        input("按 Enter 繼續...")
        return

    # Step 5: 啟動應用
    print_header("準備啟動 Streamlit 應用")
    print("📊 應用地址: http://localhost:8501")
    print("🔴 按 Ctrl+C 停止應用")
    print("=" * 60 + "\n")

    # 啟動 Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--logger.level=warning"
    ])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n應用已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 錯誤: {e}")
        sys.exit(1)

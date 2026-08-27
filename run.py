"""
OH-Pets Company BI Dashboard - 完整啟動器
自動安裝依賴、啟動 Flask 後端、打開瀏覽器
"""

import subprocess
import sys
import time
import webbrowser
import os
import signal

def print_banner():
    """列印啟動標題"""
    print("\n" + "=" * 70)
    print("  🐾 毛孩生活科技 | 企業戰情中心 - 完整 HTML 版本")
    print("  OH-Pets Company BI Dashboard")
    print("=" * 70 + "\n")

def install_dependencies():
    """安裝 Python 依賴"""
    print("[1/4] 安裝 Python 依賴...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
            check=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        print("✓ 依賴已安裝\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 安裝失敗: {e}\n")
        return False

def check_database():
    """檢查資料庫連接"""
    print("[2/4] 檢查資料庫連接...")
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
        print(f"✓ 資料庫連接成功 ({count} 筆日期記錄)\n")
        return True
    except Exception as e:
        print(f"✗ 資料庫連接失敗: {e}")
        print("  請確認 PostgreSQL 正在運行\n")
        return False

def start_backend():
    """啟動 Flask 後端"""
    print("[3/4] 啟動 Flask 後端...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "backend.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # 等待後端啟動
        print("✓ Flask 後端已啟動 (http://127.0.0.1:5000)\n")
        return backend_process
    except Exception as e:
        print(f"✗ 啟動失敗: {e}\n")
        return None

def open_browser():
    """打開瀏覽器"""
    print("[4/4] 打開瀏覽器...")
    try:
        html_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "index.html"
        )
        webbrowser.open(f"file:///{html_path}")
        print("✓ 瀏覽器已打開\n")
        return True
    except Exception as e:
        print(f"✗ 打開失敗: {e}")
        print(f"  請手動打開: {html_path}\n")
        return False

def main():
    """主程式"""
    print_banner()

    # 安裝依賴
    if not install_dependencies():
        print("無法繼續，請檢查網路連接")
        sys.exit(1)

    # 檢查資料庫
    if not check_database():
        print("無法繼續，請啟動 PostgreSQL")
        sys.exit(1)

    # 啟動後端
    backend_process = start_backend()
    if not backend_process:
        print("無法繼續，無法啟動後端")
        sys.exit(1)

    # 打開瀏覽器
    open_browser()

    print("=" * 70)
    print("✓ 戰情中心已啟動！")
    print("  • 前端: 請參考打開的瀏覽器視窗")
    print("  • 後端: http://127.0.0.1:5000")
    print("  • 按 Ctrl+C 停止")
    print("=" * 70 + "\n")

    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n正在停止...")
        backend_process.terminate()
        backend_process.wait()
        print("✓ 已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()

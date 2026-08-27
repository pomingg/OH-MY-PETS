"""
OH-Pets Company BI Dashboard - Flask Backend API
提供数据接口给前端
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# 資料庫配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'oh_pets_company',
    'user': 'postgres',
    'password': 'postgres123!@#'
}

# ============================================================
# 資料庫連接
# ============================================================

def get_db_connection():
    """建立資料庫連接"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        return None

def query_database(sql):
    """執行查詢"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"查詢失敗: {e}")
            return None
    return None

# ============================================================
# API 端點
# ============================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# ========== 總覽頁數據 ==========

@app.route('/api/overview/kpis', methods=['GET'])
def overview_kpis():
    """總覽頁 KPI"""
    results = {}

    # 銷售營收
    sales_sql = "SELECT COALESCE(SUM(order_amount), 0) as total FROM fact_orders"
    sales = query_database(sales_sql)
    results['sales'] = float(sales[0]['total']) if sales else 0

    # 生產良率
    yield_sql = "SELECT COALESCE(AVG(yield_rate), 0) as avg_yield FROM fact_production WHERE yield_rate > 0"
    yield_data = query_database(yield_sql)
    results['yield_rate'] = float(yield_data[0]['avg_yield']) if yield_data else 0

    # 在職人數
    emp_sql = "SELECT COUNT(*) as count FROM dim_employee WHERE is_active = TRUE"
    emp = query_database(emp_sql)
    results['employee_count'] = int(emp[0]['count']) if emp else 0

    # 財務總收入
    finance_sql = "SELECT COALESCE(SUM(revenue), 0) as total_rev FROM fact_finance"
    finance = query_database(finance_sql)
    results['finance_revenue'] = float(finance[0]['total_rev']) if finance else 0

    return jsonify(results)

@app.route('/api/overview/trend', methods=['GET'])
def overview_trend():
    """訂單趨勢（最近 30 天）"""
    sql = """
    SELECT dd.date, COUNT(*) as order_count
    FROM fact_orders fo
    JOIN dim_date dd ON fo.order_date_id = dd.date_id
    WHERE dd.date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY dd.date
    ORDER BY dd.date
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'dates': [item['date'].isoformat() for item in data],
            'orders': [int(item['order_count']) for item in data]
        })
    return jsonify({'dates': [], 'orders': []})

@app.route('/api/overview/sales-dist', methods=['GET'])
def overview_sales_dist():
    """銷售分布（按產品線）"""
    sql = """
    SELECT dp.product_line, COUNT(*) as cnt
    FROM fact_orders fo
    JOIN dim_product dp ON fo.product_id = dp.product_id
    GROUP BY dp.product_line
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'labels': [item['product_line'] for item in data],
            'values': [int(item['cnt']) for item in data]
        })
    return jsonify({'labels': [], 'values': []})

# ========== 銷售頁數據 ==========

@app.route('/api/sales/product-line', methods=['GET'])
def sales_product_line():
    """銷售按產品線"""
    sql = """
    SELECT dp.product_line, COUNT(*) as cnt
    FROM fact_orders fo
    JOIN dim_product dp ON fo.product_id = dp.product_id
    GROUP BY dp.product_line
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'labels': [item['product_line'] for item in data],
            'values': [int(item['cnt']) for item in data]
        })
    return jsonify({'labels': [], 'values': []})

@app.route('/api/sales/revenue-dist', methods=['GET'])
def sales_revenue_dist():
    """營收分布（按產品線）"""
    sql = """
    SELECT dp.product_line, SUM(fo.order_amount) as amt
    FROM fact_orders fo
    JOIN dim_product dp ON fo.product_id = dp.product_id
    GROUP BY dp.product_line
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'labels': [item['product_line'] for item in data],
            'values': [float(item['amt']) for item in data]
        })
    return jsonify({'labels': [], 'values': []})

# ========== 生產頁數據 ==========

@app.route('/api/production/yield-by-plant', methods=['GET'])
def production_yield_by_plant():
    """廠區良率"""
    sql = """
    SELECT dp.plant_name, AVG(fp.yield_rate) as yield
    FROM fact_production fp
    JOIN dim_plant dp ON fp.plant_id = dp.plant_id
    WHERE fp.yield_rate > 0
    GROUP BY dp.plant_id, dp.plant_name
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'labels': [item['plant_name'] for item in data],
            'values': [round(float(item['yield']), 2) for item in data]
        })
    return jsonify({'labels': [], 'values': []})

@app.route('/api/production/util-by-plant', methods=['GET'])
def production_util_by_plant():
    """廠區稼動率"""
    sql = """
    SELECT dp.plant_name, AVG(fp.equipment_utilization_rate) as util
    FROM fact_production fp
    JOIN dim_plant dp ON fp.plant_id = dp.plant_id
    WHERE fp.equipment_utilization_rate > 0
    GROUP BY dp.plant_id, dp.plant_name
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'labels': [item['plant_name'] for item in data],
            'values': [round(float(item['util']), 2) for item in data]
        })
    return jsonify({'labels': [], 'values': []})

# ========== 人資頁數據 ==========

@app.route('/api/hr/dept-distribution', methods=['GET'])
def hr_dept_distribution():
    """部門人數分布"""
    sql = """
    SELECT dd.department_name, COUNT(*) as cnt
    FROM dim_employee de
    JOIN dim_department dd ON de.department_id = dd.department_id
    WHERE de.is_active = TRUE
    GROUP BY dd.department_id, dd.department_name
    ORDER BY cnt DESC
    """
    data = query_database(sql)

    if data:
        return jsonify({
            'labels': [item['department_name'] for item in data],
            'values': [int(item['cnt']) for item in data]
        })
    return jsonify({'labels': [], 'values': []})

# ========== 財務頁數據 ==========

@app.route('/api/finance/monthly-revenue', methods=['GET'])
def finance_monthly_revenue():
    """月度營收"""
    sql = """
    SELECT dd.date, SUM(ff.revenue) as revenue
    FROM fact_finance ff
    JOIN dim_date dd ON ff.finance_month_id = dd.date_id
    GROUP BY dd.date
    ORDER BY dd.date DESC
    LIMIT 12
    """
    data = query_database(sql)

    if data:
        sorted_data = sorted(data, key=lambda x: x['date'])
        return jsonify({
            'dates': [str(item['date']) for item in sorted_data],
            'values': [float(item['revenue']) for item in sorted_data]
        })
    return jsonify({'dates': [], 'values': []})

@app.route('/api/finance/profit-trend', methods=['GET'])
def finance_profit_trend():
    """毛利 vs 淨利"""
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

    if data:
        sorted_data = sorted(data, key=lambda x: x['date'])
        return jsonify({
            'dates': [str(item['date']) for item in sorted_data],
            'gross': [float(item['gross']) for item in sorted_data],
            'net': [float(item['net']) for item in sorted_data]
        })
    return jsonify({'dates': [], 'gross': [], 'net': []})

# ============================================================
# 啟動
# ============================================================

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

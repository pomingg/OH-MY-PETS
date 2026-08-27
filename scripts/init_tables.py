#!/usr/bin/env python3
"""Initialize database tables directly with Python"""

import psycopg2
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DB_CONFIG

def create_tables():
    """Create all required tables"""

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    tables = {
        'dim_date': '''
            CREATE TABLE IF NOT EXISTS dim_date (
                date_id INT PRIMARY KEY,
                date DATE NOT NULL UNIQUE,
                year INT, quarter INT, month INT, day INT, week INT, day_of_week INT,
                day_name VARCHAR(10), is_weekend BOOLEAN, is_holiday BOOLEAN,
                is_business_day BOOLEAN, season VARCHAR(20), pet_industry_peak_season BOOLEAN
            )
        ''',
        'dim_plant': '''
            CREATE TABLE IF NOT EXISTS dim_plant (
                plant_id INT PRIMARY KEY,
                plant_code VARCHAR(10) UNIQUE, plant_name VARCHAR(100),
                plant_type VARCHAR(50), location VARCHAR(100),
                established_date DATE, capacity_units_per_month INT,
                manager_name VARCHAR(100), phone VARCHAR(20), email VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE
            )
        ''',
        'dim_product': '''
            CREATE TABLE IF NOT EXISTS dim_product (
                product_id INT PRIMARY KEY,
                product_code VARCHAR(20) UNIQUE, product_name VARCHAR(200),
                product_line VARCHAR(50), category VARCHAR(50),
                unit_cost NUMERIC(10,2), suggested_price NUMERIC(10,2),
                launch_date DATE, main_material VARCHAR(100),
                supplier_id INT, is_active BOOLEAN DEFAULT TRUE,
                created_date DATE, discontinued_date DATE
            )
        ''',
        'dim_channel': '''
            CREATE TABLE IF NOT EXISTS dim_channel (
                channel_id INT PRIMARY KEY,
                channel_code VARCHAR(20) UNIQUE, channel_name VARCHAR(100),
                channel_type VARCHAR(50), description VARCHAR(500),
                is_active BOOLEAN DEFAULT TRUE
            )
        ''',
        'dim_dealer': '''
            CREATE TABLE IF NOT EXISTS dim_dealer (
                dealer_id INT PRIMARY KEY,
                dealer_code VARCHAR(20) UNIQUE, dealer_name VARCHAR(200),
                channel_id INT, region VARCHAR(100),
                established_date DATE, cooperation_start_date DATE,
                payment_terms_days INT, credit_limit NUMERIC(15,2),
                contact_person VARCHAR(100), phone VARCHAR(20), email VARCHAR(100),
                address VARCHAR(300), is_active BOOLEAN DEFAULT TRUE
            )
        ''',
        'dim_supplier': '''
            CREATE TABLE IF NOT EXISTS dim_supplier (
                supplier_id INT PRIMARY KEY,
                supplier_code VARCHAR(20) UNIQUE, supplier_name VARCHAR(200),
                location VARCHAR(100), established_date DATE,
                cooperation_start_date DATE, payment_terms_days INT,
                lead_time_days INT, contact_person VARCHAR(100),
                phone VARCHAR(20), email VARCHAR(100), is_active BOOLEAN DEFAULT TRUE
            )
        ''',
        'dim_department': '''
            CREATE TABLE IF NOT EXISTS dim_department (
                department_id INT PRIMARY KEY,
                department_code VARCHAR(20) UNIQUE, department_name VARCHAR(100),
                description VARCHAR(500), parent_department_id INT,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''',
        'dim_employee_type': '''
            CREATE TABLE IF NOT EXISTS dim_employee_type (
                employee_type_id INT PRIMARY KEY,
                employee_type_code VARCHAR(20) UNIQUE, employee_type_name VARCHAR(100),
                description VARCHAR(500)
            )
        ''',
        'dim_employee': '''
            CREATE TABLE IF NOT EXISTS dim_employee (
                employee_id INT PRIMARY KEY,
                employee_code VARCHAR(20) UNIQUE, employee_name VARCHAR(100),
                department_id INT, employee_type_id INT, job_grade VARCHAR(50),
                birth_date DATE, hire_date DATE, termination_date DATE,
                is_active BOOLEAN DEFAULT TRUE, salary NUMERIC(12,2),
                manager_id INT, created_date DATE, updated_date DATE
            )
        ''',
        'fact_orders': '''
            CREATE TABLE IF NOT EXISTS fact_orders (
                order_id BIGINT PRIMARY KEY,
                order_date_id INT, product_id INT, dealer_id INT,
                channel_id INT, plant_id INT, order_quantity INT,
                unit_price NUMERIC(10,2), order_amount NUMERIC(15,2),
                promised_ship_date DATE, actual_ship_date DATE,
                payment_status VARCHAR(50), payment_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_sales_return': '''
            CREATE TABLE IF NOT EXISTS fact_sales_return (
                return_id BIGINT PRIMARY KEY,
                order_id BIGINT, return_date_id INT, product_id INT,
                dealer_id INT, return_quantity INT, return_reason VARCHAR(200),
                return_amount NUMERIC(15,2), refund_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_production': '''
            CREATE TABLE IF NOT EXISTS fact_production (
                production_id BIGINT PRIMARY KEY,
                production_date_id INT, plant_id INT, product_id INT,
                planned_quantity INT, actual_quantity INT, good_quantity INT,
                defective_quantity INT, yield_rate NUMERIC(5,2),
                equipment_utilization_rate NUMERIC(5,2), downtime_minutes INT,
                downtime_reason VARCHAR(200), shift VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_inventory': '''
            CREATE TABLE IF NOT EXISTS fact_inventory (
                inventory_id BIGINT PRIMARY KEY,
                inventory_date_id INT, plant_id INT, product_id INT,
                beginning_balance INT, inbound_quantity INT, outbound_quantity INT,
                ending_balance INT, days_in_stock INT, is_slow_moving BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_supplier_delivery': '''
            CREATE TABLE IF NOT EXISTS fact_supplier_delivery (
                delivery_id BIGINT PRIMARY KEY,
                delivery_date_id INT, supplier_id INT, product_id INT,
                plant_id INT, ordered_quantity INT, delivered_quantity INT,
                inspection_pass_quantity INT, inspection_fail_quantity INT,
                on_time BOOLEAN, promised_date DATE, actual_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_hr_headcount': '''
            CREATE TABLE IF NOT EXISTS fact_hr_headcount (
                headcount_id BIGINT PRIMARY KEY,
                headcount_date_id INT, department_id INT, employee_type_id INT,
                active_headcount INT, new_hire_count INT, termination_count INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_hr_attendance': '''
            CREATE TABLE IF NOT EXISTS fact_hr_attendance (
                attendance_id BIGINT PRIMARY KEY,
                attendance_date_id INT, employee_id INT, attendance_status VARCHAR(50),
                hours_worked NUMERIC(5,2), overtime_hours NUMERIC(5,2),
                is_present BOOLEAN, is_on_time BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_hr_cost': '''
            CREATE TABLE IF NOT EXISTS fact_hr_cost (
                cost_id BIGINT PRIMARY KEY,
                cost_month_id INT, department_id INT,
                base_salary NUMERIC(15,2), bonus NUMERIC(15,2),
                overtime_pay NUMERIC(15,2), benefits NUMERIC(15,2),
                total_cost NUMERIC(15,2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_safety': '''
            CREATE TABLE IF NOT EXISTS fact_safety (
                safety_id BIGINT PRIMARY KEY,
                incident_date_id INT, plant_id INT, department_id INT,
                employee_id INT, incident_type VARCHAR(100), severity VARCHAR(50),
                description VARCHAR(500), days_lost INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_finance': '''
            CREATE TABLE IF NOT EXISTS fact_finance (
                finance_id BIGINT PRIMARY KEY,
                finance_month_id INT, plant_id INT,
                revenue NUMERIC(15,2), cost_of_goods_sold NUMERIC(15,2),
                gross_profit NUMERIC(15,2), operating_expenses NUMERIC(15,2),
                operating_profit NUMERIC(15,2), other_income NUMERIC(15,2),
                other_expenses NUMERIC(15,2), net_profit NUMERIC(15,2),
                budget_revenue NUMERIC(15,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_ar_ap': '''
            CREATE TABLE IF NOT EXISTS fact_ar_ap (
                ar_ap_id BIGINT PRIMARY KEY,
                ar_ap_date_id INT, dealer_id INT, supplier_id INT,
                ar_ap_type VARCHAR(50), invoice_amount NUMERIC(15,2),
                paid_amount NUMERIC(15,2), outstanding_amount NUMERIC(15,2),
                days_overdue INT, due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'fact_balance_sheet': '''
            CREATE TABLE IF NOT EXISTS fact_balance_sheet (
                bs_id BIGINT PRIMARY KEY,
                bs_month_id INT, current_assets NUMERIC(15,2),
                fixed_assets NUMERIC(15,2), total_assets NUMERIC(15,2),
                current_liabilities NUMERIC(15,2), long_term_liabilities NUMERIC(15,2),
                total_liabilities NUMERIC(15,2), shareholders_equity NUMERIC(15,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
    }

    print("Creating tables...")
    for table_name, sql in tables.items():
        try:
            cursor.execute(sql)
            conn.commit()
            print(f"✓ {table_name}")
        except Exception as e:
            print(f"✗ {table_name}: {e}")
            conn.rollback()

    # Create indexes
    print("\nCreating indexes...")
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_orders_date ON fact_orders(order_date_id);",
        "CREATE INDEX IF NOT EXISTS idx_orders_product ON fact_orders(product_id);",
        "CREATE INDEX IF NOT EXISTS idx_orders_dealer ON fact_orders(dealer_id);",
        "CREATE INDEX IF NOT EXISTS idx_orders_plant ON fact_orders(plant_id);",
        "CREATE INDEX IF NOT EXISTS idx_production_date ON fact_production(production_date_id);",
        "CREATE INDEX IF NOT EXISTS idx_inventory_date ON fact_inventory(inventory_date_id);",
        "CREATE INDEX IF NOT EXISTS idx_attendance_date ON fact_hr_attendance(attendance_date_id);",
        "CREATE INDEX IF NOT EXISTS idx_finance_date ON fact_finance(finance_month_id);",
        "CREATE INDEX IF NOT EXISTS idx_date ON dim_date(date);",
    ]

    for idx_sql in indexes:
        try:
            cursor.execute(idx_sql)
            conn.commit()
        except:
            pass

    cursor.close()
    conn.close()
    print("\n✓ All tables created successfully")

if __name__ == '__main__':
    try:
        create_tables()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

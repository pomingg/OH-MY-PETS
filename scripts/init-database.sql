-- ============================================================
-- OH-Pets Company BI Database Initialization Script
-- PostgreSQL 16
-- ============================================================

-- 建立資料庫
CREATE DATABASE oh_pets_company
  ENCODING 'UTF8'
  LOCALE 'C'
  TEMPLATE template0;

-- 連接到新資料庫（需在單獨連接中執行）
-- \c oh_pets_company

-- ============================================================
-- 維度表 (Dimension Tables)
-- ============================================================

-- 日期維度表
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  date DATE NOT NULL UNIQUE,
  year INT NOT NULL,
  quarter INT NOT NULL,
  month INT NOT NULL,
  day INT NOT NULL,
  week INT NOT NULL,
  day_of_week INT NOT NULL,
  day_name VARCHAR(10),
  is_weekend BOOLEAN,
  is_holiday BOOLEAN,
  is_business_day BOOLEAN,
  season VARCHAR(20),
  pet_industry_peak_season BOOLEAN,
  CONSTRAINT valid_quarter CHECK (quarter BETWEEN 1 AND 4),
  CONSTRAINT valid_month CHECK (month BETWEEN 1 AND 12),
  CONSTRAINT valid_day CHECK (day BETWEEN 1 AND 31),
  CONSTRAINT valid_week CHECK (week BETWEEN 1 AND 53)
);

-- 廠區維度表
CREATE TABLE dim_plant (
  plant_id INT PRIMARY KEY,
  plant_code VARCHAR(10) NOT NULL UNIQUE,
  plant_name VARCHAR(100) NOT NULL,
  plant_type VARCHAR(50),
  location VARCHAR(100),
  established_date DATE,
  capacity_units_per_month INT,
  manager_name VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100),
  is_active BOOLEAN DEFAULT TRUE
);

-- 產品維度表
CREATE TABLE dim_product (
  product_id INT PRIMARY KEY,
  product_code VARCHAR(20) NOT NULL UNIQUE,
  product_name VARCHAR(200) NOT NULL,
  product_line VARCHAR(50) NOT NULL,
  category VARCHAR(50),
  unit_cost NUMERIC(10, 2),
  suggested_price NUMERIC(10, 2),
  launch_date DATE,
  main_material VARCHAR(100),
  supplier_id INT,
  is_active BOOLEAN DEFAULT TRUE,
  created_date DATE,
  discontinued_date DATE
);

-- 通路維度表
CREATE TABLE dim_channel (
  channel_id INT PRIMARY KEY,
  channel_code VARCHAR(20) NOT NULL UNIQUE,
  channel_name VARCHAR(100) NOT NULL,
  channel_type VARCHAR(50),
  description VARCHAR(500),
  is_active BOOLEAN DEFAULT TRUE
);

-- 經銷商維度表
CREATE TABLE dim_dealer (
  dealer_id INT PRIMARY KEY,
  dealer_code VARCHAR(20) NOT NULL UNIQUE,
  dealer_name VARCHAR(200) NOT NULL,
  channel_id INT NOT NULL,
  region VARCHAR(100),
  established_date DATE,
  cooperation_start_date DATE,
  payment_terms_days INT,
  credit_limit NUMERIC(15, 2),
  contact_person VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100),
  address VARCHAR(300),
  is_active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id)
);

-- 供應商維度表
CREATE TABLE dim_supplier (
  supplier_id INT PRIMARY KEY,
  supplier_code VARCHAR(20) NOT NULL UNIQUE,
  supplier_name VARCHAR(200) NOT NULL,
  location VARCHAR(100),
  established_date DATE,
  cooperation_start_date DATE,
  payment_terms_days INT,
  lead_time_days INT,
  contact_person VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100),
  is_active BOOLEAN DEFAULT TRUE
);

-- 部門維度表
CREATE TABLE dim_department (
  department_id INT PRIMARY KEY,
  department_code VARCHAR(20) NOT NULL UNIQUE,
  department_name VARCHAR(100) NOT NULL,
  description VARCHAR(500),
  parent_department_id INT,
  is_active BOOLEAN DEFAULT TRUE
);

-- 員工類型維度表
CREATE TABLE dim_employee_type (
  employee_type_id INT PRIMARY KEY,
  employee_type_code VARCHAR(20) NOT NULL UNIQUE,
  employee_type_name VARCHAR(100) NOT NULL,
  description VARCHAR(500)
);

-- 員工維度表
CREATE TABLE dim_employee (
  employee_id INT PRIMARY KEY,
  employee_code VARCHAR(20) NOT NULL UNIQUE,
  employee_name VARCHAR(100) NOT NULL,
  department_id INT NOT NULL,
  employee_type_id INT NOT NULL,
  job_grade VARCHAR(50),
  birth_date DATE,
  hire_date DATE,
  termination_date DATE,
  is_active BOOLEAN DEFAULT TRUE,
  salary NUMERIC(12, 2),
  manager_id INT,
  created_date DATE,
  updated_date DATE,
  FOREIGN KEY (department_id) REFERENCES dim_department(department_id),
  FOREIGN KEY (employee_type_id) REFERENCES dim_employee_type(employee_type_id),
  FOREIGN KEY (manager_id) REFERENCES dim_employee(employee_id)
);

-- ============================================================
-- 事實表 (Fact Tables)
-- ============================================================

-- 訂單事實表
CREATE TABLE fact_orders (
  order_id BIGINT PRIMARY KEY,
  order_date_id INT NOT NULL,
  product_id INT NOT NULL,
  dealer_id INT NOT NULL,
  channel_id INT NOT NULL,
  plant_id INT NOT NULL,
  order_quantity INT NOT NULL,
  unit_price NUMERIC(10, 2),
  order_amount NUMERIC(15, 2),
  promised_ship_date DATE,
  actual_ship_date DATE,
  payment_status VARCHAR(50),
  payment_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (dealer_id) REFERENCES dim_dealer(dealer_id),
  FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id),
  FOREIGN KEY (plant_id) REFERENCES dim_plant(plant_id)
);

-- 銷售退貨事實表
CREATE TABLE fact_sales_return (
  return_id BIGINT PRIMARY KEY,
  order_id BIGINT NOT NULL,
  return_date_id INT NOT NULL,
  product_id INT NOT NULL,
  dealer_id INT NOT NULL,
  return_quantity INT NOT NULL,
  return_reason VARCHAR(200),
  return_amount NUMERIC(15, 2),
  refund_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES fact_orders(order_id),
  FOREIGN KEY (return_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (dealer_id) REFERENCES dim_dealer(dealer_id)
);

-- 生產事實表
CREATE TABLE fact_production (
  production_id BIGINT PRIMARY KEY,
  production_date_id INT NOT NULL,
  plant_id INT NOT NULL,
  product_id INT NOT NULL,
  planned_quantity INT,
  actual_quantity INT,
  good_quantity INT,
  defective_quantity INT,
  yield_rate NUMERIC(5, 2),
  equipment_utilization_rate NUMERIC(5, 2),
  downtime_minutes INT,
  downtime_reason VARCHAR(200),
  shift VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (production_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (plant_id) REFERENCES dim_plant(plant_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

-- 庫存事實表
CREATE TABLE fact_inventory (
  inventory_id BIGINT PRIMARY KEY,
  inventory_date_id INT NOT NULL,
  plant_id INT NOT NULL,
  product_id INT NOT NULL,
  beginning_balance INT,
  inbound_quantity INT,
  outbound_quantity INT,
  ending_balance INT,
  days_in_stock INT,
  is_slow_moving BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (inventory_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (plant_id) REFERENCES dim_plant(plant_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

-- 供應商交貨事實表
CREATE TABLE fact_supplier_delivery (
  delivery_id BIGINT PRIMARY KEY,
  delivery_date_id INT NOT NULL,
  supplier_id INT NOT NULL,
  product_id INT NOT NULL,
  plant_id INT NOT NULL,
  ordered_quantity INT,
  delivered_quantity INT,
  inspection_pass_quantity INT,
  inspection_fail_quantity INT,
  on_time BOOLEAN,
  promised_date DATE,
  actual_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (delivery_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (plant_id) REFERENCES dim_plant(plant_id)
);

-- 人力資源人數事實表
CREATE TABLE fact_hr_headcount (
  headcount_id BIGINT PRIMARY KEY,
  headcount_date_id INT NOT NULL,
  department_id INT NOT NULL,
  employee_type_id INT NOT NULL,
  active_headcount INT,
  new_hire_count INT,
  termination_count INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (headcount_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (department_id) REFERENCES dim_department(department_id),
  FOREIGN KEY (employee_type_id) REFERENCES dim_employee_type(employee_type_id)
);

-- 出勤事實表
CREATE TABLE fact_hr_attendance (
  attendance_id BIGINT PRIMARY KEY,
  attendance_date_id INT NOT NULL,
  employee_id INT NOT NULL,
  attendance_status VARCHAR(50),
  hours_worked NUMERIC(5, 2),
  overtime_hours NUMERIC(5, 2),
  is_present BOOLEAN,
  is_on_time BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (attendance_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (employee_id) REFERENCES dim_employee(employee_id)
);

-- 人力成本事實表
CREATE TABLE fact_hr_cost (
  cost_id BIGINT PRIMARY KEY,
  cost_month_id INT NOT NULL,
  department_id INT NOT NULL,
  base_salary NUMERIC(15, 2),
  bonus NUMERIC(15, 2),
  overtime_pay NUMERIC(15, 2),
  benefits NUMERIC(15, 2),
  total_cost NUMERIC(15, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cost_month_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (department_id) REFERENCES dim_department(department_id)
);

-- 安全事件事實表
CREATE TABLE fact_safety (
  safety_id BIGINT PRIMARY KEY,
  incident_date_id INT NOT NULL,
  plant_id INT NOT NULL,
  department_id INT NOT NULL,
  employee_id INT,
  incident_type VARCHAR(100),
  severity VARCHAR(50),
  description VARCHAR(500),
  days_lost INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (incident_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (plant_id) REFERENCES dim_plant(plant_id),
  FOREIGN KEY (department_id) REFERENCES dim_department(department_id),
  FOREIGN KEY (employee_id) REFERENCES dim_employee(employee_id)
);

-- 財務事實表（月度損益）
CREATE TABLE fact_finance (
  finance_id BIGINT PRIMARY KEY,
  finance_month_id INT NOT NULL,
  plant_id INT NOT NULL,
  revenue NUMERIC(15, 2),
  cost_of_goods_sold NUMERIC(15, 2),
  gross_profit NUMERIC(15, 2),
  operating_expenses NUMERIC(15, 2),
  operating_profit NUMERIC(15, 2),
  other_income NUMERIC(15, 2),
  other_expenses NUMERIC(15, 2),
  net_profit NUMERIC(15, 2),
  budget_revenue NUMERIC(15, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (finance_month_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (plant_id) REFERENCES dim_plant(plant_id)
);

-- 應收應付事實表
CREATE TABLE fact_ar_ap (
  ar_ap_id BIGINT PRIMARY KEY,
  ar_ap_date_id INT NOT NULL,
  dealer_id INT,
  supplier_id INT,
  ar_ap_type VARCHAR(50),
  invoice_amount NUMERIC(15, 2),
  paid_amount NUMERIC(15, 2),
  outstanding_amount NUMERIC(15, 2),
  days_overdue INT,
  due_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ar_ap_date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (dealer_id) REFERENCES dim_dealer(dealer_id),
  FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id)
);

-- 資產負債表事實表（月度快照）
CREATE TABLE fact_balance_sheet (
  bs_id BIGINT PRIMARY KEY,
  bs_month_id INT NOT NULL,
  current_assets NUMERIC(15, 2),
  fixed_assets NUMERIC(15, 2),
  total_assets NUMERIC(15, 2),
  current_liabilities NUMERIC(15, 2),
  long_term_liabilities NUMERIC(15, 2),
  total_liabilities NUMERIC(15, 2),
  shareholders_equity NUMERIC(15, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bs_month_id) REFERENCES dim_date(date_id)
);

-- ============================================================
-- 建立索引以優化查詢效能
-- ============================================================

CREATE INDEX idx_orders_order_date ON fact_orders(order_date_id);
CREATE INDEX idx_orders_product ON fact_orders(product_id);
CREATE INDEX idx_orders_dealer ON fact_orders(dealer_id);
CREATE INDEX idx_orders_plant ON fact_orders(plant_id);

CREATE INDEX idx_production_date ON fact_production(production_date_id);
CREATE INDEX idx_production_plant ON fact_production(plant_id);
CREATE INDEX idx_production_product ON fact_production(product_id);

CREATE INDEX idx_inventory_date ON fact_inventory(inventory_date_id);
CREATE INDEX idx_inventory_plant ON fact_inventory(plant_id);
CREATE INDEX idx_inventory_product ON fact_inventory(product_id);

CREATE INDEX idx_attendance_date ON fact_hr_attendance(attendance_date_id);
CREATE INDEX idx_attendance_employee ON fact_hr_attendance(employee_id);

CREATE INDEX idx_finance_date ON fact_finance(finance_month_id);
CREATE INDEX idx_finance_plant ON fact_finance(plant_id);

CREATE INDEX idx_date ON dim_date(date);
CREATE INDEX idx_date_year_month ON dim_date(year, month);

-- ============================================================
-- 完成
-- ============================================================

COMMIT;

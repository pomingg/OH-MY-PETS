# Configuration for OH-Pets Company Data Generation
# All data is simulated and does not represent any real company

import os
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'oh_pets_company',
    'user': 'postgres',
    'password': 'postgres123!@#'
}

# Project Configuration
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
SCRIPTS_DIR = os.path.join(PROJECT_DIR, 'scripts')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Data Generation Configuration
DATA_GEN_CONFIG = {
    'start_date': datetime(2023, 1, 1),
    'end_date': datetime.now(),
    'num_plants': 3,
    'num_products': 12,
    'num_dealers': 25,
    'num_suppliers': 15,
    'num_employees': 150,
    'num_departments': 8,
    'monthly_revenue_base': 200_000_000,  # 2億台幣
    'monthly_revenue_variance': 0.15,  # 15% variance
}

# Dirty Data Injection Configuration (intentional for data cleaning demonstration)
DIRTY_DATA_CONFIG = {
    'duplicate_rate': 0.02,  # 2% duplicate records
    'missing_value_rate': 0.05,  # 5% missing values
    'format_inconsistency_rate': 0.03,  # 3% format inconsistencies (full/half-width)
    'type_error_rate': 0.01,  # 1% type errors
    'outlier_rate': 0.02,  # 2% outliers
    'foreign_key_mismatch_rate': 0.01,  # 1% foreign key mismatches
}

# Anomaly Events Configuration (for data quality demonstration)
ANOMALY_EVENTS = {
    'supplier_stockout': {
        'probability_per_month': 0.15,
        'duration_days': 7,
        'affected_products_ratio': 0.3,
        'description': 'Supplier delivery delay'
    },
    'equipment_failure': {
        'probability_per_month': 0.1,
        'duration_days': 2,
        'affected_plants_ratio': 1,
        'description': 'Equipment malfunction'
    },
    'high_season': {
        'probability_per_month': 0.3,
        'duration_days': 30,
        'peak_season_months': [3, 4, 9, 10],  # March, April, September, October
        'revenue_multiplier': 1.4,
        'description': 'Pet industry peak season (holidays, promotions)'
    },
    'employee_turnover': {
        'monthly_turnover_rate': 0.012,  # 1.2% per month
        'description': 'Employee resignation/termination'
    }
}

# Dimensional Data Seeds
PLANTS = [
    {'plant_id': 1, 'plant_code': 'PL001', 'plant_name': 'A廠-主力組裝廠', 'plant_type': 'Assembly', 'location': '台北'},
    {'plant_id': 2, 'plant_code': 'PL002', 'plant_name': 'B廠-零組件廠', 'plant_type': 'Components', 'location': '新竹'},
    {'plant_id': 3, 'plant_code': 'PL003', 'plant_name': 'C廠-衛星廠', 'plant_type': 'Satellite', 'location': '台中'},
]

PRODUCT_LINES = [
    {'product_line_id': 1, 'product_line_name': 'Premium Pet Toys', 'category': 'Toys'},
    {'product_line_id': 2, 'product_line_name': 'Pet Nutrition', 'category': 'Food & Supplements'},
]

CHANNELS = [
    {'channel_id': 1, 'channel_code': 'CH001', 'channel_name': 'E-Commerce DTC', 'channel_type': 'Direct'},
    {'channel_id': 2, 'channel_code': 'CH002', 'channel_name': 'Retail Dealers', 'channel_type': 'Indirect'},
    {'channel_id': 3, 'channel_code': 'CH003', 'channel_name': 'OEM/Contract Manufacturing', 'channel_type': 'B2B'},
]

DEPARTMENTS = [
    {'department_id': 1, 'department_code': 'SALES', 'department_name': '銷售部'},
    {'department_id': 2, 'department_code': 'PROD', 'department_name': '生產部'},
    {'department_id': 3, 'department_code': 'QC', 'department_name': '品保部'},
    {'department_id': 4, 'department_code': 'HR', 'department_name': '人力資源部'},
    {'department_id': 5, 'department_code': 'FIN', 'department_name': '財務部'},
    {'department_id': 6, 'department_code': 'LOG', 'department_name': '物流部'},
    {'department_id': 7, 'department_code': 'IT', 'department_name': '資訊部'},
    {'department_id': 8, 'department_code': 'MGT', 'department_name': '主管級'},
]

EMPLOYEE_TYPES = [
    {'employee_type_id': 1, 'employee_type_code': 'FT', 'employee_type_name': 'Full-Time'},
    {'employee_type_id': 2, 'employee_type_code': 'PT', 'employee_type_name': 'Part-Time'},
    {'employee_type_id': 3, 'employee_type_code': 'CT', 'employee_type_name': 'Contract'},
]

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Data Quality Report Configuration
QUALITY_REPORT_CONFIG = {
    'include_before_after_comparison': True,
    'include_dirty_data_samples': True,
    'include_cleaning_rules_documentation': True,
}

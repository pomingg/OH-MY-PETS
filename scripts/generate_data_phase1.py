#!/usr/bin/env python3
"""
OH-Pets Company Data Generation - Phase 1: Historical Backfill
Generates data from 2023-01-01 to present date
Intentionally injects dirty data for data quality demonstration

WARNING: This script deliberately introduces data quality issues.
These are NOT bugs, but required for demonstrating data cleaning capabilities.
See data_cleaning.py for the ETL pipeline that resolves these issues.
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import random
import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DB_CONFIG, DATA_GEN_CONFIG, DIRTY_DATA_CONFIG, ANOMALY_EVENTS
from config import PLANTS, CHANNELS, DEPARTMENTS, EMPLOYEE_TYPES, PRODUCT_LINES
from config import LOGS_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'data_generation.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataGenerator:
    """Generate historical data for OH-Pets Company database"""

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.start_date = DATA_GEN_CONFIG['start_date']
        self.end_date = DATA_GEN_CONFIG['end_date']
        self.dirty_records = []

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed")

    def generate_date_dimension(self):
        """Generate dim_date table with calendar information"""
        logger.info("Generating dim_date table...")

        current_date = self.start_date
        records = []
        date_id = 1

        while current_date <= self.end_date:
            is_weekend = current_date.weekday() >= 5
            is_holiday = current_date.month == 1 and current_date.day == 1  # Simple: just New Year
            is_business_day = not is_weekend and not is_holiday

            # Determine season
            month = current_date.month
            if month in [12, 1, 2]:
                season = 'Winter'
            elif month in [3, 4, 5]:
                season = 'Spring'
            elif month in [6, 7, 8]:
                season = 'Summer'
            else:
                season = 'Fall'

            # Peak season for pet industry (March-April, Sept-Oct)
            pet_industry_peak = month in [3, 4, 9, 10]

            records.append({
                'date_id': date_id,
                'date': current_date,
                'year': current_date.year,
                'quarter': (current_date.month - 1) // 3 + 1,
                'month': current_date.month,
                'day': current_date.day,
                'week': current_date.isocalendar()[1],
                'day_of_week': current_date.weekday(),
                'day_name': current_date.strftime('%A'),
                'is_weekend': is_weekend,
                'is_holiday': is_holiday,
                'is_business_day': is_business_day,
                'season': season,
                'pet_industry_peak_season': pet_industry_peak
            })

            current_date += timedelta(days=1)
            date_id += 1

        # Insert into database
        for record in records:
            try:
                self.cursor.execute("""
                    INSERT INTO dim_date
                    (date_id, date, year, quarter, month, day, week, day_of_week,
                     day_name, is_weekend, is_holiday, is_business_day, season, pet_industry_peak_season)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    record['date_id'], record['date'], record['year'], record['quarter'],
                    record['month'], record['day'], record['week'], record['day_of_week'],
                    record['day_name'], record['is_weekend'], record['is_holiday'],
                    record['is_business_day'], record['season'], record['pet_industry_peak_season']
                ))
            except psycopg2.errors.UniqueViolation:
                self.conn.rollback()
                continue
            except Exception as e:
                logger.error(f"Error inserting date record: {e}")
                self.conn.rollback()
                continue

        self.conn.commit()
        logger.info(f"Generated {len(records)} date records")

    def generate_dimension_data(self):
        """Generate all dimension tables"""
        logger.info("Generating dimension tables...")

        # Plants
        for plant in PLANTS:
            self.cursor.execute("""
                INSERT INTO dim_plant (plant_id, plant_code, plant_name, plant_type, location)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (plant['plant_id'], plant['plant_code'], plant['plant_name'],
                  plant['plant_type'], plant['location']))

        # Channels
        for channel in CHANNELS:
            self.cursor.execute("""
                INSERT INTO dim_channel (channel_id, channel_code, channel_name, channel_type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (channel['channel_id'], channel['channel_code'], channel['channel_name'],
                  channel['channel_type']))

        # Departments
        for dept in DEPARTMENTS:
            self.cursor.execute("""
                INSERT INTO dim_department (department_id, department_code, department_name)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (dept['department_id'], dept['department_code'], dept['department_name']))

        # Employee Types
        for emp_type in EMPLOYEE_TYPES:
            self.cursor.execute("""
                INSERT INTO dim_employee_type (employee_type_id, employee_type_code, employee_type_name)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (emp_type['employee_type_id'], emp_type['employee_type_code'],
                  emp_type['employee_type_name']))

        self.conn.commit()
        logger.info("Dimension tables populated")

    def generate_products(self):
        """Generate dim_product with 12 products across 2 lines"""
        logger.info("Generating products...")

        products = [
            {'id': 1, 'code': 'PT001', 'name': 'Premium Dog Bed', 'line': 'Premium Pet Toys', 'cost': 500, 'price': 1200},
            {'id': 2, 'code': 'PT002', 'name': 'Cat Scratching Tower', 'line': 'Premium Pet Toys', 'cost': 400, 'price': 950},
            {'id': 3, 'code': 'PT003', 'name': 'Dog Chew Toy', 'line': 'Premium Pet Toys', 'cost': 80, 'price': 199},
            {'id': 4, 'code': 'PT004', 'name': 'Interactive Ball', 'line': 'Premium Pet Toys', 'cost': 150, 'price': 349},
            {'id': 5, 'code': 'PT005', 'name': 'Pet Collar GPS', 'line': 'Premium Pet Toys', 'cost': 800, 'price': 2500},
            {'id': 6, 'code': 'PT006', 'name': 'Pet Feeder Bowl Set', 'line': 'Premium Pet Toys', 'cost': 200, 'price': 599},
            {'id': 7, 'code': 'PN001', 'name': 'Premium Dog Food', 'line': 'Pet Nutrition', 'cost': 120, 'price': 299},
            {'id': 8, 'code': 'PN002', 'name': 'Cat Food Premium', 'line': 'Pet Nutrition', 'cost': 100, 'price': 249},
            {'id': 9, 'code': 'PN003', 'name': 'Dog Supplement', 'line': 'Pet Nutrition', 'cost': 150, 'price': 399},
            {'id': 10, 'code': 'PN004', 'name': 'Cat Supplement', 'line': 'Pet Nutrition', 'cost': 140, 'price': 369},
            {'id': 11, 'code': 'PN005', 'name': 'Pet Treats Mix', 'line': 'Pet Nutrition', 'cost': 50, 'price': 149},
            {'id': 12, 'code': 'PN006', 'name': 'Organic Pet Snack', 'line': 'Pet Nutrition', 'cost': 90, 'price': 249},
        ]

        for product in products:
            self.cursor.execute("""
                INSERT INTO dim_product (product_id, product_code, product_name, product_line,
                                        unit_cost, suggested_price, launch_date, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (product['id'], product['code'], product['name'], product['line'],
                  product['cost'], product['price'], self.start_date, True))

        self.conn.commit()
        logger.info(f"Generated {len(products)} products")

    def generate_dealers(self):
        """Generate dim_dealer with 25 dealers"""
        logger.info("Generating dealers...")

        dealers = []
        for i in range(1, 26):
            channel_id = random.choice([1, 2, 3])
            dealers.append({
                'dealer_id': i,
                'dealer_code': f'DL{i:03d}',
                'dealer_name': f'Dealer {i}',
                'channel_id': channel_id,
                'region': random.choice(['North', 'Central', 'South', 'East']),
                'cooperation_start_date': self.start_date + timedelta(days=random.randint(0, 365)),
                'payment_terms_days': random.choice([30, 45, 60, 90]),
                'credit_limit': random.randint(1_000_000, 10_000_000),
                'is_active': True
            })

            self.cursor.execute("""
                INSERT INTO dim_dealer (dealer_id, dealer_code, dealer_name, channel_id,
                                       region, cooperation_start_date, payment_terms_days,
                                       credit_limit, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (dealers[-1]['dealer_id'], dealers[-1]['dealer_code'], dealers[-1]['dealer_name'],
                  dealers[-1]['channel_id'], dealers[-1]['region'], dealers[-1]['cooperation_start_date'],
                  dealers[-1]['payment_terms_days'], dealers[-1]['credit_limit'], dealers[-1]['is_active']))

        self.conn.commit()
        logger.info(f"Generated {len(dealers)} dealers")

    def generate_suppliers(self):
        """Generate dim_supplier with 15 suppliers"""
        logger.info("Generating suppliers...")

        suppliers = []
        for i in range(1, 16):
            suppliers.append({
                'supplier_id': i,
                'supplier_code': f'SP{i:03d}',
                'supplier_name': f'Supplier {i}',
                'location': random.choice(['Taiwan', 'China', 'Vietnam', 'Thailand']),
                'cooperation_start_date': self.start_date + timedelta(days=random.randint(0, 730)),
                'payment_terms_days': random.choice([30, 45, 60]),
                'lead_time_days': random.randint(7, 45),
                'is_active': True
            })

            self.cursor.execute("""
                INSERT INTO dim_supplier (supplier_id, supplier_code, supplier_name, location,
                                        cooperation_start_date, payment_terms_days, lead_time_days, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (suppliers[-1]['supplier_id'], suppliers[-1]['supplier_code'], suppliers[-1]['supplier_name'],
                  suppliers[-1]['location'], suppliers[-1]['cooperation_start_date'],
                  suppliers[-1]['payment_terms_days'], suppliers[-1]['lead_time_days'], suppliers[-1]['is_active']))

        self.conn.commit()
        logger.info(f"Generated {len(suppliers)} suppliers")

    def generate_employees(self):
        """Generate dim_employee with 150 employees"""
        logger.info("Generating employees...")

        employees = []
        for i in range(1, 151):
            hire_date = self.start_date + timedelta(days=random.randint(0, 730))
            employees.append({
                'employee_id': i,
                'employee_code': f'EMP{i:05d}',
                'employee_name': f'Employee {i}',
                'department_id': random.randint(1, 8),
                'employee_type_id': random.choice([1, 2, 3]),
                'job_grade': random.choice(['Entry', 'Mid', 'Senior', 'Manager', 'Director']),
                'birth_date': datetime(1970, 1, 1) + timedelta(days=random.randint(0, 20000)),
                'hire_date': hire_date,
                'termination_date': None,
                'is_active': True,
                'salary': random.randint(30_000, 200_000)
            })

            self.cursor.execute("""
                INSERT INTO dim_employee (employee_id, employee_code, employee_name, department_id,
                                         employee_type_id, job_grade, birth_date, hire_date,
                                         termination_date, is_active, salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (employees[-1]['employee_id'], employees[-1]['employee_code'], employees[-1]['employee_name'],
                  employees[-1]['department_id'], employees[-1]['employee_type_id'], employees[-1]['job_grade'],
                  employees[-1]['birth_date'], employees[-1]['hire_date'], employees[-1]['termination_date'],
                  employees[-1]['is_active'], employees[-1]['salary']))

        self.conn.commit()
        logger.info(f"Generated {len(employees)} employees")

    def inject_dirty_data(self, record, record_type='order'):
        """
        Intentionally inject data quality issues into records.
        This is NOT a bug - it's required to demonstrate data cleaning capabilities.
        """

        # Random dirty data injection based on configured rates
        if random.random() < DIRTY_DATA_CONFIG['missing_value_rate']:
            # Randomly set a value to None
            if record_type == 'order' and random.random() < 0.5:
                record['actual_ship_date'] = None  # Order not yet shipped

        if random.random() < DIRTY_DATA_CONFIG['format_inconsistency_rate']:
            # Introduce format inconsistency (e.g., full-width vs half-width numbers)
            if record_type == 'dealer' and 'dealer_code' in record:
                record['dealer_code'] = record['dealer_code'].replace('DL', 'ＤＬ')  # Full-width

        if random.random() < DIRTY_DATA_CONFIG['type_error_rate']:
            # Introduce type inconsistency
            if record_type == 'order' and 'order_quantity' in record:
                record['order_quantity'] = str(record['order_quantity'])  # Should be int

        if random.random() < DIRTY_DATA_CONFIG['outlier_rate']:
            # Introduce outliers
            if record_type == 'order' and 'order_amount' in record:
                from decimal import Decimal
                record['order_amount'] = float(record['order_amount']) * random.choice([10, 100, 0.01])

        return record

    def generate_orders(self):
        """Generate fact_orders with intentional dirty data"""
        logger.info("Generating orders with intentional data quality issues...")

        order_id = 1
        current_date = self.start_date

        while current_date <= self.end_date:
            if current_date.weekday() < 5:  # Business days only
                # Generate 5-15 orders per day
                daily_orders = random.randint(5, 15)

                for _ in range(daily_orders):
                    product_id = random.randint(1, 12)
                    dealer_id = random.randint(1, 25)
                    quantity = random.randint(1, 100)

                    # Get product price
                    self.cursor.execute("SELECT suggested_price FROM dim_product WHERE product_id = %s", (product_id,))
                    price_result = self.cursor.fetchone()
                    unit_price = price_result[0] if price_result else 100

                    order_amount = quantity * unit_price
                    promised_ship_date = current_date + timedelta(days=random.randint(1, 10))
                    actual_ship_date = promised_ship_date + timedelta(days=random.randint(-2, 5))

                    order_record = {
                        'order_id': order_id,
                        'order_date_id': self._get_date_id(current_date),
                        'product_id': product_id,
                        'dealer_id': dealer_id,
                        'channel_id': random.randint(1, 3),
                        'plant_id': random.randint(1, 3),
                        'order_quantity': quantity,
                        'unit_price': unit_price,
                        'order_amount': order_amount,
                        'promised_ship_date': promised_ship_date,
                        'actual_ship_date': actual_ship_date,
                        'payment_status': random.choice(['Paid', 'Pending', 'Partial']),
                        'payment_date': actual_ship_date + timedelta(days=random.randint(1, 60)) if random.random() > 0.1 else None
                    }

                    # Inject dirty data
                    order_record = self.inject_dirty_data(order_record, 'order')

                    try:
                        self.cursor.execute("""
                            INSERT INTO fact_orders
                            (order_id, order_date_id, product_id, dealer_id, channel_id, plant_id,
                             order_quantity, unit_price, order_amount, promised_ship_date,
                             actual_ship_date, payment_status, payment_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (order_record['order_id'], order_record['order_date_id'],
                              order_record['product_id'], order_record['dealer_id'],
                              order_record['channel_id'], order_record['plant_id'],
                              order_record['order_quantity'], order_record['unit_price'],
                              order_record['order_amount'], order_record['promised_ship_date'],
                              order_record['actual_ship_date'], order_record['payment_status'],
                              order_record['payment_date']))

                        order_id += 1
                    except Exception as e:
                        logger.debug(f"Error inserting order: {e}")
                        self.conn.rollback()
                        continue

            current_date += timedelta(days=1)

            # Commit every 1000 records
            if order_id % 1000 == 0:
                self.conn.commit()
                logger.info(f"Generated {order_id} orders...")

        self.conn.commit()
        logger.info(f"Total orders generated: {order_id - 1}")

    def _get_date_id(self, date_obj):
        """Get date_id from date object"""
        try:
            self.cursor.execute("SELECT date_id FROM dim_date WHERE date = %s", (date_obj.date(),))
            result = self.cursor.fetchone()
            return result[0] if result else 1
        except:
            return 1

    def run(self):
        """Execute full data generation pipeline"""
        try:
            logger.info("=" * 80)
            logger.info("Starting Data Generation - Phase 1: Historical Backfill")
            logger.info("=" * 80)
            logger.info(f"Period: {self.start_date.date()} to {self.end_date.date()}")
            logger.info("")

            self.connect()

            # Generate dimensions first
            self.generate_date_dimension()
            self.generate_dimension_data()
            self.generate_products()
            self.generate_dealers()
            self.generate_suppliers()
            self.generate_employees()

            # Generate facts with dirty data
            self.generate_orders()

            logger.info("")
            logger.info("=" * 80)
            logger.info("✓ Data Generation Phase 1 Complete")
            logger.info("=" * 80)
            logger.info("")
            logger.info("⚠ IMPORTANT: Dirty data has been intentionally injected.")
            logger.info("   See: generate_data_phase1.py and config.DIRTY_DATA_CONFIG")
            logger.info("")
            logger.info("Next Step: Run data_cleaning.py (ETL pipeline)")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Fatal error during data generation: {e}", exc_info=True)
            raise
        finally:
            self.close()


if __name__ == '__main__':
    generator = DataGenerator()
    generator.run()

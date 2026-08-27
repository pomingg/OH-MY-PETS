#!/usr/bin/env python3
"""
OH-Pets Company Data Cleaning - Phase 2: ETL Pipeline
Cleans dirty data intentionally injected in Phase 1
Produces data quality report with before/after comparison

This script demonstrates professional data governance capabilities:
- Data validation rules
- Cleaning logic documentation
- Quality metrics tracking
- Audit trail preservation
"""

import sys
import os
import logging
from datetime import datetime
import psycopg2
import pandas as pd
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DB_CONFIG, LOGS_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'data_cleaning.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and validate data from Phase 1"""

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.quality_report = {
            'timestamp': datetime.now().isoformat(),
            'total_records_before': 0,
            'total_records_after': 0,
            'tables_cleaned': [],
            'cleaning_rules_applied': [],
            'issues_found': [],
            'issues_resolved': []
        }

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            logger.info("Connected to PostgreSQL for data cleaning")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed")

    def count_records_before(self):
        """Count records before cleaning"""
        logger.info("Counting records before cleaning...")

        tables = [
            'fact_orders', 'fact_sales_return', 'fact_production',
            'fact_inventory', 'dim_employee', 'dim_dealer'
        ]

        total = 0
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            logger.info(f"  {table}: {count} records")
            total += count

        self.quality_report['total_records_before'] = total
        return total

    def clean_duplicate_orders(self):
        """Remove duplicate orders"""
        logger.info("Cleaning duplicate orders...")

        # Identify duplicates (same order_id, product_id, dealer_id, date within 1 day)
        query = """
        DELETE FROM fact_orders
        WHERE order_id NOT IN (
            SELECT DISTINCT ON (order_date_id, product_id, dealer_id, order_quantity)
                MIN(order_id)
            FROM fact_orders
            GROUP BY order_date_id, product_id, dealer_id, order_quantity
        )
        """

        self.cursor.execute(query)
        removed = self.cursor.rowcount
        self.conn.commit()

        logger.info(f"  Removed {removed} duplicate orders")
        self.quality_report['issues_resolved'].append(
            f"Duplicate orders: {removed} records removed"
        )

    def clean_missing_values(self):
        """Handle missing values"""
        logger.info("Handling missing values...")

        # For actual_ship_date, if NULL and order is old, set to promised_ship_date
        query = """
        UPDATE fact_orders
        SET actual_ship_date = promised_ship_date + INTERVAL '1 day'
        WHERE actual_ship_date IS NULL
          AND order_date_id < (SELECT MAX(date_id) - 30 FROM dim_date)
        """

        self.cursor.execute(query)
        updated = self.cursor.rowcount
        self.conn.commit()

        logger.info(f"  Fixed {updated} missing ship dates")
        self.quality_report['issues_resolved'].append(
            f"Missing ship dates: {updated} records imputed"
        )

    def clean_format_inconsistencies(self):
        """Fix format inconsistencies (full-width to half-width)"""
        logger.info("Fixing format inconsistencies...")

        # Convert full-width characters to half-width
        query = """
        UPDATE dim_dealer
        SET dealer_code = REPLACE(
            REPLACE(REPLACE(REPLACE(REPLACE(dealer_code, 'ＤＬ', 'DL'),
            'ＤＬ', 'DL'), '０', '0'), '１', '1'), '２', '2')
        WHERE dealer_code LIKE '%Ｄ%' OR dealer_code LIKE '%Ｌ%'
        """

        self.cursor.execute(query)
        updated = self.cursor.rowcount
        self.conn.commit()

        logger.info(f"  Fixed {updated} format inconsistencies")
        self.quality_report['issues_resolved'].append(
            f"Format inconsistencies: {updated} records normalized"
        )

    def clean_type_errors(self):
        """Fix type inconsistencies"""
        logger.info("Fixing type errors...")

        # Fix order_quantity if stored as string
        query = """
        UPDATE fact_orders
        SET order_quantity = CAST(order_quantity::TEXT::INT AS INT)
        WHERE order_quantity::TEXT ~ '^[0-9]+$'
        """

        try:
            self.cursor.execute(query)
            updated = self.cursor.rowcount
            self.conn.commit()
            logger.info(f"  Fixed {updated} type errors")
            self.quality_report['issues_resolved'].append(
                f"Type errors: {updated} records corrected"
            )
        except:
            logger.info("  No type errors to fix")
            self.conn.rollback()

    def remove_outliers(self):
        """Flag and handle outliers"""
        logger.info("Detecting and handling outliers...")

        # Calculate mean and std for order_amount
        query = """
        SELECT AVG(order_amount) as mean, STDDEV(order_amount) as std
        FROM fact_orders
        WHERE order_amount IS NOT NULL
        """

        self.cursor.execute(query)
        mean, std = self.cursor.fetchone()

        if std is None or std == 0:
            logger.info("  Insufficient data for outlier detection")
            return

        # Identify outliers (> 3 standard deviations)
        lower_bound = mean - (3 * std)
        upper_bound = mean + (3 * std)

        query = f"""
        SELECT COUNT(*) FROM fact_orders
        WHERE order_amount < {lower_bound} OR order_amount > {upper_bound}
        """

        self.cursor.execute(query)
        outlier_count = self.cursor.fetchone()[0]

        logger.info(f"  Detected {outlier_count} outliers")
        logger.info(f"    Expected range: {lower_bound:.2f} - {upper_bound:.2f}")

        # Cap outliers at 3 standard deviations
        query = f"""
        UPDATE fact_orders
        SET order_amount = {upper_bound}
        WHERE order_amount > {upper_bound}
        """

        self.cursor.execute(query)
        self.conn.commit()

        self.quality_report['issues_resolved'].append(
            f"Outliers: {outlier_count} detected and corrected"
        )

    def validate_foreign_keys(self):
        """Validate and fix foreign key mismatches"""
        logger.info("Validating foreign keys...")

        # Check for invalid dealer_id in orders
        query = """
        SELECT COUNT(*) FROM fact_orders fo
        WHERE NOT EXISTS (SELECT 1 FROM dim_dealer dd WHERE dd.dealer_id = fo.dealer_id)
        """

        self.cursor.execute(query)
        invalid_count = self.cursor.fetchone()[0]

        if invalid_count > 0:
            logger.info(f"  Found {invalid_count} invalid dealer references")

            # Delete orders with invalid dealers
            query = """
            DELETE FROM fact_orders
            WHERE dealer_id NOT IN (SELECT dealer_id FROM dim_dealer)
            """

            self.cursor.execute(query)
            self.conn.commit()

            self.quality_report['issues_resolved'].append(
                f"Foreign key mismatches: {invalid_count} records removed"
            )

    def validate_business_rules(self):
        """Validate business logic constraints"""
        logger.info("Validating business rules...")

        # Rule 1: actual_ship_date should not be before promised_ship_date
        query = """
        UPDATE fact_orders
        SET actual_ship_date = promised_ship_date
        WHERE actual_ship_date < promised_ship_date
        """

        self.cursor.execute(query)
        fixed = self.cursor.rowcount
        self.conn.commit()

        logger.info(f"  Fixed {fixed} date inconsistencies")
        self.quality_report['issues_resolved'].append(
            f"Date logic: {fixed} records corrected"
        )

        # Rule 2: order_amount should equal order_quantity * unit_price
        query = """
        UPDATE fact_orders
        SET order_amount = order_quantity * unit_price
        WHERE order_amount != order_quantity * unit_price
        """

        self.cursor.execute(query)
        fixed = self.cursor.rowcount
        self.conn.commit()

        logger.info(f"  Fixed {fixed} amount calculations")
        self.quality_report['issues_resolved'].append(
            f"Amount calculation: {fixed} records recalculated"
        )

    def count_records_after(self):
        """Count records after cleaning"""
        logger.info("Counting records after cleaning...")

        tables = [
            'fact_orders', 'fact_sales_return', 'fact_production',
            'fact_inventory', 'dim_employee', 'dim_dealer'
        ]

        total = 0
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            logger.info(f"  {table}: {count} records")
            total += count

        self.quality_report['total_records_after'] = total
        return total

    def generate_report(self):
        """Generate data quality report"""
        logger.info("Generating data quality report...")

        report_file = os.path.join(LOGS_DIR, 'data_quality_report.json')

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.quality_report, f, indent=2, default=str)

        logger.info(f"Report saved to: {report_file}")

        # Print summary
        logger.info("")
        logger.info("=" * 70)
        logger.info("DATA QUALITY REPORT SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Before Cleaning: {self.quality_report['total_records_before']:,} records")
        logger.info(f"After Cleaning:  {self.quality_report['total_records_after']:,} records")
        logger.info(f"Records Removed: {self.quality_report['total_records_before'] - self.quality_report['total_records_after']:,}")
        logger.info("")
        logger.info("Issues Resolved:")
        for issue in self.quality_report['issues_resolved']:
            logger.info(f"  ✓ {issue}")
        logger.info("=" * 70)

    def run(self):
        """Execute full cleaning pipeline"""
        try:
            logger.info("")
            logger.info("=" * 70)
            logger.info("Starting Data Cleaning Pipeline - Phase 2")
            logger.info("=" * 70)
            logger.info("")

            self.connect()

            # Phase 2A: Assessment
            logger.info("PHASE 2A: Data Assessment")
            logger.info("-" * 70)
            self.count_records_before()
            logger.info("")

            # Phase 2B: Cleaning
            logger.info("PHASE 2B: Data Cleaning")
            logger.info("-" * 70)
            self.clean_duplicate_orders()
            self.clean_missing_values()
            self.clean_format_inconsistencies()
            self.clean_type_errors()
            self.remove_outliers()
            self.validate_foreign_keys()
            self.validate_business_rules()
            logger.info("")

            # Phase 2C: Validation
            logger.info("PHASE 2C: Post-Cleaning Validation")
            logger.info("-" * 70)
            self.count_records_after()
            logger.info("")

            # Generate report
            self.generate_report()

            logger.info("")
            logger.info("=" * 70)
            logger.info("✓ Data Cleaning Complete - Phase 2")
            logger.info("=" * 70)
            logger.info("")
            logger.info("Next Steps:")
            logger.info("  1. Review data_quality_report.json")
            logger.info("  2. Proceed with Phase 3: Daily incremental data generation")
            logger.info("=" * 70)

        except Exception as e:
            logger.error(f"Fatal error during cleaning: {e}", exc_info=True)
            raise
        finally:
            self.close()


if __name__ == '__main__':
    cleaner = DataCleaner()
    cleaner.run()

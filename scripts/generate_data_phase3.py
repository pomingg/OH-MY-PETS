#!/usr/bin/env python3
"""
Phase 3: Daily Incremental Data Generation
Generates ONE day of data, maintaining state continuity
Runs via Windows Task Scheduler at 5:00 PM on business days

State Continuity Rules:
- Yesterday's closing inventory = Today's opening inventory
- Employees who left yesterday don't appear today
- In-progress orders advance toward completion
- Supplier delays carry over if unresolved
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import random
import psycopg2
from psycopg2 import sql

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DB_CONFIG, LOGS_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'phase3-daily.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DailyDataGenerator:
    """Generate incremental daily data with state continuity"""

    def __init__(self, target_date=None):
        """
        Initialize generator
        target_date: None = today, or datetime object for catch-up
        """
        self.conn = None
        self.cursor = None
        self.target_date = target_date or datetime.now().date()
        self.previous_date = self.target_date - timedelta(days=1)
        self.active_employees = []
        self.previous_inventory = {}
        self.monthly_turnover_rate = 0.012  # 1.2% per month

    def connect(self):
        """Connect to PostgreSQL"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to PostgreSQL for date: {self.target_date}")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise

    def close(self):
        """Close connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def is_business_day(self):
        """Check if target date is a business day"""
        self.cursor.execute(
            "SELECT is_business_day FROM dim_date WHERE date = %s",
            (self.target_date,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else False

    def get_date_id(self, date_obj):
        """Get date_id for a given date"""
        self.cursor.execute(
            "SELECT date_id FROM dim_date WHERE date = %s",
            (date_obj,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def load_state(self):
        """Load previous day's state for continuity"""
        logger.info("Loading previous day state...")

        # Get active employees (hired before today, not terminated)
        self.cursor.execute("""
            SELECT employee_id FROM dim_employee
            WHERE hire_date <= %s AND (termination_date IS NULL OR termination_date > %s)
        """, (self.target_date, self.target_date))
        self.active_employees = [row[0] for row in self.cursor.fetchall()]

        # Get previous day inventory (becomes today's opening)
        self.cursor.execute("""
            SELECT product_id, plant_id, ending_balance
            FROM fact_inventory
            WHERE inventory_date_id = (
                SELECT date_id FROM dim_date WHERE date = %s
            )
        """, (self.previous_date,))
        for product_id, plant_id, ending_balance in self.cursor.fetchall():
            self.previous_inventory[(product_id, plant_id)] = ending_balance

        logger.info(f"Loaded {len(self.active_employees)} active employees")
        logger.info(f"Loaded {len(self.previous_inventory)} inventory positions")

    def simulate_employee_changes(self):
        """Simulate employee turnover (resignations/terminations)"""
        logger.info("Simulating employee changes...")

        # Calculate daily turnover probability
        daily_turnover_prob = self.monthly_turnover_rate / 30

        terminations = []
        for employee_id in self.active_employees:
            if random.random() < daily_turnover_prob:
                terminations.append(employee_id)

        # Update termination dates
        for emp_id in terminations:
            self.cursor.execute("""
                UPDATE dim_employee
                SET termination_date = %s, is_active = FALSE
                WHERE employee_id = %s
            """, (self.target_date, emp_id))

        if terminations:
            self.conn.commit()
            logger.info(f"Terminated {len(terminations)} employees")
            self.active_employees = [e for e in self.active_employees if e not in terminations]

    def generate_orders(self):
        """Generate daily orders (only on business days)"""
        if not self.is_business_day():
            logger.info("Non-business day - skipping orders")
            return 0

        logger.info("Generating daily orders...")

        # Get max order_id for ID generation
        self.cursor.execute("SELECT MAX(order_id) FROM fact_orders")
        max_order_id = (self.cursor.fetchone()[0] or 0) + 1

        date_id = self.get_date_id(self.target_date)
        num_orders = random.randint(5, 15)  # 5-15 orders per business day
        order_count = 0

        for _ in range(num_orders):
            product_id = random.randint(1, 12)
            dealer_id = random.randint(1, 25)
            quantity = random.randint(1, 100)

            # Get product price
            self.cursor.execute(
                "SELECT suggested_price FROM dim_product WHERE product_id = %s",
                (product_id,)
            )
            price_result = self.cursor.fetchone()
            unit_price = float(price_result[0]) if price_result else 100

            order_amount = quantity * unit_price

            try:
                self.cursor.execute("""
                    INSERT INTO fact_orders
                    (order_id, order_date_id, product_id, dealer_id, channel_id, plant_id,
                     order_quantity, unit_price, order_amount, promised_ship_date,
                     actual_ship_date, payment_status, payment_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    max_order_id + order_count,
                    date_id, product_id, dealer_id,
                    random.randint(1, 3), random.randint(1, 3),
                    quantity, unit_price, order_amount,
                    self.target_date + timedelta(days=random.randint(1, 10)),
                    None,  # actual_ship_date not yet known
                    random.choice(['Pending', 'Paid']),
                    None
                ))
                order_count += 1
            except Exception as e:
                logger.debug(f"Order insert error: {e}")
                self.conn.rollback()

        self.conn.commit()
        logger.info(f"Generated {order_count} orders")
        return order_count

    def generate_production(self):
        """Generate daily production data (only on business days)"""
        if not self.is_business_day():
            return 0

        logger.info("Generating production data...")

        date_id = self.get_date_id(self.target_date)
        production_count = 0

        for plant_id in [1, 2, 3]:
            for product_id in range(1, 13):
                # Random production quantities
                planned = random.randint(100, 500)
                actual = int(planned * random.uniform(0.8, 1.0))
                good = int(actual * random.uniform(0.95, 0.99))
                defective = actual - good

                yield_rate = (good / actual * 100) if actual > 0 else 0
                utilization = random.uniform(0.7, 0.95) * 100
                downtime = random.randint(0, 120) if random.random() < 0.1 else 0

                try:
                    self.cursor.execute("""
                        INSERT INTO fact_production
                        (production_id, production_date_id, plant_id, product_id,
                         planned_quantity, actual_quantity, good_quantity, defective_quantity,
                         yield_rate, equipment_utilization_rate, downtime_minutes,
                         downtime_reason, shift)
                        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        date_id, plant_id, product_id,
                        planned, actual, good, defective,
                        yield_rate, utilization, downtime,
                        'Equipment failure' if downtime > 0 else None,
                        random.choice(['Morning', 'Afternoon', 'Night'])
                    ))
                    production_count += 1
                except:
                    self.conn.rollback()

        self.conn.commit()
        logger.info(f"Generated {production_count} production records")
        return production_count

    def generate_inventory(self):
        """Generate daily inventory (state continuity: yesterday's ending = today's opening)"""
        logger.info("Generating inventory with state continuity...")

        date_id = self.get_date_id(self.target_date)
        inventory_count = 0

        for plant_id in [1, 2, 3]:
            for product_id in range(1, 13):
                key = (product_id, plant_id)

                # Get yesterday's ending balance
                beginning = self.previous_inventory.get(key, random.randint(100, 1000))

                # Simulate inbound/outbound
                inbound = random.randint(0, 200)
                outbound = random.randint(0, 150)
                ending = max(0, beginning + inbound - outbound)

                try:
                    self.cursor.execute("""
                        INSERT INTO fact_inventory
                        (inventory_id, inventory_date_id, plant_id, product_id,
                         beginning_balance, inbound_quantity, outbound_quantity,
                         ending_balance, days_in_stock, is_slow_moving)
                        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        date_id, plant_id, product_id,
                        beginning, inbound, outbound, ending,
                        random.randint(1, 90),
                        ending > 300  # Flag slow-moving if high inventory
                    ))
                    inventory_count += 1
                except:
                    self.conn.rollback()

        self.conn.commit()
        logger.info(f"Generated {inventory_count} inventory records")
        return inventory_count

    def generate_attendance(self):
        """Generate daily attendance for active employees"""
        logger.info("Generating attendance...")

        date_id = self.get_date_id(self.target_date)
        attendance_count = 0

        for employee_id in self.active_employees:
            # Attendance probability
            is_present = random.random() > 0.05  # 95% attendance rate
            is_on_time = random.random() > 0.1 if is_present else False

            if is_present:
                hours = random.uniform(8, 9)
                overtime = random.uniform(0, 2) if random.random() > 0.9 else 0
            else:
                hours = 0
                overtime = 0

            try:
                self.cursor.execute("""
                    INSERT INTO fact_hr_attendance
                    (attendance_id, attendance_date_id, employee_id, attendance_status,
                     hours_worked, overtime_hours, is_present, is_on_time)
                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    date_id, employee_id,
                    'Present' if is_present else 'Absent',
                    hours, overtime, is_present, is_on_time
                ))
                attendance_count += 1
            except:
                self.conn.rollback()

        self.conn.commit()
        logger.info(f"Generated {attendance_count} attendance records")
        return attendance_count

    def run(self):
        """Execute daily data generation"""
        try:
            logger.info("")
            logger.info("=" * 80)
            logger.info(f"Phase 3: Daily Data Generation for {self.target_date}")
            logger.info("=" * 80)

            self.connect()
            self.load_state()
            self.simulate_employee_changes()

            # Generate data
            order_count = self.generate_orders()
            production_count = self.generate_production()
            inventory_count = self.generate_inventory()
            attendance_count = self.generate_attendance()

            logger.info("")
            logger.info("=" * 80)
            logger.info(f"✓ Daily Generation Complete for {self.target_date}")
            logger.info("=" * 80)
            logger.info(f"  Orders:      {order_count}")
            logger.info(f"  Production:  {production_count}")
            logger.info(f"  Inventory:   {inventory_count}")
            logger.info(f"  Attendance:  {attendance_count}")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            raise
        finally:
            self.close()


def catch_up_missing_days():
    """
    Catch-up mechanism: if script hasn't run for several days,
    generate data for all missing business days
    """
    logger.info("Checking for missing days...")

    generator = DailyDataGenerator()
    generator.connect()

    # Get the last date with data
    generator.cursor.execute("""
        SELECT MAX(order_date_id) FROM fact_orders
    """)
    last_date_id = generator.cursor.fetchone()[0]

    if last_date_id:
        generator.cursor.execute(
            "SELECT date FROM dim_date WHERE date_id = %s",
            (last_date_id,)
        )
        last_date = generator.cursor.fetchone()[0]
        generator.close()

        # Generate for all missing business days
        current = last_date + timedelta(days=1)
        today = datetime.now().date()

        while current <= today:
            logger.info(f"Generating catch-up data for {current}")
            daily_gen = DailyDataGenerator(current)
            daily_gen.run()
            current += timedelta(days=1)
    else:
        generator.close()


if __name__ == '__main__':
    # Check if specific date provided
    if len(sys.argv) > 1:
        try:
            target = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
            generator = DailyDataGenerator(target)
            generator.run()
        except ValueError:
            logger.error("Invalid date format. Use: YYYY-MM-DD")
            sys.exit(1)
    else:
        # Default: today, with catch-up if needed
        catch_up_missing_days()
        generator = DailyDataGenerator()
        generator.run()

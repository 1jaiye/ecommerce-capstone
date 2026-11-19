import unittest
import psycopg2


class TestWarehouse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(
            dbname="ecommerce_db",
            user="elijah",
            host="/var/run/postgresql",
            port=5432
        )

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_customer_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM dim_customer")
            self.assertEqual(cur.fetchone()[0], 100)

    def test_product_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM dim_product")
            self.assertEqual(cur.fetchone()[0], 20)

    def test_sales_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM fact_sales")
            self.assertEqual(cur.fetchone()[0], 516)

    def test_revenue_consistency(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT SUM(sales_amount)
                FROM fact_sales
                WHERE successfully_paid = TRUE
            """)
            warehouse_revenue = cur.fetchone()[0]

            cur.execute("""
                SELECT SUM(amount)
                FROM payments
                WHERE payment_status = 'successful'
            """)
            payment_revenue = cur.fetchone()[0]

            self.assertEqual(warehouse_revenue, payment_revenue)


if __name__ == "__main__":
    unittest.main()

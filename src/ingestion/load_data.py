import pandas as pd
import json
import psycopg2

conn = psycopg2.connect(
    dbname="ecommerce_db",
    user="elijah",
    host="/var/run/postgresql",
    port=5432
)

try:
    with conn:
        with conn.cursor() as cur:

            customers = pd.read_csv("data/raw/customers.csv")
            products = pd.read_json("data/raw/products.json")
            orders = pd.read_csv("data/raw/orders.csv")
            items = pd.read_csv("data/raw/order_items.csv")
            payments = pd.read_csv("data/raw/payments.csv")

            cur.executemany(
                "INSERT INTO customers VALUES (%s,%s,%s,%s,%s) ON CONFLICT (customer_id) DO NOTHING",
                customers.values.tolist()
            )

            cur.executemany(
                "INSERT INTO products VALUES (%s,%s,%s,%s) ON CONFLICT (product_id) DO NOTHING",
                products.values.tolist()
            )

            cur.executemany(
                "INSERT INTO orders VALUES (%s,%s,%s,%s) ON CONFLICT (order_id) DO NOTHING",
                orders.values.tolist()
            )

            cur.executemany(
                "INSERT INTO order_items VALUES (%s,%s,%s,%s,%s) ON CONFLICT (order_item_id) DO NOTHING",
                items.values.tolist()
            )

            cur.executemany(
                "INSERT INTO payments VALUES (%s,%s,%s,%s) ON CONFLICT (payment_id) DO NOTHING",
                payments.values.tolist()
            )

    print("Data loading completed successfully!")

except Exception as e:
    print("Loading failed:", e)
    raise

finally:
    conn.close()

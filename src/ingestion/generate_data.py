
import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Make the generated data repeatable
random.seed(42)

# Project folders
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Sample customers
customers = []

first_names = ["John", "Mary", "David", "Sarah", "James",
               "Grace", "Daniel", "Aisha", "Peter", "Fatima"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Okafor",
              "Yusuf", "Bello", "Musa", "Adeyemi", "Garba"]

cities = ["Lagos", "Abuja", "Kano", "Bauchi", "Port Harcourt"]

for customer_id in range(1, 101):
    first = random.choice(first_names)
    last = random.choice(last_names)

    customers.append({
        "customer_id": customer_id,
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}{customer_id}@example.com",
        "city": random.choice(cities)
    })

# Sample products
categories = ["Electronics", "Fashion", "Home", "Books", "Accessories"]

products = []

for product_id in range(1, 21):
    products.append({
        "product_id": product_id,
        "name": f"Product {product_id}",
        "category": random.choice(categories),
        "price": round(random.uniform(10, 500), 2)
    })

# Sample orders and order items
orders = []
order_items = []

statuses = ["paid", "pending", "cancelled", "shipped"]

start_date = datetime(2026, 1, 1)

for order_id in range(1, 201):
    customer_id = random.randint(1, 100)
    order_date = start_date + timedelta(days=random.randint(0, 300))
    status = random.choice(statuses)

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "status": status
    })

    # Each order contains between 1 and 4 products
    selected_products = random.sample(products, random.randint(1, 4))

    for item_number, product in enumerate(selected_products, start=1):
        quantity = random.randint(1, 3)

        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": product["price"]
        })

# Sample payments
payments = []

for order in orders:
    if order["status"] == "paid":
        payment_status = "successful"
    elif order["status"] == "cancelled":
        payment_status = "failed"
    else:
        payment_status = random.choice(["pending", "successful"])

    matching_items = [
        item for item in order_items
        if item["order_id"] == order["order_id"]
    ]

    amount = sum(
        item["quantity"] * item["unit_price"]
        for item in matching_items
    )

    payments.append({
        "payment_id": len(payments) + 1,
        "order_id": order["order_id"],
        "amount": round(amount, 2),
        "payment_status": payment_status
    })

# Save CSV files
def save_csv(filename, records):
    filepath = RAW_DIR / filename

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Created {filename}: {len(records)} records")


save_csv("customers.csv", customers)
save_csv("orders.csv", orders)
save_csv("order_items.csv", order_items)
save_csv("payments.csv", payments)

# Save products as JSON
products_file = RAW_DIR / "products.json"

with open(products_file, "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4)

print(f"Created products.json: {len(products)} records")

print("\nSample data generation completed!")

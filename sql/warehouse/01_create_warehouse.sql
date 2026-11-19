CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_date (
    full_date DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    day INTEGER
);

CREATE TABLE IF NOT EXISTS fact_sales (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES dim_customer(customer_id),
    product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
    order_date DATE NOT NULL REFERENCES dim_date(full_date),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    sales_amount NUMERIC(12,2) NOT NULL,
    successfully_paid BOOLEAN NOT NULL
);

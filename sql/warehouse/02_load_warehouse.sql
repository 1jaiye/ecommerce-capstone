-- Load customer dimension
INSERT INTO dim_customer
SELECT customer_id, first_name, last_name, email, city
FROM customers
ON CONFLICT (customer_id) DO NOTHING;

-- Load product dimension
INSERT INTO dim_product
SELECT product_id, name, category
FROM products
ON CONFLICT (product_id) DO NOTHING;

-- Load date dimension
INSERT INTO dim_date
SELECT DISTINCT
    order_date,
    EXTRACT(YEAR FROM order_date)::INTEGER,
    EXTRACT(MONTH FROM order_date)::INTEGER,
    TO_CHAR(order_date, 'Month'),
    EXTRACT(QUARTER FROM order_date)::INTEGER,
    EXTRACT(DAY FROM order_date)::INTEGER
FROM orders
ON CONFLICT (full_date) DO NOTHING;

-- Load sales fact table
INSERT INTO fact_sales (
    order_item_id, order_id, customer_id, product_id,
    order_date, quantity, unit_price, sales_amount,
    successfully_paid
)
SELECT
    oi.order_item_id,
    o.order_id,
    o.customer_id,
    oi.product_id,
    o.order_date,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price,
    EXISTS (
        SELECT 1
        FROM payments p
        WHERE p.order_id = o.order_id
          AND p.payment_status = 'successful'
    )
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
ON CONFLICT (order_item_id) DO NOTHING;

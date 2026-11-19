-- 1. Total revenue from successfully paid orders
SELECT
    SUM(amount) AS total_revenue
FROM payments
WHERE payment_status = 'successful';


-- 2. Top five products by revenue from successfully paid orders
SELECT
    p.name AS product_name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE EXISTS (
    SELECT 1
    FROM payments pay
    WHERE pay.order_id = o.order_id
      AND pay.payment_status = 'successful'
)
GROUP BY p.product_id, p.name
ORDER BY revenue DESC
LIMIT 5;


-- 3. Customers with more than three orders
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 3
ORDER BY order_count DESC;


-- 4. Monthly revenue from successfully paid orders
SELECT
    DATE_TRUNC('month', o.order_date)::DATE AS month,
    SUM(pay.amount) AS monthly_revenue
FROM payments pay
JOIN orders o ON o.order_id = pay.order_id
WHERE pay.payment_status = 'successful'
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;


-- 5. Top three customers by spending in each city
WITH customer_spending AS (
    SELECT
        c.city,
        c.customer_id,
        c.first_name,
        c.last_name,
        SUM(pay.amount) AS total_spending
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    JOIN payments pay ON pay.order_id = o.order_id
    WHERE pay.payment_status = 'successful'
    GROUP BY c.city, c.customer_id, c.first_name, c.last_name
),
ranked_customers AS (
    SELECT *,
        DENSE_RANK() OVER (
            PARTITION BY city
            ORDER BY total_spending DESC
        ) AS spending_rank
    FROM customer_spending
)
SELECT *
FROM ranked_customers
WHERE spending_rank <= 3
ORDER BY city, spending_rank;


-- 6. Order cancellation percentage
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'cancelled')
        / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_percentage
FROM orders;


-- 7. Cumulative monthly revenue
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date)::DATE AS month,
        SUM(pay.amount) AS revenue
    FROM payments pay
    JOIN orders o ON o.order_id = pay.order_id
    WHERE pay.payment_status = 'successful'
    GROUP BY DATE_TRUNC('month', o.order_date)
)
SELECT
    month,
    revenue,
    SUM(revenue) OVER (ORDER BY month) AS cumulative_revenue
FROM monthly_revenue
ORDER BY month;


-- 8. Customers who have never placed an order
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;

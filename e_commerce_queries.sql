USE ecommerce_analysis;

-- 1. VERIFY ALL TABLES
SELECT 'orders' AS table_name, COUNT(*) AS total FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers;

-- 2. TOTAL REVENUE
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(payment_value), 2) AS avg_order_value
FROM payments;

-- 3. MONTHLY REVENUE TREND
SELECT
    o.order_year,
    o.order_month,
    o.order_month_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY o.order_year, o.order_month, o.order_month_name
ORDER BY o.order_year, o.order_month;

-- 4. TOP 10 PRODUCT CATEGORIES BY REVENUE
SELECT
    pr.product_category_name_english AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.total_price), 2) AS total_revenue
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;

-- 5. CUSTOMER SEGMENTATION BY STATE
SELECT
    c.customer_state,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC
LIMIT 10;

-- 6. PAYMENT METHOD ANALYSIS
SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(payment_value), 2) AS total_value,
    ROUND(AVG(payment_value), 2) AS avg_value
FROM payments
GROUP BY payment_type
ORDER BY total_transactions DESC;

-- 7. ORDER STATUS BREAKDOWN
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 8. AVERAGE DELIVERY TIME BY STATE
SELECT
    c.customer_state,
    ROUND(AVG(o.delivery_days), 2) AS avg_delivery_days,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.delivery_days IS NOT NULL
  AND o.delivery_days > 0
GROUP BY c.customer_state
ORDER BY avg_delivery_days ASC
LIMIT 10;

-- 9. DAY WISE ORDER PATTERN
SELECT
    order_day,
    COUNT(*) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY order_day
ORDER BY total_orders DESC;

-- 10. TOP 10 CITIES BY ORDERS
SELECT
    c.customer_city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
GROUP BY c.customer_city
ORDER BY total_orders DESC
LIMIT 10;

-- 11. DELIVERY PERFORMANCE
SELECT
    delivery_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders
         WHERE delivery_status IS NOT NULL), 2) AS percentage
FROM orders
WHERE delivery_status IS NOT NULL
GROUP BY delivery_status;

-- 12. REVENUE BY PAYMENT INSTALLMENTS
SELECT
    payment_installments,
    COUNT(*) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    ROUND(AVG(payment_value), 2) AS avg_order_value
FROM payments
GROUP BY payment_installments
ORDER BY total_orders DESC
LIMIT 10;

-- 13. TOP 10 SELLERS BY REVENUE
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.total_price), 2) AS total_revenue
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
GROUP BY s.seller_id, s.seller_city, s.seller_state
ORDER BY total_revenue DESC
LIMIT 10;

-- 14. QUARTERLY REVENUE
SELECT
    order_year,
    order_quarter,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS quarterly_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY order_year, order_quarter
ORDER BY order_year, order_quarter;
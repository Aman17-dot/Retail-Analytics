-- SQL Analysis: Retail Order Data
-- Run against data/retail.db (SQLite). Table: orders (already cleaned by clean_data.py)
--
-- These queries answer the same business question as analysis.ipynb, using SQL only:
-- "Is any product category quietly declining in Q3 2024, even though total revenue looks fine?"

-- 1. Overall Q2 vs Q3 revenue check
SELECT
    CASE WHEN quarter = 2 THEN 'Q2' WHEN quarter = 3 THEN 'Q3' END AS qtr,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(*) AS order_count
FROM orders
WHERE quarter IN (2, 3) AND order_status IN ('Delivered', 'Returned')
GROUP BY quarter;

-- 2. Revenue by category, Q2 vs Q3, with % change (the key diagnostic query)
WITH cat_qtr AS (
    SELECT
        category,
        quarter,
        SUM(revenue) AS revenue
    FROM orders
    WHERE quarter IN (2, 3) AND order_status IN ('Delivered', 'Returned')
    GROUP BY category, quarter
),
pivoted AS (
    SELECT
        category,
        SUM(CASE WHEN quarter = 2 THEN revenue ELSE 0 END) AS q2_revenue,
        SUM(CASE WHEN quarter = 3 THEN revenue ELSE 0 END) AS q3_revenue
    FROM cat_qtr
    GROUP BY category
)
SELECT
    category,
    ROUND(q2_revenue, 2) AS q2_revenue,
    ROUND(q3_revenue, 2) AS q3_revenue,
    ROUND(100.0 * (q3_revenue - q2_revenue) / q2_revenue, 1) AS pct_change
FROM pivoted
ORDER BY pct_change ASC;

-- 3. Order count by month for Fashion & Beauty (checking volume collapse vs price change)
SELECT
    month,
    category,
    COUNT(*) AS order_count,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM orders
WHERE category IN ('Fashion', 'Beauty') AND order_status IN ('Delivered', 'Returned')
GROUP BY month, category
ORDER BY category, month;

-- 4. Customer segment (tercile by lifetime spend) x quarter revenue change
WITH customer_spend AS (
    SELECT customer_id, SUM(revenue) AS total_spend
    FROM orders
    WHERE customer_id != 'UNKNOWN' AND order_status IN ('Delivered', 'Returned')
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_spend,
        NTILE(3) OVER (ORDER BY total_spend) AS spend_tercile
    FROM customer_spend
),
segment_map AS (
    SELECT
        customer_id,
        CASE spend_tercile
            WHEN 1 THEN 'Low Value'
            WHEN 2 THEN 'Mid Value'
            WHEN 3 THEN 'High Value'
        END AS segment
    FROM ranked
)
SELECT
    s.segment,
    o.quarter,
    ROUND(SUM(o.revenue), 2) AS revenue
FROM orders o
JOIN segment_map s ON o.customer_id = s.customer_id
WHERE o.quarter IN (2, 3) AND o.order_status IN ('Delivered', 'Returned')
GROUP BY s.segment, o.quarter
ORDER BY s.segment, o.quarter;

-- 5. Top 10 customers by lifetime revenue (typical stakeholder ask)
SELECT
    customer_id,
    COUNT(*) AS order_count,
    ROUND(SUM(revenue), 2) AS lifetime_revenue
FROM orders
WHERE customer_id != 'UNKNOWN' AND order_status IN ('Delivered', 'Returned')
GROUP BY customer_id
ORDER BY lifetime_revenue DESC
LIMIT 10;

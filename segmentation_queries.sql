-- =====================================================================
-- CUSTOMER RFM SEGMENTATION & CHURN ANALYTICS REPOSITORY
-- Author: Ayush Kumar
-- =====================================================================

CREATE DATABASE IF NOT EXISTS retail_analytics;
USE retail_analytics;

-- 1. BASELINE TABLE SCHEMA
CREATE TABLE IF NOT EXISTS customer_rfm (
    customer_id INT PRIMARY KEY,
    recency INT NOT NULL,
    frequency INT NOT NULL,
    monetary DECIMAL(12,2) NOT NULL,
    country VARCHAR(100),
    recency_score INT,
    frequency_score INT,
    monetary_score INT,
    rfm_score VARCHAR(10),
    segment VARCHAR(50),
    segment_tier VARCHAR(50)
);

-- 2. EXECUTIVE SEGMENT LTV & REVENUE CONCENTRATION
SELECT 
    segment,
    segment_tier,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / SUM(COUNT(customer_id)) OVER (), 2) AS customer_share_pct,
    CONCAT('$', FORMAT(ROUND(SUM(monetary), 2), 2)) AS aggregate_revenue,
    ROUND(SUM(monetary) * 100.0 / SUM(SUM(monetary)) OVER (), 2) AS revenue_contribution_pct,
    CONCAT('$', FORMAT(ROUND(AVG(monetary), 2), 2)) AS segment_aov,
    ROUND(AVG(recency), 1) AS mean_recency_days,
    ROUND(AVG(frequency), 1) AS mean_purchase_frequency
FROM customer_rfm
GROUP BY segment, segment_tier
ORDER BY SUM(monetary) DESC;

-- 3. PARETO 80/20 CUSTOMER VALUE CONCENTRATION
WITH RankedCustomers AS (
    SELECT 
        customer_id,
        monetary,
        ROW_NUMBER() OVER (ORDER BY monetary DESC) AS customer_rank,
        COUNT(*) OVER () AS total_customer_base,
        SUM(monetary) OVER () AS total_platform_spend,
        SUM(monetary) OVER (ORDER BY monetary DESC) AS cumulative_spend
    FROM customer_rfm
)
SELECT 
    ROUND((customer_rank * 100.0 / total_customer_base), 2) AS percentile_customers,
    ROUND((cumulative_spend * 100.0 / total_platform_spend), 2) AS cumulative_revenue_pct
FROM RankedCustomers
WHERE customer_rank IN (
    ROUND(total_customer_base * 0.05),
    ROUND(total_customer_base * 0.10),
    ROUND(total_customer_base * 0.20),
    ROUND(total_customer_base * 0.50)
);

-- 4. CHURN ATTRITION EARLY WARNING MATRIX
SELECT 
    country,
    COUNT(customer_id) AS cohort_size,
    SUM(CASE WHEN recency > 180 THEN 1 ELSE 0 END) AS dormant_customers,
    ROUND(SUM(CASE WHEN recency > 180 THEN 1 ELSE 0 END) * 100.0 / COUNT(customer_id), 2) AS churn_rate_pct,
    CONCAT('$', FORMAT(ROUND(SUM(CASE WHEN recency > 180 THEN monetary ELSE 0 END), 2), 2)) AS gmv_at_risk
FROM customer_rfm
GROUP BY country
HAVING COUNT(customer_id) >= 20
ORDER BY churn_rate_pct DESC;

-- 5. RFM TIER MATRIX MAPPING
SELECT 
    recency_score,
    frequency_score,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(monetary), 2) AS avg_monetary_spend
FROM customer_rfm
GROUP BY recency_score, frequency_score
ORDER BY recency_score DESC, frequency_score DESC;

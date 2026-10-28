-- ============================================================================
-- Script: 03_data_validation.sql
-- Description: Post-import data validation queries to verify ingestion integrity.
-- Author: Senior Data Analyst & Technical Mentor
-- ============================================================================

-- 1. Verify Total Imported Row Count (Expected: exactly 2,480 rows)
SELECT 
    COUNT(*) AS total_rows,
    CASE 
        WHEN COUNT(*) = 2480 THEN 'PASS: Row count matches cleaned CSV'
        ELSE 'FAIL: Row count mismatch'
    END AS validation_status
FROM sales_orders;

-- 2. Verify Primary Key Uniqueness & Null Integrity
SELECT 
    COUNT(*) AS total_records,
    COUNT(row_id) AS non_null_ids,
    COUNT(DISTINCT row_id) AS distinct_ids,
    CASE 
        WHEN COUNT(*) = COUNT(DISTINCT row_id) THEN 'PASS: Primary Key is unique and complete'
        ELSE 'FAIL: Duplicate row_ids detected'
    END AS pk_status
FROM sales_orders;

-- 3. Check Date Ranges
SELECT 
    MIN(order_date) AS earliest_order,
    MAX(order_date) AS latest_order,
    MIN(ship_date)  AS earliest_ship,
    MAX(ship_date)  AS latest_ship,
    MIN(shipping_days) AS min_lead_time_days,
    MAX(shipping_days) AS max_lead_time_days
FROM sales_orders;

-- 4. Benchmark Totals Reconciliation Check
-- Ground Truth:
-- Revenue: $1,520,482.40 | Profit: $262,363.90 | Orders: 1,613 | Units: 6,748
SELECT 
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS overall_profit_margin_pct
FROM sales_orders;

-- 5. Check Distinct Count of Dimensions
SELECT 
    COUNT(DISTINCT customer_id) AS distinct_customers,
    COUNT(DISTINCT product_id)  AS distinct_products,
    COUNT(DISTINCT category)    AS distinct_categories,
    COUNT(DISTINCT sub_category) AS distinct_subcategories,
    COUNT(DISTINCT state)       AS distinct_states,
    COUNT(DISTINCT region)      AS distinct_regions
FROM sales_orders;

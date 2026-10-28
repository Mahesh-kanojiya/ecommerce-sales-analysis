-- ============================================================================
-- Script: 04_business_analysis.sql
-- Description: Core business intelligence queries for executive decision-making.
-- Author: Senior Data Analyst & Technical Mentor
-- ============================================================================

-- ============================================================================
-- QUERY 1: TOTAL REVENUE
-- Business Question: What is the gross revenue generated across the business?
-- Why this clause: SUM(sales) aggregates all transaction amounts.
-- Output Meaning: Total dollar volume invoiced to customers.
-- Business Action: Benchmark overall commercial scale and top-line performance.
-- ============================================================================
SELECT 
    ROUND(SUM(sales), 2) AS total_revenue
FROM sales_orders;


-- ============================================================================
-- QUERY 2: TOTAL PROFIT & OVERALL PROFIT MARGIN
-- Business Question: How much net profit did the business make and what is the margin?
-- Why this clause: SUM(profit) computes total bottom-line dollars; 
-- (SUM(profit)/SUM(sales))*100 computes the aggregate ratio (not average of rows!).
-- Output Meaning: Bottom-line retained earnings after accounting for product costs.
-- Business Action: Evaluate if top-line growth is translating into healthy earnings.
-- ============================================================================
SELECT 
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS overall_profit_margin_pct
FROM sales_orders;


-- ============================================================================
-- QUERY 3: TOTAL ORDERS PLACED
-- Business Question: How many distinct customer purchase orders were completed?
-- Why this clause: COUNT(DISTINCT order_id) avoids double-counting multi-item orders.
-- Output Meaning: The real number of shopping carts / invoices processed.
-- Business Action: Track transaction volume and operational fulfillment workload.
-- ============================================================================
SELECT 
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_orders;


-- ============================================================================
-- QUERY 4: TOTAL PHYSICAL UNITS SOLD & AVERAGE ITEMS PER ORDER
-- Business Question: How many physical product units were sold and basket size?
-- Why this clause: SUM(quantity) totals physical volume; dividing by distinct orders gives basket size.
-- Output Meaning: Physical volume moving through logistics and average items per cart.
-- Business Action: Optimize warehouse capacity and design cross-sell bundles.
-- ============================================================================
SELECT 
    SUM(quantity) AS total_units_sold,
    ROUND(CAST(SUM(quantity) AS NUMERIC) / COUNT(DISTINCT order_id), 2) AS avg_items_per_order
FROM sales_orders;


-- ============================================================================
-- QUERY 5: MONTHLY SALES & PROFIT TRENDS
-- Business Question: How do revenue and profit trend month-over-month across years?
-- Why this clause: GROUP BY order_year, order_month aggregates chronologically.
-- Output Meaning: Identifies peak commercial seasons and slow periods.
-- Business Action: Plan inventory stocking and marketing budgets ahead of Q4 surge.
-- ============================================================================
SELECT 
    order_year,
    order_month,
    order_month_name,
    COUNT(DISTINCT order_id) AS orders_count,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS monthly_profit_margin_pct
FROM sales_orders
GROUP BY order_year, order_month, order_month_name
ORDER BY order_month ASC;


-- ============================================================================
-- QUERY 6: CATEGORY-WISE SALES CONTRIBUTION
-- Business Question: Which merchandise division generates the highest revenue?
-- Why this clause: GROUP BY category with percentage contribution calculation.
-- Output Meaning: Shows the portfolio revenue mix across main divisions.
-- Business Action: Prioritize vendor negotiations for top revenue-driving categories.
-- ============================================================================
SELECT 
    category,
    COUNT(DISTINCT order_id) AS orders_count,
    SUM(quantity) AS total_units,
    ROUND(SUM(sales), 2) AS category_sales,
    ROUND((SUM(sales) / (SELECT SUM(sales) FROM sales_orders)) * 100, 2) AS sales_contribution_pct
FROM sales_orders
GROUP BY category
ORDER BY category_sales DESC;


-- ============================================================================
-- QUERY 7: CATEGORY-WISE PROFIT & PROFIT MARGIN COMPARISON
-- Business Question: Does high sales in a category guarantee high profit?
-- Why this clause: Compares SUM(sales) with SUM(profit) and calculates margin.
-- Output Meaning: Reveals whether high-revenue categories are truly lucrative or bleeding margin.
-- Business Action: Re-evaluate pricing or discount caps on low-margin categories like Furniture.
-- ============================================================================
SELECT 
    category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM sales_orders
GROUP BY category
ORDER BY total_profit DESC;


-- ============================================================================
-- QUERY 8: TOP 10 REVENUE-GENERATING PRODUCTS
-- Business Question: Which individual product SKUs drive the most revenue?
-- Why this clause: GROUP BY product, ORDER BY SUM(sales) DESC, LIMIT 10.
-- Output Meaning: Identifies the business's flagship "cash-cow" offerings.
-- Business Action: Protect inventory supply chain and prevent stock-outs on these items.
-- ============================================================================
SELECT 
    product_name,
    category,
    sub_category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_orders
GROUP BY product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================================
-- QUERY 9: BOTTOM 10 PRODUCTS BY PROFIT (LOSS-MAKING PRODUCTS)
-- Business Question: Which products are eroding company profits the most?
-- Why this clause: ORDER BY SUM(profit) ASC LIMIT 10 highlights net-negative items.
-- Output Meaning: Identifies products sold at a steep loss due to excessive discounting or high cost.
-- Business Action: Implement maximum discount caps, renegotiate supplier costs, or delist.
-- ============================================================================
SELECT 
    product_name,
    category,
    sub_category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_loss,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_given
FROM sales_orders
GROUP BY product_name, category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_loss ASC
LIMIT 10;


-- ============================================================================
-- QUERY 10: REGIONAL SALES & PROFITABILITY PERFORMANCE
-- Business Question: How do different geographic territories compare?
-- Why this clause: GROUP BY region to evaluate geographical health.
-- Output Meaning: Highlights high-performing vs under-performing sales regions.
-- Business Action: Reallocate regional sales incentives and review regional discount policies.
-- ============================================================================
SELECT 
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS regional_sales,
    ROUND(SUM(profit), 2) AS regional_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM sales_orders
GROUP BY region
ORDER BY regional_profit DESC;


-- ============================================================================
-- QUERY 11: MONTH-OVER-MONTH (MoM) SALES GROWTH USING LAG() WINDOW FUNCTION
-- Business Question: By what percentage did revenue grow or contract compared to the prior month?
-- Why this clause: CTE aggregates monthly sales, LAG() fetches previous row's sales value.
-- Output Meaning: Measures revenue velocity and business momentum month-by-month.
-- Business Action: Detect revenue deceleration early and investigate sudden monthly dips.
-- ============================================================================
WITH MonthlySales AS (
    SELECT 
        order_month,
        ROUND(SUM(sales), 2) AS current_month_sales
    FROM sales_orders
    GROUP BY order_month
)
SELECT 
    order_month,
    current_month_sales,
    LAG(current_month_sales, 1) OVER (ORDER BY order_month) AS prior_month_sales,
    ROUND(
        ((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY order_month)) /
         LAG(current_month_sales, 1) OVER (ORDER BY order_month)) * 100, 
        2
    ) AS mom_growth_pct
FROM MonthlySales
ORDER BY order_month ASC;


-- ============================================================================
-- QUERY 12: RANKING SUB-CATEGORIES WITHIN CATEGORIES USING DENSE_RANK()
-- Business Question: Within each main category, how do sub-categories rank by profit?
-- Why this clause: DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC).
-- Output Meaning: Provides a clean hierarchical ranking without skipping rank numbers.
-- Business Action: Focus category manager resources on top-ranked sub-categories.
-- ============================================================================
WITH SubCategoryProfit AS (
    SELECT 
        category,
        sub_category,
        ROUND(SUM(sales), 2) AS subcat_sales,
        ROUND(SUM(profit), 2) AS subcat_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
    FROM sales_orders
    GROUP BY category, sub_category
)
SELECT 
    category,
    sub_category,
    subcat_sales,
    subcat_profit,
    profit_margin_pct,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY subcat_profit DESC) AS profit_rank_within_cat
FROM SubCategoryProfit
ORDER BY category, profit_rank_within_cat;

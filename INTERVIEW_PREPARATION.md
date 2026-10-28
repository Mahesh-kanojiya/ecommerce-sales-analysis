# Data Analyst Portfolio Project: Interview Preparation Guide

**Project:** E-Commerce Sales & Business Performance Analysis  
**Candidate Target Role:** Junior Data Analyst / BI Analyst / Business Analyst  
**Core Technologies:** Excel, Python (Pandas), SQL (PostgreSQL), Power BI  

---

## 1. The 60–90 Second Project Elevator Pitch

> *"In my recent portfolio project, I developed an end-to-end commercial performance analysis for an e-commerce retail business operating across the United States with over 2,400 transaction line-items spanning 2023 and 2024.*
>
> *I followed a complete analytics lifecycle: First, I inspected the raw data in **Excel** to identify data hygiene anomalies such as duplicate records and mixed date formats. Next, I engineered an automated cleaning and ETL pipeline in **Python using Pandas**, resolving data quality issues, auditing duplicate transactions versus legitimate multi-item orders, and deriving analytical features.*
>
> *I loaded the cleaned data into a **PostgreSQL** database where I authored structured analytical queries using CTEs, window functions like `LAG()` and `DENSE_RANK()`, and aggregations to answer 12 core commercial questions. Finally, I built an interactive executive dashboard in **Power BI**, engineering custom DAX measures for KPIs like Average Order Value and aggregate Profit Margin.*
>
> *A key finding from my analysis was that while the **Technology** division drives 53% of sales and over 75% of net profit, the **Furniture** category suffered from severe margin erosion—specifically the **Tables** sub-category, which lost over $62,000 due to uncontrolled discounting exceeding 30%. I recommended implementing hard discount caps and shifting regional sales incentives from top-line revenue to margin contribution, which would immediately protect an estimated $50,000 in bottom-line profits."*

---

## 2. End-to-End Workflow & Technology Rationale

```
[ Raw CSV Data ] 
       │
       ▼
[ Excel Inspection ] ─────► Ad-hoc checks, missing values, formula audits (=COUNTIF, =SUM, =IFERROR)
       │
       ▼
[ Python Pandas ETL ] ────► Systematic deduplication, whitespace trimming, ISO date parsing, feature engineering
       │
       ▼
[ PostgreSQL / SQL ] ─────► Fact table schema, data validation, 12 business queries (CTEs, LAG, DENSE_RANK)
       │
       ▼
[ Power BI Dashboard ] ───► Dedicated Date Dimension, DAX modeling, KPI cards, interactive executive reporting
       │
       ▼
[ Business Recommendations ] ► Strategic actions on pricing caps, regional discounts, and cross-selling
```

### Why Use All 4 Tools? (Interview Defense)
- **Excel:** Best for rapid exploratory data inspection, sanity checking small slices of data, and building quick ad-hoc PivotTables for non-technical managers.
- **Python (Pandas):** Essential for reproducible, automated, and auditable ETL workflows. Manual spreadsheet cleaning risks human error and does not scale to millions of rows.
- **PostgreSQL / SQL:** The backbone of enterprise data warehouses. SQL provides secure, centralized, and fast querying across relational tables using industry-standard ANSI SQL.
- **Power BI:** The storytelling layer. Executives do not read raw SQL or Python scripts; they require interactive, visual dashboards with slicers, drill-downs, and automated refresh.

---

## 3. Data Cleaning Challenges & Business Rules Applied

| Problem Detected in Raw Data | Discovery Method | How It Was Solved in Python | Business Rationale |
| :--- | :--- | :--- | :--- |
| **Duplicate Records** | `.duplicated()` vs `.duplicated(subset=['Order ID'])` | Removed 3 exact duplicate rows using `.drop_duplicates()`. | **Critical Interview Concept:** In e-commerce, one `Order ID` can appear multiple times for legitimate multi-item carts. Only identical rows across *all* columns were dropped. |
| **Trailing Whitespace** | `.unique()` revealed `" Technology "` and `"Office Supplies "` | Applied `.astype(str).str.strip()` across all string columns. | Prevents duplicate category buckets in `GROUP BY` and Power BI slicers. |
| **Mixed Date Formats** | Identified strings like `15/01/2023` and `2023-01-15` | Parsed with `pd.to_datetime(..., format='mixed').dt.strftime('%Y-%m-%d')`. | Standardized into uniform ISO-8601 strings for SQL `DATE` ingestion. |
| **Missing Postal Codes** | 15 rows had `NaN` in Postal Code | Imputed with string `'Unknown'`. | Postal Code was non-critical; Region and State were 100% complete. Dropping rows would unnecessarily lose valid sales revenue. |
| **Impossible Outliers** | Found negative quantity (`-1`) and discount `> 100%` | Filtered out records using boolean mask `(Quantity > 0) & (Discount < 1.0)`. | Physical impossibility indicates erroneous test data; removing 2 rows protected financial integrity. |

---

## 4. Deep-Dive into Core SQL Queries

### A. Total Orders vs Total Rows (Query 3)
```sql
SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales_orders;
```
- **Interviewer Question:** *"Why did you use `COUNT(DISTINCT order_id)` instead of `COUNT(*)`?"*
- **Candidate Answer:** *"Our transactional dataset is at the order line-item level, meaning an order with 3 items occupies 3 rows. `COUNT(*)` returns 2,480 line items, whereas `COUNT(DISTINCT order_id)` accurately tells management that 1,613 unique purchasing transactions occurred."*

### B. Month-over-Month Growth via `LAG()` (Query 11)
```sql
WITH MonthlySales AS (
    SELECT order_month, ROUND(SUM(sales), 2) AS current_month_sales
    FROM sales_orders GROUP BY order_month
)
SELECT 
    order_month,
    current_month_sales,
    LAG(current_month_sales, 1) OVER (ORDER BY order_month) AS prior_month_sales,
    ROUND(((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY order_month)) /
           LAG(current_month_sales, 1) OVER (ORDER BY order_month)) * 100, 2) AS mom_growth_pct
FROM MonthlySales;
```
- **Interviewer Question:** *"What does `LAG()` do here?"*
- **Candidate Answer:** *"`LAG()` is a window function that reaches back to the preceding row in chronological order without requiring an expensive self-join. It fetches the prior month's revenue so we can calculate percentage velocity month-over-month."*

### C. Sub-Category Ranking via `DENSE_RANK()` (Query 12)
```sql
DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS profit_rank
```
- **Candidate Answer:** *"`PARTITION BY category` resets the ranking counter for each parent category division, and `DENSE_RANK()` ensures consecutive rank numbering without skipping values in the event of ties."*

---

## 5. Power BI DAX Modeling & Ratios

### The "Profit Margin" Interview Question
- **Interviewer Question:** *"How did you calculate overall profit margin in Power BI?"*
- **Wrong Answer:** `AVERAGE(sales_orders[profit_margin_pct])` (Averaging row percentages leads to massive mathematical errors because it treats a $10 sale the same as a $10,000 sale!).
- **Correct Answer:**
  ```dax
  Profit Margin % = 
  DIVIDE(
      [Total Profit], 
      [Total Revenue], 
      0
  )
  ```
- **Explanation:** *"Profit margin is an **aggregate ratio**, computed as total aggregated profit divided by total aggregated revenue. I used the `DIVIDE()` function because it natively guards against division-by-zero errors."*

### Dedicated Date Dimension Table
- **Interviewer Question:** *"Why not just use the date column in the sales table?"*
- **Candidate Answer:** *"Enterprise Power BI best practice requires a dedicated, continuous Date dimension table (`DateTable`) marked as a Date Table. This enables accurate Time Intelligence DAX functions like `DATEADD()` and `SAMEPERIODLASTYEAR`, ensures uniform chronological sorting, and decouples time filtering from transactional granularity."*

---

## 6. The 5 Core Business Insights (Quick-Recall Summary)

1. **Technology is the Growth Engine:** Contributes 53.04% of revenue ($806.5K) and 75.42% of total profit ($197.9K) at a healthy 24.54% margin.
2. **The Furniture Margin Trap:** Furniture generates $615K in sales but only $25.2K in profit (4.10% margin). The entire **Tables** subcategory operates at **-$62.9K net loss** due to excessive discounts (26%–31%).
3. **Office Supplies is High-Margin but Under-Marketed:** Generates the highest margin (39.73%), with Paper (42%) and Storage (45%), but only accounts for 6.5% of total sales. Recommended automated cross-selling at checkout.
4. **Central Region Margin Disparity:** Central region margin (12.70%) lags East (19.54%) and West (19.11%) because Central sales teams grant 2.6× higher average discounts (17.01% vs 6.2%). Recommended aligning sales incentives with margin dollars rather than gross sales.
5. **Q4 Surge (+37.8%):** Strong holiday seasonality in October, November, and December requires locking in inventory orders 90 days in advance.

---

## 7. Ten Likely Fresher Interview Questions with Model Answers

### Q1: Walk me through your project.
- **Answer:** Follow the 60-90 second elevator pitch in Section 1. Highlight the problem, your 4-tool stack, key findings, and business recommendations.

### Q2: What was your criteria for removing duplicate records?
- **Answer:** *"I differentiated between exact duplicate transactions (ETL logging glitches) and repeated `Order ID`s. In retail e-commerce, multiple rows sharing an `Order ID` represent valid line items in a single customer cart. I only dropped the 3 rows that were 100% duplicate across all fields."*

### Q3: Why didn't you drop rows with missing postal codes?
- **Answer:** *"Out of 2,485 rows, only 15 were missing postal codes. The State, City, and Region columns were 100% populated. Dropping those rows would have unnecessarily discarded legitimate revenue and units. Instead, I imputed `'Unknown'`."*

### Q4: How did you reconcile your results across Excel, Python, and SQL?
- **Answer:** *"I built an automated Python verification script (`reconcile_metrics.py`) that loaded the outputs from all three environments. Total Revenue ($1,520,482.40), Total Profit ($262,363.90), Total Orders (1,613), and Profit Margin (17.26%) matched to the penny across all tools."*

### Q5: What is the difference between `WHERE` and `HAVING` in SQL?
- **Answer:** *"`WHERE` filters individual rows before any grouping or aggregation takes place. `HAVING` filters aggregated groups after `GROUP BY`. In Query 9, I used `HAVING SUM(profit) < 0` to filter only product groups with a net aggregate loss."*

### Q6: What is a CTE and why did you use it?
- **Answer:** *"A Common Table Expression (CTE) creates a temporary, named result set defined with the `WITH` keyword. I used it in Query 11 (MoM growth) and Query 12 (Rankings) to make complex queries modular, readable, and easy to debug."*

### Q7: What is the difference between `RANK()` and `DENSE_RANK()`?
- **Answer:** *"Both rank records within a partition. However, if two records tie for rank 1, `RANK()` will skip rank 2 and assign rank 3 to the next record. `DENSE_RANK()` does not skip rank numbers; the next record receives rank 2."*

### Q8: What visual hierarchy did you use in Power BI?
- **Answer:** *"I placed global date and category slicers in the top header, followed immediately by 5 primary KPI summary cards (Revenue, Profit, Margin, Orders, Units). Below that, I placed the broad monthly trajectory line chart and category breakdown, finishing with detailed product-level rankings and loss-makers at the bottom."*

### Q9: If a business manager asked you why Furniture profit is so low, how would you respond?
- **Answer:** *"I would guide them to the sub-category drill-down. Chairs and Bookcases are actually profitable (>21% margin). The entire profit drain is isolated in the Tables sub-category, which lost -$62,914 because average discounts exceeded 26% while unit costs are high. Capping discounts on Tables at 10% would instantly restore Furniture profitability."*

### Q10: How would you scale this project if the data grew to 50 million rows?
- **Answer:** *"For 50 million rows, I would move data cleaning into a distributed engine like PySpark or dbt, store the fact and dimension tables in a columnar cloud data warehouse like Snowflake or BigQuery, and connect Power BI using DirectQuery or an Aggregation / Composite Model to maintain sub-second visual performance."*

---

## 8. Five Tricky Follow-Up Questions (Advanced Preparation)

### 1. Data Quality: *"What would you do if order dates were after ship dates?"*
- **Answer:** *"That violates physical causality. I would log those records into an anomaly quarantine table, flag them for the data engineering team as order-management system (OMS) timestamp errors, and exclude them from shipping lead-time KPIs."*

### 2. Duplicates: *"How would you deduplicate records in pure SQL?"*
- **Answer:**
  ```sql
  WITH RankedRows AS (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id, product_id ORDER BY row_id) AS rn
      FROM sales_orders
  )
  DELETE FROM sales_orders WHERE row_id IN (SELECT row_id FROM RankedRows WHERE rn > 1);
  ```

### 3. Financial Logic: *"Why can a product have high sales but negative profit?"*
- **Answer:** *"Sales measures top-line revenue after discount (`Quantity * Price * (1 - Discount)`), but profit subtracts cost of goods sold. If the promotional discount rate is greater than the gross margin percentage, every incremental unit sold increases the company's financial loss."*

### 4. SQL Performance: *"What indexes did you create and why?"*
- **Answer:** *"I created B-Tree indexes on `order_date`, `category`, `region`, `customer_id`, and `order_id`. These columns are frequently used in `WHERE` filters, `JOIN` conditions, and `GROUP BY` aggregations, allowing PostgreSQL to use index scans instead of expensive sequential table scans."*

### 5. Dashboard UX: *"Why did you limit the dashboard to 5 core visuals?"*
- **Answer:** *"To avoid cognitive overload. An executive dashboard should answer high-level questions in under 10 seconds. Visual clutter dilutes decision-making. Deeper operational drill-downs can be provided via tooltips or secondary drill-through pages."*

---

## 9. Project Limitations & Future Improvements

- **Dataset Limitation:** The dataset spans 2 calendar years and 2,480 cleaned rows, which is ideal for desktop portfolio evaluation, but does not capture multi-year macroeconomic shifts.
- **Future Improvements:**
  1. **Customer RFM Segmentation:** Calculate Recency, Frequency, and Monetary scores to segment customers into Champions, Loyal, At-Risk, and Lost.
  2. **Predictive Sales Forecasting:** Implement a Time-Series forecasting model (ARIMA or Prophet) in Python to forecast Q4 holiday demand.
  3. **Automated CI/CD ETL Pipeline:** Package the Python cleaning script into a scheduled Apache Airflow DAG or GitHub Actions workflow.

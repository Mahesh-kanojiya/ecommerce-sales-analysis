# E-Commerce Sales & Business Performance Analysis

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791.svg)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-Office_365-217346.svg)](https://www.microsoft.com/excel)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> **A realistic, industry-aligned Data Analytics portfolio project demonstrating end-to-end commercial performance analysis across Excel, Python (Pandas/NumPy), SQL (PostgreSQL), and Power BI (DAX).**

---

## 1. Project Overview & Business Context

In competitive retail e-commerce, top-line revenue growth can often mask critical underlying margin erosion. The goal of this project is to analyze transactional sales data across the United States (2023–2024), diagnose commercial bottlenecks, and deliver actionable recommendations to corporate leadership.

### Primary Business Questions Addressed:
- What are the company's total gross sales, net profit, and aggregate profit margin?
- How many distinct purchase orders were processed, and what is the average basket size?
- Which merchandise categories drive top-line revenue versus bottom-line profit?
- Are there specific products exhibiting high sales but negative profitability?
- What regional performance disparities exist, and what role does discounting play?
- What operational and pricing interventions should executive managers implement?

---

## 2. Key Executive Metrics (Reconciled & Verified)

All calculations are mathematically reconciled across Excel, Python, PostgreSQL, and Power BI DAX:

| Executive Metric | Reconciled Value | Business Interpretation |
| :--- | :--- | :--- |
| **Total Gross Revenue** | **$1,520,482.40** | Total customer invoiced sales across 2023–2024 |
| **Total Net Profit** | **$262,363.90** | Net earnings retained after product and fulfillment costs |
| **Overall Profit Margin** | **17.26%** | Aggregate ratio: `Total Profit / Total Revenue` |
| **Total Distinct Orders** | **1,613** | Unique customer checkout carts / invoices |
| **Total Physical Units Sold**| **6,748** | Merchandise units shipped (Avg: 4.18 items/order) |
| **Top Revenue Category** | **Technology ($806.5K)** | 53.04% of total sales, 24.54% profit margin |
| **Profit Bleeder Sub-Category** | **Tables (-$62.9K)** | High volume destroyed by steep 26–31% discounts |

---

## 3. End-to-End Analytics Workflow

```
Raw Data Inspection ──► Automated Python ETL ──► Relational Database ──► SQL Analysis ──► Power BI Dashboard ──► Business Strategy
   (Excel Formulas)         (Pandas Cleaning)         (PostgreSQL Schema)    (CTEs & Windows)       (DAX & Visuals)       (Action Matrix)
```

1. **Excel Inspection:** Inspected data types, detected trailing whitespace in categories, audited duplicates, and validated preliminary sums with `=SUM()`, `=COUNTIF()`, and `=IFERROR()`.
2. **Python Data Cleaning:** Systematically deduplicated records, preserved legitimate multi-item orders, standardized dates to ISO `YYYY-MM-DD`, trimmed string padding, and engineered derived features (`order_month`, `profit_margin_pct`, `cost`, `shipping_days`).
3. **PostgreSQL Database:** Designed an indexed fact table, verified data ingestion integrity, and authored 12 modular business queries utilizing window functions (`LAG()`, `DENSE_RANK()`), CTEs, and aggregations.
4. **Power BI Dashboard:** Created a dedicated Date Dimension (`DateTable`), engineered DAX measures (`DIVIDE()`, `DISTINCTCOUNT()`), and built an interactive 5-KPI executive dashboard with monthly trajectories, category breakdowns, and loss-maker alerts.
5. **Reconciliation Audit:** Verified 100% mathematical consistency across all four tools.

---

## 4. Repository Structure

```
ecommerce-sales-analysis/
│
├── README.md                           # Master project documentation
├── INTERVIEW_PREPARATION.md            # 60s pitch, 10 interview Q&As, follow-ups
├── requirements.txt                    # Python library dependencies
├── .gitignore                          # Standard git ignore rules
├── .env.example                        # PostgreSQL database environment template
│
├── data/
│   ├── DATA_DICTIONARY.md              # Detailed 21-column schema specifications
│   ├── raw/
│   │   └── ecommerce_sales_raw.csv     # Raw dataset with controlled data issues
│   └── processed/
│       ├── cleaned_sales_data.csv      # Cleaned, standardized dataset (2,480 rows)
│       └── ecommerce.db                # Embedded SQLite database for zero-config testing
│
├── excel/
│   ├── ecommerce_sales_analysis.xlsx   # 4-tab styled workbook with formulas & PivotTable
│   └── EXCEL_WORKFLOW_GUIDE.md         # Step-by-step Excel tutorial and formulas guide
│
├── notebooks/
│   └── 01_data_cleaning_and_eda.ipynb  # Interactive Jupyter notebook for cleaning & EDA
│
├── python/
│   ├── generate_raw_data.py            # Generates realistic synthetic benchmark dataset
│   ├── data_cleaning.py                # Production-grade Python ETL cleaning pipeline
│   ├── generate_excel_workbook.py      # Builds styled Excel portfolio workbook
│   ├── run_sql_analysis.py             # Executes and verifies all 12 SQL queries
│   ├── generate_dashboard_visuals.py   # Renders dashboard mockup and chart previews
│   └── reconcile_metrics.py            # Cross-tool reconciliation validator
│
├── sql/
│   ├── 01_schema_setup.sql             # PostgreSQL DDL table creation and indexes
│   ├── 02_data_import.sql              # CSV copy instructions (psql, pgAdmin, Python)
│   ├── 03_data_validation.sql          # Post-import sanity and benchmark checks
│   └── 04_business_analysis.sql        # 12 executive business intelligence queries
│
├── powerbi/
│   ├── measures.dax                    # Production DAX measures with formula explanations
│   ├── dashboard_instructions.md       # Canvas layout, palette, and build walkthrough
│   └── dashboard_preview.png           # High-resolution executive dashboard mockup
│
└── reports/
    ├── business_insights.md            # 5 deep-dive insights with hypotheses and actions
    ├── data_cleaning_audit.md          # ETL data quality transformation report
    ├── sql_analysis_summary.md         # Formatted outputs of all 12 SQL queries
    ├── reconciliation_matrix.md        # Cross-tool mathematical comparison matrix
    └── charts/
        ├── monthly_trend.png           # Monthly revenue and profit trajectory
        └── category_breakdown.png      # Category revenue and margin comparisons
```

---

## 5. Executive Dashboard Design Reference

Below is the design layout implemented for the Power BI Dashboard:

```
+----------------------------------------------------------------------------------------------------+
|  LOGO: Executive E-Commerce Sales & Business Performance Dashboard          [DATE] [CAT] [REGION]  |
+----------------------------------------------------------------------------------------------------+
| [ TOTAL REVENUE ]   [ TOTAL PROFIT ]   [ PROFIT MARGIN ]   [ TOTAL ORDERS ]   [ UNITS SHIPPED ]    |
|   $1,520,482           $262,364             17.3%               1,613              6,748           |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 1: Monthly Revenue & Profit Trajectory   |  VISUAL 2: Category Revenue vs Profit Mix       |
|  (Line and Column Chart - Peaks in Q4 Highlight) |  (Clustered Bar Chart - Technology Dominance)   |
|                                                  |                                                 |
+--------------------------------------------------+-------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 3: Top 5 Revenue-Generating Products     |  VISUAL 4: Loss-Making Products ($K Loss)       |
|  (Flagship Enterprise Printers & Phones)         |  (Heavily Discounted Tables - Margin Bleeders)  |
|                                                  |                                                 |
+--------------------------------------------------+-------------------------------------------------+
|  VISUAL 5: Regional Profit Margin Comparison (West: 19.1%, East: 19.5%, Central: 12.7%)           |
+----------------------------------------------------------------------------------------------------+
```

*Full visual preview available in [`powerbi/dashboard_preview.png`](file:///c:/Users/mahes/OneDrive/Desktop/ecommerce-sales-analysis/powerbi/dashboard_preview.png).*

---

## 6. How to Run & Verify the Project Locally

### Prerequisites
- Python 3.10 or higher
- Git

### Step 1: Clone Repository & Install Dependencies
```bash
git clone https://github.com/your-username/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis
python -m pip install -r requirements.txt
```

### Step 2: Run Data Cleaning & ETL Pipeline
```bash
python python/data_cleaning.py
```
*Expected Output:* Cleans raw transactions, removes exact duplicates, standardizes dates, and creates `data/processed/cleaned_sales_data.csv`.

### Step 3: Generate the Excel Portfolio Workbook
```bash
python python/generate_excel_workbook.py
```
*Expected Output:* Generates `excel/ecommerce_sales_analysis.xlsx` with live `=SUM()`, `=COUNTIF()`, and PivotTables.

### Step 4: Run SQL Analysis Queries
```bash
python python/run_sql_analysis.py
```
*Expected Output:* Loads the cleaned data into SQLite (or PostgreSQL if `.env` configured) and executes all 12 analytical queries, saving outputs to `reports/sql_analysis_summary.md`.

### Step 5: Validate Cross-Tool KPI Reconciliation
```bash
python python/reconcile_metrics.py
```
*Expected Output:* Displays the exact match matrix confirming zero discrepancy across Python, SQL, Excel, and Power BI.

### Step 6: Build the Power BI Dashboard
1. Open Power BI Desktop.
2. Follow the detailed build instructions in [`powerbi/dashboard_instructions.md`](file:///c:/Users/mahes/OneDrive/Desktop/ecommerce-sales-analysis/powerbi/dashboard_instructions.md).
3. Copy DAX measures directly from [`powerbi/measures.dax`](file:///c:/Users/mahes/OneDrive/Desktop/ecommerce-sales-analysis/powerbi/measures.dax).

---

## 7. Strategic Recommendations for Business Leadership

1. **Enforce Hard Discount Caps on Furniture Tables:** Tables lost **-$62,914** due to average discounts exceeding 26%. Capping table discounts at 10% immediately protects ~$50,000 in bottom-line margin.
2. **Align Central Territory Sales Incentives with Profit Margin:** Central region margins lag by 7 percentage points due to 2.6× higher discounts. Shifting sales rep compensation from gross volume to gross margin dollars will curb excessive discounting.
3. **Automate Cross-Selling for High-Margin Office Supplies:** Office supplies boasts a **39.73% profit margin** (Paper: 42%, Art: 51%), but only 6.5% of revenue. Recommend bundling office supplies with technology purchases at checkout.
4. **Advance Inventory Procurement for Q4 Surge:** Fourth-quarter sales jump by **37.8%**. Procuring flagship enterprise tech items 90 days in advance prevents holiday stock-outs.

---

## 8. Author & Interview Readiness

- **Author:** Fresher Data Analyst Portfolio
- **Interview Guide:** Read [`INTERVIEW_PREPARATION.md`](file:///c:/Users/mahes/OneDrive/Desktop/ecommerce-sales-analysis/INTERVIEW_PREPARATION.md) for the 60-second pitch, tricky follow-up questions, and sample interview answers.
- **Data License:** Curated synthetic dataset modeled on the Global Superstore benchmark schema under Creative Commons CC-BY 4.0.

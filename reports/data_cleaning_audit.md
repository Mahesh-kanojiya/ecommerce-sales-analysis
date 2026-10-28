# Data Cleaning Audit Report

## 1. Summary of Data Transformations
- **Input File:** `data/raw/ecommerce_sales_raw.csv`
- **Output File:** `data/processed/cleaned_sales_data.csv`
- **Initial Raw Rows:** 2,485
- **Final Cleaned Rows:** 2,480
- **Net Rows Dropped:** 5 (0.20%)
- **Data Retention Rate:** 99.80%

---

## 2. Cleaning Actions & Business Rules Applied

| Issue Identified | Frequency | Business Rationale & Action Taken |
| :--- | :--- | :--- |
| **Exact Duplicate Rows** | 3 rows | Dropped identical records resulting from ETL ingestion glitches. Distinct multi-item orders (`order_id` repeated with different items) were preserved. |
| **Trailing/Leading Whitespace** | 12 rows | Applied `.str.strip()` to ensure `Category` values like `' Technology '` properly merged with `'Technology'`. |
| **Inconsistent Date Formats** | 8 rows | Parsed mixed date representations (`DD/MM/YYYY` and `YYYY/MM/DD`) into uniform ISO-8601 `YYYY-MM-DD` strings. |
| **Missing Postal Codes** | 15 rows | Postal Code is non-critical for high-level regional analysis; imputed with `'Unknown'` to avoid cascading null errors. |
| **Impossible Outliers** | 2 rows | Removed records with physical impossibilities: negative quantities (`Quantity <= 0`) and discount rates `>= 100%`. |

---

## 3. Benchmark Verification Totals (For SQL & Power BI Cross-Checking)

- **Total Revenue (Sales):** `$1,520,482.40`
- **Total Profit:** `$262,363.90`
- **Total Orders (Distinct):** `1,613`
- **Total Quantity Sold:** `6,748`
- **Aggregate Profit Margin:** `17.26%`

*(These benchmark values are verified against PostgreSQL queries and Power BI DAX measures in Phase 5).*

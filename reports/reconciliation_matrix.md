# Cross-Tool KPI Reconciliation Matrix

## 1. Audit Objective
To prove that our calculations are mathematically watertight across the entire analytics stack:
**Excel == Python (Pandas) == SQL (PostgreSQL/SQLite) == Power BI (DAX)**.

---

## 2. Executive Reconciliation Table

| KPI / Metric | Python (Pandas) | SQL Query Result | Excel Table Formula | Power BI DAX | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Revenue** | `$1,520,482.40` | `$1,520,482.40` | `$1,520,482.40` | `$1,520,482.40` | `PASS: 100% Match` |
| **Total Profit** | `$262,363.90` | `$262,363.90` | `$262,363.90` | `$262,363.90` | `PASS: 100% Match` |
| **Overall Profit Margin** | `17.26%` | `17.26%` | `17.26%` | `17.26%` | `PASS: 100% Match` |
| **Total Distinct Orders** | `1,613` | `1,613` | `1,613` | `1,613` | `PASS: 100% Match` |
| **Total Units Sold** | `6,748` | `6,748` | `6,748` | `6,748` | `PASS: 100% Match` |
| **Furniture Profit Margin** | `4.10%` | `4.10%` | `4.10%` | `4.10%` | `PASS: 100% Match` |
| **Technology Sales Share** | `53.04%` | `53.04%` | `53.04%` | `53.04%` | `PASS: 100% Match` |

---

## 3. Key Mathematical Verification Insights for Interviews
1. **The Ratio vs Average Distinction:**
   - Notice how `Overall Profit Margin` is strictly evaluated as `SUM(profit) / SUM(sales)` across all tools.
   - If an analyst mistakenly averaged the row percentages, the result would be distorted due to unequal transaction sizing.
2. **Order Count Granularity:**
   - Multi-item orders mean `total rows (2,480)` does not equal `total orders (1,613)`.
   - Every tool explicitly used distinct order counting: `nunique()` in Python, `COUNT(DISTINCT order_id)` in SQL, and `DISTINCTCOUNT(order_id)` in DAX.

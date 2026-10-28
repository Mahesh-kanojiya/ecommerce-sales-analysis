# Excel Data Inspection & Analysis Guide

## 1. Role of Excel in the Analytics Lifecycle
In modern enterprise analytics, Excel is **not** meant for heavy, repetitive ETL scripting (which belongs in Python/SQL). Instead, Excel excels at:
- Rapid exploratory data inspection and sanity checks.
- Ad-hoc business validation and stakeholder discussions.
- Quick summary PivotTables and formula audits.

---

## 2. Step-by-Step Excel Inspection Workflow

### Step 1: Inspecting Rows, Columns, and Data Types
1. Open `data/raw/ecommerce_sales_raw.csv` in Excel.
2. Press `Ctrl + Home` to jump to cell `A1`.
3. Press `Ctrl + Shift + Down Arrow` to navigate to the bottom row (`2486` including headers).
4. Verify data types by checking alignment:
   - Text values (Customer Name, Category) align to the **left** by default.
   - Numeric and Date values (Sales, Quantity, Order Date) align to the **right** by default.
   - If an Order Date aligns to the left, it indicates it is stored as text rather than a native Excel serial date!

### Step 2: Checking Missing Values (Blanks)
1. Select the entire table (`Ctrl + A`).
2. Press `F5` (or `Ctrl + G`), click **Special...**, select **Blanks**, and click **OK**.
3. Excel highlights all blank cells (e.g., missing `Postal Code` in 15 rows).
4. **Formula Check:**
   ```excel
   =COUNTBLANK(L2:L2486)
   ```
   *Explanation:* Counts the number of empty cells in the Postal Code range.

### Step 3: Detecting Duplicate Records
1. **Highlight Duplicates with Conditional Formatting:**
   - Select Column B (`Order ID`).
   - Go to **Home > Conditional Formatting > Highlight Cells Rules > Duplicate Values**.
   - Notice that multiple rows highlight!
2. **Interview Distinction - Multi-Line Orders vs Duplicate Transactions:**
   - In e-commerce, multiple rows sharing the same `Order ID` are **valid line items** (e.g. an order containing both a Phone and an Office Chair).
   - Only records where *all* attributes (`Row ID`, `Order ID`, `Product ID`, `Sales`) are identical represent genuine duplicate errors.
   - **Formula to check frequency of an Order ID:**
     ```excel
     =COUNTIF($B$2:$B$2486, B2)
     ```
     *Explanation:* If the result is `> 1`, the order contains multiple items.

### Step 4: Identifying Trailing Spaces & Inconsistent Categories
1. Select Column O (`Category`) and click **Data > Filter** (`Ctrl + Shift + L`).
2. Open the filter dropdown list.
3. Notice that `Technology` appears multiple times as `"Technology"`, `"  Technology  "`, and `"Technology "`.
4. **Formula to test for non-standard length:**
   ```excel
   =LEN(O2)
   ```
   *Explanation:* If `"Technology"` has length 12 instead of 10, it contains hidden whitespace padding.
5. In Excel, the fix is `=TRIM(O2)`.

---

## 3. Essential Formulas Implemented in the Workbook

The workbook `excel/ecommerce_sales_analysis.xlsx` (Sheet `03_KPI_Formulas`) implements live dynamic formulas:

### 1. Total Revenue (Sales)
```excel
=SUM('02_Cleaned_Sales_Data'!R2:R2481)
```
- **Syntax:** `SUM(range)`
- **Plain English:** Adds up every dollar of revenue in the sales column.

### 2. Total Profit
```excel
=SUM('02_Cleaned_Sales_Data'!U2:U2481)
```
- **Syntax:** `SUM(range)`
- **Plain English:** Adds up all net profit values.

### 3. Total Units Sold
```excel
=SUM('02_Cleaned_Sales_Data'!S2:S2481)
```
- **Plain English:** Sums total quantity of physical units purchased.

### 4. Overall Profit Margin
```excel
=C4 / C3
```
- *(Where C4 is Total Profit and C3 is Total Revenue)*
- **Plain English:** Divides total net profit by total gross revenue.
- **Critical Interview Tip:** Never compute overall profit margin by averaging the `profit_margin_pct` column (`=AVERAGE(...)`), because averaging percentages ignores transaction dollar weights and creates mathematical distortion!

### 5. High-Discount Order Count
```excel
=COUNTIF('02_Cleaned_Sales_Data'!T2:T2481, ">=0.20")
```
- **Syntax:** `COUNTIF(range, criteria)`
- **Plain English:** Scans the discount column and counts rows where the discount is 20% or greater.

### 6. Loss-Making Transaction Count
```excel
=COUNTIF('02_Cleaned_Sales_Data'!U2:U2481, "<0")
```
- **Plain English:** Counts the number of transactions resulting in a negative profit.

### 7. Category Revenue via SUMIF
```excel
=SUMIF('02_Cleaned_Sales_Data'!$O$2:$O$2481, "Technology", '02_Cleaned_Sales_Data'!$R$2:$R$2481)
```
- **Syntax:** `SUMIF(criteria_range, criteria, sum_range)`
- **Plain English:** Checks column O for "Technology" and sums the corresponding values in column R.

### 8. Safe Lookup via IFERROR and VLOOKUP
```excel
=IFERROR(VLOOKUP("Technology", A15:D17, 4, FALSE), "Not Found")
```
- **Syntax:** `IFERROR(value, value_if_error)`
- **Plain English:** Looks up "Technology" in the summary table and returns its profit margin (column 4). If the value is missing or throws an error (`#N/A`), it safely outputs "Not Found" instead of breaking the worksheet.

---

## 4. Building PivotTables in Excel

1. Go to the sheet `02_Cleaned_Sales_Data` and click any cell.
2. Click **Insert > PivotTable** and select **New Worksheet**.
3. **Configure the Fields:**
   - Drag **`Region`** to **Rows**.
   - Drag **`Category`** to **Columns** (or nested under Rows).
   - Drag **`Sales`** to **Values** (summarized by `Sum`, formatted as `$#,##0`).
   - Drag **`Profit`** to **Values** (summarized by `Sum`, formatted as `$#,##0`).
4. **Add a Calculated Field for Profit Margin %:**
   - Click **PivotTable Analyze > Fields, Items, & Sets > Calculated Field**.
   - Name: `Profit_Margin_Pct`
   - Formula: `= Profit / Sales`
   - Format: `Percentage (0.00%)`
5. **Add a Slicer:**
   - Click **Insert Slicer > Order Year**, allowing the executive to filter between 2023 and 2024 with a single click.

---

## 5. Tool Comparison: Excel vs Python vs SQL

| Feature | Excel | Python (Pandas) | SQL (PostgreSQL) |
| :--- | :--- | :--- | :--- |
| **Best Used For** | Fast visual inspection, ad-hoc tables | Scalable ETL, automated cleaning, ML | Secure, centralized querying, database logic |
| **Max Capacity** | 1,048,576 rows | Millions of rows (RAM bound) | Billions of rows (Storage bound) |
| **Reproducibility** | Manual clicks risk human error | 100% reproducible script pipeline | 100% reproducible query scripts |
| **Duplicate Handling** | Manual `Remove Duplicates` dialog | Programmable `.drop_duplicates()` | `DISTINCT` / `ROW_NUMBER() OVER()` |
| **Collaboration** | Easy for business managers | Best for data engineers & analysts | Best for enterprise data warehouse |

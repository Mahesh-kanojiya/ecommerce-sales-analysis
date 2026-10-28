# Power BI Dashboard Build Instructions

## Executive Overview: E-Commerce Sales & Business Performance
This guide provides exact, step-by-step instructions to recreate the professional Executive Dashboard in Power BI Desktop from scratch.

---

## 1. Project Specifications & Design Palette

- **Canvas Size:** 16:9 Aspect Ratio (1920 × 1080 px or standard 1280 × 720 px)
- **Theme Palette:** Modern Executive Slate / Dark Navy
  - **Background:** Slate Charcoal (`#0F172A`) or Light Off-White (`#F8FAFC`)
  - **Card / Visual Container Fill:** Pure White (`#FFFFFF`) or Dark Card Slate (`#1E293B`)
  - **Primary Brand Color (Revenue):** Royal / Electric Blue (`#2563EB` or `#3B82F6`)
  - **Success / Positive Profit:** Emerald Green (`#10B981`)
  - **Alert / Loss / Negative Profit:** Crimson Coral (`#EF4444`)
  - **Neutral / Secondary:** Cool Slate Gray (`#64748B`)
- **Typography:** Segoe UI or Aptos (Clean, modern sans-serif)

---

## 2. Step 1: Connecting to Data in Power BI Desktop

### Option A: Direct PostgreSQL Connection
1. Open Power BI Desktop.
2. Click **Get Data > PostgreSQL database**.
3. Server: `localhost:5432`, Database: `ecommerce_db`.
4. Data Connectivity mode: Select **Import** (recommended for sub-100K transaction datasets for maximum speed and DAX flexibility).
5. Enter credentials if prompted, select table `sales_orders`, and click **Load**.

### Option B: Cleaned CSV Ingestion (Zero-Friction Fallback)
1. In Power BI Desktop, click **Get Data > Text/CSV**.
2. Browse to `data/processed/cleaned_sales_data.csv`.
3. In the preview window, ensure data types are correct:
   - `order_date`, `ship_date`: Date
   - `sales`, `profit`, `cost`: Decimal number
   - `quantity`, `row_id`: Whole number
   - `discount`: Decimal number (formatted as percentage)
4. Click **Load**.
5. Rename the table to `sales_orders`.

---

## 3. Step 2: Creating the Date Dimension Table (Best Practice)

In professional Power BI development, Time Intelligence requires a continuous calendar table:
1. In Power BI Desktop, click **Modeling > New Table**.
2. Paste the following DAX formula:
   ```dax
   DateTable = 
   VAR MinDate = MIN(sales_orders[order_date])
   VAR MaxDate = MAX(sales_orders[order_date])
   RETURN
   ADDCOLUMNS(
       CALENDAR(MinDate, MaxDate),
       "Year", YEAR([Date]),
       "Year Month", FORMAT([Date], "YYYY-MM"),
       "Month Name", FORMAT([Date], "MMMM"),
       "Month Number", MONTH([Date]),
       "Quarter", "Q" & FORMAT([Date], "Q"),
       "Year Quarter", FORMAT([Date], "YYYY") & " Q" & FORMAT([Date], "Q")
   )
   ```
3. Mark as Date Table: Right-click `DateTable` in data pane > **Mark as date table** > Select column `Date`.
4. Switch to **Model View**:
   - Drag `DateTable[Date]` to `sales_orders[order_date]`.
   - Cardinality: **One to Many (1 : \*)**, Cross filter direction: **Single**.

---

## 4. Step 3: Creating a Dedicated Measures Table

1. On the **Home** tab, click **Enter Data**.
2. Name the table `_AllMeasures` and click **Load**.
3. Create each measure from `powerbi/measures.dax` inside `_AllMeasures`:
   - `Total Revenue = SUM(sales_orders[sales])` (Format: `$#,##0.00`)
   - `Total Profit = SUM(sales_orders[profit])` (Format: `$#,##0.00`)
   - `Total Orders = DISTINCTCOUNT(sales_orders[order_id])` (Format: `#,##0`)
   - `Total Units Sold = SUM(sales_orders[quantity])` (Format: `#,##0`)
   - `Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)` (Format: `0.0%`)
   - `Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)` (Format: `$#,##0.00`)
4. Hide the dummy `Column1` in `_AllMeasures`.

---

## 5. Step 4: Canvas Layout & Visual Hierarchy

```
+----------------------------------------------------------------------------------------------------+
|  LOGO / TITLE: Executive E-Commerce Sales & Business Performance Dashboard   [DATE] [CAT] [REGION] |
+----------------------------------------------------------------------------------------------------+
| [ KPI 1: REVENUE ]  [ KPI 2: PROFIT ]  [ KPI 3: ORDERS ]  [ KPI 4: UNITS ]  [ KPI 5: MARGIN % ]    |
|   $1,520,482            $262,364             1,613             6,748              17.3%            |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 1: Monthly Sales & Profit Trend (2023-24)|  VISUAL 2: Category Sales vs Profit Margin      |
|  (Line and Clustered Column Chart)               |  (Clustered Bar Chart)                          |
|                                                  |                                                 |
+--------------------------------------------------+-------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 3: Top 10 Products by Revenue            |  VISUAL 4: Loss-Making Products (Bottom Profit) |
|  (Horizontal Bar Chart - Cash Cows)              |  (Horizontal Bar Chart - Margin Bleeders)       |
|                                                  |                                                 |
+--------------------------------------------------+-------------------------------------------------+
|  VISUAL 5: Regional Sales & Profit Comparison (Donut or Clustered Column Chart)                    |
+----------------------------------------------------------------------------------------------------+
```

### Detailed Component Build Steps:

#### A. Header & Global Filters (Top Section)
1. **Title Text Box:** "Executive E-Commerce Sales & Business Performance Analysis" (20pt Bold).
2. **Slicer 1 (Date Range):** Field: `DateTable[Date]`. Slicer style: **Between** (Slider).
3. **Slicer 2 (Category):** Field: `sales_orders[category]`. Slicer style: **Tile** or **Dropdown**.
4. **Slicer 3 (Region):** Field: `sales_orders[region]`. Slicer style: **Dropdown** with "Select All" enabled.

#### B. KPI Cards (Row 1)
Use the **Card** or **New Card (Visual)**:
1. **Card 1 (Total Revenue):** Measure: `[Total Revenue]`. Display units: Auto (displays `$1.52M`).
2. **Card 2 (Total Profit):** Measure: `[Total Profit]`. Display units: Auto (displays `$262.4K`).
3. **Card 3 (Total Orders):** Measure: `[Total Orders]`. Display units: None (displays `1,613`).
4. **Card 4 (Total Units Sold):** Measure: `[Total Units Sold]`. Display units: None (displays `6,748`).
5. **Card 5 (Profit Margin):** Measure: `[Profit Margin %]`. Format: `17.3%`.

#### C. Visual 1: Monthly Sales & Profit Trend (Middle-Left)
- **Visual Type:** **Line and Clustered Column Chart**.
- **X-Axis:** `DateTable[Year Month]` (Sorted chronologically).
- **Column Y-Axis (Sales):** `[Total Revenue]` (Bar color: Electric Blue `#3B82F6`).
- **Line Y-Axis (Profit):** `[Total Profit]` (Line color: Emerald Green `#10B981`, stroke width 3, markers enabled).
- **Title:** "Monthly Sales & Profit Trajectory (Seasonal Peaks Highlighted)".

#### D. Visual 2: Category Sales & Profit Margin (Middle-Right)
- **Visual Type:** **Clustered Bar Chart** or **Dual Axis Chart**.
- **Y-Axis:** `sales_orders[category]`.
- **X-Axis:** `[Total Revenue]` and `[Total Profit]`.
- **Colors:** Revenue: Blue, Profit: Green.
- **Data Labels:** On (Inside End).
- **Title:** "Category Performance: Revenue vs Net Profit Contribution".

#### E. Visual 3: Top 10 Products by Revenue (Bottom-Left)
- **Visual Type:** **Clustered Bar Chart (Horizontal)**.
- **Y-Axis:** `sales_orders[product_name]`.
- **X-Axis:** `[Total Revenue]`.
- **Filter Pane:** Filter on `product_name` > Filter type: **Top N** > Show top **10** items by `[Total Revenue]`.
- **Title:** "Top 10 Revenue-Generating Flagship Products".

#### F. Visual 4: Loss-Making Products / Margin Bleeders (Bottom-Right)
- **Visual Type:** **Clustered Bar Chart (Horizontal)**.
- **Y-Axis:** `sales_orders[product_name]`.
- **X-Axis:** `[Total Profit]`.
- **Filter Pane:** Filter on `product_name` > Filter type: **Bottom N** > Show bottom **5** items by `[Total Profit]`.
- **Color:** Dynamic conditional formatting or solid Crimson Alert (`#EF4444`).
- **Title:** "Margin Erosion: Heavily Discounted Loss-Making Products".

#### G. Visual 5: Regional Performance Breakdown (Bottom Banner)
- **Visual Type:** **Clustered Column Chart** or **Donut Chart**.
- **X-Axis:** `sales_orders[region]`.
- **Y-Axis:** `[Total Revenue]`, `[Total Profit]`.
- **Tooltip:** Add `[Average Discount %]` to reveal Central region discount disparity.
- **Title:** "Regional Revenue & Profitability (West & East vs Central)".

---

## 6. Verification Checklist for Freshers in Interviews

| Metric | Power BI Target | SQL Verified Value | Excel Formula Value |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | `$1,520,482.40` | `$1,520,482.40` | `$1,520,482.40` |
| **Total Profit** | `$262,363.90` | `$262,363.90` | `$262,363.90` |
| **Total Orders** | `1,613` | `1,613` | `1,613` |
| **Units Sold** | `6,748` | `6,748` | `6,748` |
| **Profit Margin**| `17.26%` | `17.26%` | `17.26%` |

# Data Dictionary: E-Commerce Sales & Business Performance

## 1. Dataset Overview & Provenance
- **Dataset Name:** E-Commerce Retail Sales Transactions (2023–2024)
- **Source & Benchmark:** Curated synthetic dataset modeled after the industry-standard Global Superstore retail benchmark schema.
- **License / Usage:** Open access for educational, academic, and portfolio demonstration purposes (Creative Commons CC-BY 4.0 style).
- **Timeframe:** January 1, 2023 – December 31, 2024 (2 full calendar years).
- **Dataset Granularity:** **Order Line-Item level**. Each record represents a single product purchased within an order. An order can contain multiple line items.
- **Total Raw Records:** 2,485 rows.
- **Total Columns:** 21 attributes.

---

## 2. Column Specifications & Data Dictionary

| Column Name | Raw Data Type | Cleaned Data Type | Description | Example Values | Business Rules & Validation Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Row ID` | Integer | Integer | Unique surrogate row identifier for data auditing | `1`, `1042`, `2485` | Must be positive, consecutive integers. |
| `Order ID` | Text / String | String | Unique transaction / invoice identifier | `ORD-1002`, `ORD-1450` | One `Order ID` can appear multiple times for multi-product orders. |
| `Order Date` | String (Mixed) | Date (`YYYY-MM-DD`) | Date when customer placed the transaction | `2023-05-14`, `14/05/2023` | Cleaned into standard ISO format. Must be `<= Ship Date`. |
| `Ship Date` | String | Date (`YYYY-MM-DD`) | Date when order was dispatched from fulfillment center | `2023-05-18` | Must be on or after `Order Date`. |
| `Ship Mode` | String | String | Fulfillment shipping tier selected by customer | `Standard Class`, `Second Class`, `First Class`, `Same Day` | Standard lead times: Same Day (0d), First (2d), Second (3d), Standard (4d). |
| `Customer ID` | String | String | Unique permanent identifier for customer | `CUST-1042`, `CUST-1399` | 450 unique customers across the 2-year period. |
| `Customer Name`| String | String | Full name of the customer | `James Smith`, `Sarah Miller` | High-value attribute for customer segmentation. |
| `Segment` | String | String | Customer market classification | `Consumer`, `Corporate`, `Home Office` | Standard retail customer segmentation. |
| `Country` | String | String | Country of transaction | `United States` | Single-country dataset for focused regional analysis. |
| `City` | String | String | Delivery destination city | `New York`, `Los Angeles`, `Chicago` | Used for geographical drilldowns. |
| `State` | String | String | Delivery destination state | `California`, `Texas`, `New York` | Aggregates to administrative state performance. |
| `Postal Code` | String / Float | String | 5-digit ZIP code | `10001`, `90001`, `NaN` | Handled as string to preserve leading zeros; missing codes imputed/flagged. |
| `Region` | String | String | Major sales territory | `East`, `West`, `Central`, `South` | Primary geographical sales hierarchy. |
| `Product ID` | String | String | Unique Stock Keeping Unit (SKU) identifier | `PROD-TEC-PHO-101` | Format encodes Category and Sub-Category prefix. |
| `Category` | String | String | Top-level product division | `Technology`, `Furniture`, `Office Supplies` | Trimmed of accidental leading/trailing spaces during cleaning. |
| `Sub-Category` | String | String | Specific product grouping under Category | `Phones`, `Chairs`, `Tables`, `Storage`, etc. | 14 distinct sub-categories. |
| `Product Name` | String | String | Commercial product catalog description | `Apple iPhone 14 128GB`, `Herman Miller Aeron` | Identifies specific merchandise. |
| `Sales` | Float | Float (Numeric 10,2) | Net transaction revenue after discount ($ USD) | `799.00`, `45.60` | Formula: `Quantity * Unit_Price * (1 - Discount)`. |
| `Quantity` | Integer | Integer | Number of units ordered | `1`, `4`, `8` | Must be strictly positive integer (`Quantity >= 1`). |
| `Discount` | Float | Float (Numeric 4,2) | Promotional price reduction rate (0.0 to 1.0) | `0.00`, `0.15`, `0.30` | Valid range: `0.0 <= Discount < 1.0` (100%). |
| `Profit` | Float | Float (Numeric 10,2) | Net financial margin on the transaction ($ USD) | `219.00`, `-45.20` | Formula: `Sales - Total_Cost`. Can be negative on discounted items! |

---

## 3. Key Derived Metrics (Calculated in Python / SQL / Power BI)

1. **Total Revenue / Sales:**
   $$\text{Total Sales} = \sum \text{Sales}$$
2. **Total Profit:**
   $$\text{Total Profit} = \sum \text{Profit}$$
3. **Total Orders:**
   $$\text{Total Orders} = \text{COUNT}(\text{DISTINCT } \text{Order ID})$$
   *(Note: Never use `COUNT(Row ID)` for orders because multi-item orders have multiple rows!)*
4. **Total Units Sold:**
   $$\text{Total Units Sold} = \sum \text{Quantity}$$
5. **Profit Margin (%):**
   $$\text{Profit Margin} = \frac{\text{Total Profit}}{\text{Total Sales}} \times 100$$
   *(Crucial interview point: Profit margin is an **aggregate ratio**, never an average of row percentages!)*
6. **Average Order Value (AOV):**
   $$\text{AOV} = \frac{\text{Total Sales}}{\text{Total Orders}}$$

# SQL Business Intelligence Analysis Summary

This document presents the verified outputs of the 12 core SQL queries run against the cleaned sales orders database.

---

## Query 1: Total Revenue
**Business Question:** What is the total gross revenue generated?

```sql
SELECT ROUND(SUM(sales), 2) AS total_revenue FROM sales_orders;
```

|   total_revenue |
|----------------:|
|     1.52048e+06 |

---

## Query 2: Total Profit & Margin
**Business Question:** What is the net profit and overall profit margin?

```sql
SELECT ROUND(SUM(profit), 2) AS total_profit,
                   ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS overall_profit_margin_pct
            FROM sales_orders;
```

|   total_profit |   overall_profit_margin_pct |
|---------------:|----------------------------:|
|         262364 |                       17.26 |

---

## Query 3: Total Orders
**Business Question:** How many distinct customer orders were placed?

```sql
SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales_orders;
```

|   total_orders |
|---------------:|
|           1613 |

---

## Query 4: Units Sold & Basket Size
**Business Question:** What is the total volume of units sold and average basket size?

```sql
SELECT SUM(quantity) AS total_units_sold,
                   ROUND(CAST(SUM(quantity) AS REAL) / COUNT(DISTINCT order_id), 2) AS avg_items_per_order
            FROM sales_orders;
```

|   total_units_sold |   avg_items_per_order |
|-------------------:|----------------------:|
|               6748 |                  4.18 |

---

## Query 5: Monthly Sales Trends (Sample)
**Business Question:** How do sales and profit trend month by month? (First 6 months preview)

```sql
SELECT order_month,
                   COUNT(DISTINCT order_id) AS orders_count,
                   ROUND(SUM(sales), 2) AS monthly_sales,
                   ROUND(SUM(profit), 2) AS monthly_profit,
                   ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
            FROM sales_orders
            GROUP BY order_month
            ORDER BY order_month ASC
            LIMIT 6;
```

| order_month   |   orders_count |   monthly_sales |   monthly_profit |   profit_margin_pct |
|:--------------|---------------:|----------------:|-----------------:|--------------------:|
| 2023-01       |             53 |         48986.5 |         11480    |               23.44 |
| 2023-02       |             60 |         60560.3 |         13013.3  |               21.49 |
| 2023-03       |             71 |         84724.6 |         14938    |               17.63 |
| 2023-04       |             54 |         46489.3 |          9632.35 |               20.72 |
| 2023-05       |             80 |         69474.5 |         11524    |               16.59 |
| 2023-06       |             54 |         50035.9 |         10058.4  |               20.1  |

---

## Query 6: Category-Wise Sales Contribution
**Business Question:** Which product category drives the highest revenue?

```sql
SELECT category,
                   COUNT(DISTINCT order_id) AS orders_count,
                   SUM(quantity) AS total_units,
                   ROUND(SUM(sales), 2) AS category_sales,
                   ROUND((SUM(sales) / (SELECT SUM(sales) FROM sales_orders)) * 100, 2) AS sales_contrib_pct
            FROM sales_orders
            GROUP BY category
            ORDER BY category_sales DESC;
```

| category        |   orders_count |   total_units |   category_sales |   sales_contrib_pct |
|:----------------|---------------:|--------------:|-----------------:|--------------------:|
| Technology      |            689 |          2213 |         806503   |               53.04 |
| Furniture       |            645 |          2004 |         615131   |               40.46 |
| Office Supplies |            772 |          2531 |          98848.1 |                6.5  |

---

## Query 7: Category Profit & Profit Margin
**Business Question:** How do category profits compare against their revenue and discount rates?

```sql
SELECT category,
                   ROUND(SUM(sales), 2) AS total_sales,
                   ROUND(SUM(profit), 2) AS total_profit,
                   ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
                   ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
            FROM sales_orders
            GROUP BY category
            ORDER BY total_profit DESC;
```

| category        |   total_sales |   total_profit |   profit_margin_pct |   avg_discount_pct |
|:----------------|--------------:|---------------:|--------------------:|-------------------:|
| Technology      |      806503   |       197882   |               24.54 |               6.82 |
| Office Supplies |       98848.1 |        39271.6 |               39.73 |               7.56 |
| Furniture       |      615131   |        25210.2 |                4.1  |              12.65 |

---

## Query 8: Top 10 Products by Revenue
**Business Question:** Which top 10 products generate the most revenue?

```sql
SELECT product_name, category,
                   SUM(quantity) AS units_sold,
                   ROUND(SUM(sales), 2) AS total_revenue,
                   ROUND(SUM(profit), 2) AS total_profit,
                   ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_pct
            FROM sales_orders
            GROUP BY product_name, category
            ORDER BY total_revenue DESC
            LIMIT 10;
```

| product_name                         | category   |   units_sold |   total_revenue |   total_profit |   margin_pct |
|:-------------------------------------|:-----------|-------------:|----------------:|---------------:|-------------:|
| HP Color LaserJet Enterprise M555dn  | Technology |          185 |        156471   |        41770.9 |        26.7  |
| Samsung Galaxy S23 128GB             | Technology |          163 |        114672   |        26651.9 |        23.24 |
| Steelcase Gesture Office Chair       | Furniture  |          139 |        110458   |        25667.5 |        23.24 |
| Herman Miller Aeron Ergonomic Chair  | Furniture  |          115 |        106614   |        23814.2 |        22.34 |
| Apple iPhone 14 128GB                | Technology |          131 |         96399.4 |        20419.3 |        21.18 |
| Google Pixel 7 128GB                 | Technology |          171 |         95241   |        23421   |        24.59 |
| Chromcraft Rectangular Dining Table  | Furniture  |          157 |         89622   |       -21848   |       -24.38 |
| Sony WH-1000XM5 Headphones           | Technology |          182 |         65695.4 |        16555.3 |        25.2  |
| Balt Standing Adjustable Table       | Furniture  |          176 |         65234   |       -17486   |       -26.81 |
| Canon imageCLASS D1620 Multifunction | Technology |          115 |         65051.4 |        17901.4 |        27.52 |

---

## Query 9: Bottom 10 Products by Profit (Loss-Makers)
**Business Question:** Which products generate the greatest financial losses?

```sql
SELECT product_name, category,
                   SUM(quantity) AS units_sold,
                   ROUND(SUM(sales), 2) AS total_revenue,
                   ROUND(SUM(profit), 2) AS total_loss,
                   ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
            FROM sales_orders
            GROUP BY product_name, category
            HAVING SUM(profit) < 0
            ORDER BY total_loss ASC
            LIMIT 10;
```

| product_name                          | category   |   units_sold |   total_revenue |   total_loss |   avg_discount_pct |
|:--------------------------------------|:-----------|-------------:|----------------:|-------------:|-------------------:|
| Chromcraft Rectangular Dining Table   | Furniture  |          157 |           89622 |       -21848 |              26.45 |
| Balt Standing Adjustable Table        | Furniture  |          176 |           65234 |       -17486 |              29.05 |
| Bevis Training Table 60x30            | Furniture  |          130 |           38010 |       -12690 |              31.14 |
| Bush Furniture Conference Table (Oak) | Furniture  |          110 |           52910 |       -10890 |              26.46 |

---

## Query 10: Regional Sales Performance
**Business Question:** How do geographic regions compare in sales and profitability?

```sql
SELECT region,
                   COUNT(DISTINCT order_id) AS total_orders,
                   ROUND(SUM(sales), 2) AS regional_sales,
                   ROUND(SUM(profit), 2) AS regional_profit,
                   ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
                   ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
            FROM sales_orders
            GROUP BY region
            ORDER BY regional_profit DESC;
```

| region   |   total_orders |   regional_sales |   regional_profit |   profit_margin_pct |   avg_discount_pct |
|:---------|---------------:|-----------------:|------------------:|--------------------:|-------------------:|
| West     |            515 |           474098 |           90617.8 |               19.11 |               6.22 |
| East     |            485 |           448234 |           87587.4 |               19.54 |               6.58 |
| Central  |            363 |           346229 |           43958.7 |               12.7  |              17.01 |
| South    |            250 |           251920 |           40200   |               15.96 |               7.06 |

---

## Query 11: Month-over-Month (MoM) Growth via LAG()
**Business Question:** What is the month-over-month growth velocity using window functions? (First 8 months)

```sql
WITH MonthlySales AS (
                SELECT order_month,
                       ROUND(SUM(sales), 2) AS current_month_sales
                FROM sales_orders
                GROUP BY order_month
            )
            SELECT order_month,
                   current_month_sales,
                   LAG(current_month_sales, 1) OVER (ORDER BY order_month) AS prior_month_sales,
                   ROUND(
                       ((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY order_month)) /
                        LAG(current_month_sales, 1) OVER (ORDER BY order_month)) * 100, 2
                   ) AS mom_growth_pct
            FROM MonthlySales
            ORDER BY order_month ASC
            LIMIT 8;
```

| order_month   |   current_month_sales |   prior_month_sales |   mom_growth_pct |
|:--------------|----------------------:|--------------------:|-----------------:|
| 2023-01       |               48986.5 |               nan   |           nan    |
| 2023-02       |               60560.3 |             48986.5 |            23.63 |
| 2023-03       |               84724.6 |             60560.3 |            39.9  |
| 2023-04       |               46489.3 |             84724.6 |           -45.13 |
| 2023-05       |               69474.5 |             46489.3 |            49.44 |
| 2023-06       |               50035.9 |             69474.5 |           -27.98 |
| 2023-07       |               50450.1 |             50035.9 |             0.83 |
| 2023-08       |               48487.8 |             50450.1 |            -3.89 |

---

## Query 12: Ranking Sub-Categories within Category via DENSE_RANK()
**Business Question:** How do sub-categories rank by profit inside their parent category?

```sql
WITH SubCatSummary AS (
                SELECT category, sub_category,
                       ROUND(SUM(sales), 2) AS subcat_sales,
                       ROUND(SUM(profit), 2) AS subcat_profit,
                       ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_pct
                FROM sales_orders
                GROUP BY category, sub_category
            )
            SELECT category, sub_category, subcat_sales, subcat_profit, margin_pct,
                   DENSE_RANK() OVER (PARTITION BY category ORDER BY subcat_profit DESC) AS profit_rank
            FROM SubCatSummary
            ORDER BY category, profit_rank;
```

| category        | sub_category   |   subcat_sales |   subcat_profit |   margin_pct |   profit_rank |
|:----------------|:---------------|---------------:|----------------:|-------------:|--------------:|
| Furniture       | Chairs         |       270106   |         62470.8 |        23.13 |             1 |
| Furniture       | Bookcases      |        73859.5 |         16109.5 |        21.81 |             2 |
| Furniture       | Furnishings    |        25390   |          9544   |        37.59 |             3 |
| Furniture       | Tables         |       245776   |        -62914   |       -25.6  |             4 |
| Office Supplies | Storage        |        26245.6 |         11932.6 |        45.47 |             1 |
| Office Supplies | Appliances     |        37475   |         10970   |        29.27 |             2 |
| Office Supplies | Paper          |        15660.5 |          6638.5 |        42.39 |             3 |
| Office Supplies | Art            |        11824.2 |          6101.2 |        51.6  |             4 |
| Office Supplies | Binders        |         7642.8 |          3629.3 |        47.49 |             5 |
| Technology      | Phones         |       335308   |         76628.3 |        22.85 |             1 |
| Technology      | Copiers        |       221522   |         59672.3 |        26.94 |             2 |
| Technology      | Machines       |       155037   |         32196.7 |        20.77 |             3 |
| Technology      | Accessories    |        94635.7 |         29384.7 |        31.05 |             4 |

---

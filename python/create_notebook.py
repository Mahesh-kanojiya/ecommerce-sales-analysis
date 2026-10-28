"""
Script to generate 01_data_cleaning_and_eda.ipynb
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title & Context
cells.append(nbf.v4.new_markdown_cell("""# E-Commerce Sales Analysis: Data Cleaning & Exploratory Data Analysis (EDA)
**Author:** Senior Data Analyst & Technical Mentor  
**Objective:** Load raw transaction data, perform data quality auditing, execute systematic cleaning, engineer analytical features, and perform initial exploratory data analysis.

---
### Workflow Architecture:
1. **Load Raw Data & Inspect Schema**
2. **Data Quality Audit (Nulls, Duplicates, Trailing Spaces, Anomalies)**
3. **Data Cleaning & Standardization**
4. **Feature Engineering (Dates, Financial Margins, Lead Times)**
5. **Exploratory Data Analysis (Visualizations)**
6. **Export Cleaned Dataset for PostgreSQL & Power BI**
"""))

# Cell 1: Imports
cells.append(nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["font.size"] = 11

print("Libraries imported successfully!")
"""))

# Cell 2: Load Data
cells.append(nbf.v4.new_markdown_cell("""## Step 1: Load Raw Dataset & Inspect Structure"""))
cells.append(nbf.v4.new_code_cell("""raw_data_path = os.path.join("..", "data", "raw", "ecommerce_sales_raw.csv")
df_raw = pd.read_csv(raw_data_path)

print(f"Dataset Shape: {df_raw.shape[0]:,} rows, {df_raw.shape[1]} columns")
df_raw.head(5)
"""))

# Cell 3: Data Quality Audit
cells.append(nbf.v4.new_markdown_cell("""## Step 2: Comprehensive Data Quality Audit

In interviews, always emphasize that you **never delete data silently**. Every check must be measured and documented:
1. Missing values (`.isnull().sum()`)
2. Exact duplicate records vs repeated `Order ID` (multi-item orders)
3. String whitespace in categorical attributes
4. Value boundaries (e.g. negative quantities or impossible discount rates)
"""))
cells.append(nbf.v4.new_code_cell("""# 1. Missing Values
print("--- Missing Values ---")
print(df_raw.isnull().sum()[df_raw.isnull().sum() > 0])

# 2. Duplicate Audit
exact_dups = df_raw.duplicated().sum()
repeated_order_ids = df_raw.duplicated(subset=['Order ID']).sum()
print(f"\\nExact duplicate rows: {exact_dups}")
print(f"Repeated Order IDs (Valid Multi-item orders): {repeated_order_ids}")

# 3. Category Whitespace Check
print("\\nDistinct Categories (Notice trailing/leading spaces):")
print(df_raw['Category'].unique())

# 4. Outliers & Invalid Values
print("\\nNegative or zero quantities:", (df_raw['Quantity'] <= 0).sum())
print("Discounts >= 100%:", (df_raw['Discount'] >= 1.0).sum())
"""))

# Cell 4: Execute Cleaning
cells.append(nbf.v4.new_markdown_cell("""## Step 3: Execute Systematic Cleaning Transformations"""))
cells.append(nbf.v4.new_code_cell("""df_clean = df_raw.copy()

# A. Drop exact duplicate rows
df_clean = df_clean.drop_duplicates()

# B. Trim whitespace across all string columns
string_cols = ['Ship Mode', 'Customer Name', 'Segment', 'Country', 
               'City', 'State', 'Region', 'Category', 'Sub-Category', 'Product Name']
for col in string_cols:
    df_clean[col] = df_clean[col].astype(str).str.strip()

# C. Impute missing Postal Codes
df_clean['Postal Code'] = df_clean['Postal Code'].fillna('Unknown').astype(str).str.replace(r'\\.0$', '', regex=True)

# D. Standardize Dates to ISO YYYY-MM-DD
df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'], format='mixed').dt.strftime('%Y-%m-%d')
df_clean['Ship Date'] = pd.to_datetime(df_clean['Ship Date'], format='mixed').dt.strftime('%Y-%m-%d')

# E. Filter invalid business records
valid_mask = (df_clean['Quantity'] > 0) & (df_clean['Discount'] < 1.0) & (df_clean['Sales'] > 0)
df_clean = df_clean[valid_mask].copy()

# Reset Row ID
df_clean['Row ID'] = range(1, len(df_clean) + 1)

print(f"Cleaned dataset rows: {len(df_clean):,}")
print("Distinct Clean Categories:", df_clean['Category'].unique())
"""))

# Cell 5: Feature Engineering
cells.append(nbf.v4.new_markdown_cell("""## Step 4: Analytical Feature Engineering"""))
cells.append(nbf.v4.new_code_cell("""order_dt = pd.to_datetime(df_clean['Order Date'])
ship_dt = pd.to_datetime(df_clean['Ship Date'])

df_clean['Order Year'] = order_dt.dt.year
df_clean['Order Month'] = order_dt.dt.strftime('%Y-%m')
df_clean['Order Month Name'] = order_dt.dt.strftime('%B')
df_clean['Order Quarter'] = 'Q' + order_dt.dt.quarter.astype(str)
df_clean['Cost'] = (df_clean['Sales'] - df_clean['Profit']).round(2)
df_clean['Profit Margin Pct'] = ((df_clean['Profit'] / df_clean['Sales']) * 100).round(2)
df_clean['Shipping Days'] = (ship_dt - order_dt).dt.days

df_clean[['Order ID', 'Order Date', 'Order Month', 'Sales', 'Cost', 'Profit', 'Profit Margin Pct']].head(5)
"""))

# Cell 6: Visual EDA
cells.append(nbf.v4.new_markdown_cell("""## Step 5: Exploratory Data Analysis & Visualizations"""))
cells.append(nbf.v4.new_code_cell("""# Visual 1: Monthly Sales & Profit Trend
monthly_summary = df_clean.groupby('Order Month')[['Sales', 'Profit']].sum().reset_index()

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

ax1.plot(monthly_summary['Order Month'], monthly_summary['Sales'] / 1000, color='#1f77b4', marker='o', linewidth=2.5, label='Sales ($K)')
ax2.plot(monthly_summary['Order Month'], monthly_summary['Profit'] / 1000, color='#2ca02c', marker='s', linewidth=2.5, linestyle='--', label='Profit ($K)')

ax1.set_xlabel('Order Month', fontweight='bold')
ax1.set_ylabel('Sales ($ in Thousands)', color='#1f77b4', fontweight='bold')
ax2.set_ylabel('Profit ($ in Thousands)', color='#2ca02c', fontweight='bold')
ax1.set_xticklabels(monthly_summary['Order Month'], rotation=45)
plt.title('Monthly Sales & Profit Performance (2023 - 2024)', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Visual 2: Sales and Profit by Category
cat_summary = df_clean.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
cat_summary['Profit Margin %'] = (cat_summary['Profit'] / cat_summary['Sales']) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=cat_summary, x='Category', y='Sales', ax=ax1, palette='Blues_d')
ax1.set_title('Total Revenue by Category ($)', fontweight='bold')
ax1.set_ylabel('Revenue ($)')

sns.barplot(data=cat_summary, x='Category', y='Profit Margin %', ax=ax2, palette='Greens_d')
ax2.set_title('Profit Margin % by Category', fontweight='bold')
ax2.set_ylabel('Margin (%)')

plt.tight_layout()
plt.show()
"""))

# Cell 7: Summary Metrics
cells.append(nbf.v4.new_markdown_cell("""## Step 6: Summary Metrics for Database Cross-Validation"""))
cells.append(nbf.v4.new_code_cell("""print("=" * 50)
print("GROUND TRUTH METRICS FOR SQL & POWER BI:")
print(f"Total Revenue:       ${df_clean['Sales'].sum():,.2f}")
print(f"Total Profit:        ${df_clean['Profit'].sum():,.2f}")
print(f"Total Orders:        {df_clean['Order ID'].nunique():,}")
print(f"Total Units Sold:    {df_clean['Quantity'].sum():,}")
print(f"Total Profit Margin: {(df_clean['Profit'].sum() / df_clean['Sales'].sum()) * 100:.2f}%")
print("=" * 50)
"""))

nb.cells = cells

with open("notebooks/01_data_cleaning_and_eda.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Created notebooks/01_data_cleaning_and_eda.ipynb successfully!")

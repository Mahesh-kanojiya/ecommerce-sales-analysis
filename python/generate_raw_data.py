"""
Generate Raw E-Commerce Sales Dataset
Author: Senior Data Analyst & Technical Mentor
Description:
    Generates a realistic, industry-standard retail e-commerce sales dataset
    modeled on the Global Superstore benchmark schema (~2,500 transactions).
    Includes intentional, controlled real-world data quality issues
    to demonstrate professional data cleaning workflows in Excel and Python.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set fixed random seed for 100% reproducibility across all tools
np.random.seed(42)
random.seed(42)

def generate_dataset():
    # Catalog definition: Category -> Sub-Categories -> Products with base pricing
    catalog = {
        "Technology": {
            "Phones": [
                ("Apple iPhone 14 128GB", 799.0, 580.0),
                ("Samsung Galaxy S23 128GB", 749.0, 540.0),
                ("Google Pixel 7 128GB", 599.0, 420.0),
                ("Motorola Moto G Stylus", 249.0, 180.0),
            ],
            "Accessories": [
                ("Logitech MX Master 3S Mouse", 99.0, 55.0),
                ("Anker USB-C Hub 7-in-1", 49.0, 24.0),
                ("SanDisk 128GB Extreme MicroSD", 25.0, 11.0),
                ("Sony WH-1000XM5 Headphones", 399.0, 270.0),
            ],
            "Machines": [
                ("Brother HL-L2350DW Laser Printer", 149.0, 110.0),
                ("Epson EcoTank ET-2800", 229.0, 165.0),
                ("HP LaserJet Pro MFP 4101fdw", 449.0, 340.0),
                ("Zebra Thermal Label Printer", 289.0, 210.0),
            ],
            "Copiers": [
                ("Canon imageCLASS D1620 Multifunction", 599.0, 410.0),
                ("HP Color LaserJet Enterprise M555dn", 899.0, 620.0),
            ]
        },
        "Furniture": {
            "Chairs": [
                ("Herman Miller Aeron Ergonomic Chair", 995.0, 720.0),
                ("Steelcase Gesture Office Chair", 850.0, 610.0),
                ("HON Exposure Mesh Task Chair", 220.0, 150.0),
                ("Alera Elusion Swivel Chair", 160.0, 115.0),
            ],
            "Tables": [
                ("Bush Furniture Conference Table (Oak)", 650.0, 580.0),  # High cost, vulnerable to discount loss
                ("Bevis Training Table 60x30", 420.0, 390.0),
                ("Balt Standing Adjustable Table", 520.0, 470.0),
                ("Chromcraft Rectangular Dining Table", 780.0, 710.0),
            ],
            "Bookcases": [
                ("Sauder 5-Shelf Wood Bookcase", 180.0, 130.0),
                ("Bush Furniture Cabot Bookcase", 260.0, 195.0),
                ("O’Sullivan 3-Shelf Bookcase", 110.0, 75.0),
            ],
            "Furnishings": [
                ("Tenex Floor Mat 46x60", 65.0, 40.0),
                ("Eldon Executive Desk Pad", 35.0, 18.0),
                ("Luxo L-1 Task Lamp", 85.0, 50.0),
            ]
        },
        "Office Supplies": {
            "Storage": [
                ("Fellowes Bankers Box 12-Pack", 45.0, 22.0),
                ("Iris 4-Drawer Mobile Storage Cart", 60.0, 32.0),
                ("Akro-Mils 24-Drawer Cabinet", 42.0, 21.0),
                ("Sterilite 66 Qt Latch Box 4-Pack", 55.0, 28.0),
            ],
            "Binders": [
                ("Wilson Jones Heavy Duty 3-Inch Binder", 18.0, 9.0),
                ("Avery Durable View Binder 1-Inch", 6.0, 2.5),
                ("GBC VeloBind System Covers", 32.0, 16.0),
            ],
            "Paper": [
                ("Hammermill 20lb Copy Paper 10 Reams", 48.0, 26.0),
                ("HP Multipurpose Ultra White 5 Reams", 28.0, 14.0),
                ("Xerox Premium Recycled Paper 5 Reams", 34.0, 18.0),
            ],
            "Art": [
                ("Prismacolor Premier Colored Pencils 48ct", 42.0, 20.0),
                ("Sanford Sharpie Permanent Markers 24ct", 22.0, 9.0),
                ("Fiskars 8-Inch Stainless Scissors", 12.0, 5.0),
            ],
            "Appliances": [
                ("Keurig K-Elite Coffee Maker", 140.0, 95.0),
                ("Honeywell QuietSet Tower Fan", 65.0, 42.0),
                ("Holmes Compact Ceramic Heater", 35.0, 21.0),
            ]
        }
    }

    # Geography definition: Region -> States -> Cities + Postal Codes
    geography = {
        "East": [
            ("New York", "New York", "10001"),
            ("New York", "Buffalo", "14201"),
            ("Pennsylvania", "Philadelphia", "19102"),
            ("Massachusetts", "Boston", "02108"),
            ("New Jersey", "Newark", "07102"),
        ],
        "West": [
            ("California", "Los Angeles", "90001"),
            ("California", "San Francisco", "94102"),
            ("California", "San Diego", "92101"),
            ("Washington", "Seattle", "98101"),
            ("Colorado", "Denver", "80202"),
        ],
        "Central": [
            ("Illinois", "Chicago", "60601"),
            ("Texas", "Houston", "77001"),
            ("Texas", "Dallas", "75201"),
            ("Michigan", "Detroit", "48201"),
            ("Ohio", "Columbus", "43201"),
        ],
        "South": [
            ("Florida", "Miami", "33101"),
            ("Florida", "Tampa", "33601"),
            ("Georgia", "Atlanta", "30301"),
            ("North Carolina", "Charlotte", "28202"),
            ("Tennessee", "Nashville", "37201"),
        ]
    }

    segments = ["Consumer", "Corporate", "Home Office"]
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

    # Customer pool (~450 unique customers)
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                   "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
                   "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
                   "Matthew", "Margaret", "Anthony", "Betty", "Donald", "Sandra", "Mark", "Ashley"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                  "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"]

    customer_pool = []
    for i in range(1, 451):
        cid = f"CUST-{1000 + i}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        seg = random.choices(segments, weights=[0.52, 0.30, 0.18])[0]
        customer_pool.append((cid, f"{fn} {ln}", seg))

    # Generate 2,500 total transaction records across 2023-2024
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days

    records = []
    row_counter = 1
    order_counter = 1001

    # Flatten products for random sampling
    all_products = []
    for cat, subcats in catalog.items():
        for subcat, prods in subcats.items():
            for p_idx, (pname, price, cost) in enumerate(prods, 1):
                pid = f"PROD-{cat[:3].upper()}-{subcat[:3].upper()}-{100 + p_idx}"
                all_products.append((cat, subcat, pid, pname, price, cost))

    # Weight distribution across categories: Technology 35%, Furniture 30%, Office Supplies 35%
    cat_weights = {"Technology": 0.35, "Furniture": 0.30, "Office Supplies": 0.35}

    # Generate multi-item orders (approx 1,500 distinct orders generating ~2,500 rows)
    while len(records) < 2480:
        order_counter += 1
        oid = f"ORD-{order_counter}"
        
        # Order date with realistic seasonal weighting (Q4 surges: Oct, Nov, Dec get higher weight)
        day_offset = random.randint(0, days_range)
        cur_date = start_date + timedelta(days=day_offset)
        # 30% boost for Q4 months
        if cur_date.month in [10, 11, 12] and random.random() < 0.35:
            # Re-pick within Q4
            cur_date = datetime(cur_date.year, random.choice([10, 11, 12]), random.randint(1, 28))

        ship_mode = random.choices(ship_modes, weights=[0.60, 0.20, 0.15, 0.05])[0]
        ship_days = {"Standard Class": 4, "Second Class": 3, "First Class": 2, "Same Day": 0}[ship_mode]
        ship_date = cur_date + timedelta(days=ship_days)

        # Customer & Region
        cust_id, cust_name, segment = random.choice(customer_pool)
        region = random.choices(["West", "East", "Central", "South"], weights=[0.32, 0.30, 0.22, 0.16])[0]
        state, city, postal_code = random.choice(geography[region])

        # Number of items in this order: 1 to 4 items
        num_items = random.choices([1, 2, 3, 4], weights=[0.62, 0.24, 0.10, 0.04])[0]
        selected_prods = random.sample(all_products, min(num_items, len(all_products)))

        for cat, subcat, pid, pname, price, cost in selected_prods:
            qty = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[0.30, 0.25, 0.18, 0.12, 0.08, 0.04, 0.02, 0.01])[0]
            
            # Central region gets higher discounts on average (simulating competitive market)
            # Tables category often heavily discounted (business insight: negative profit driver)
            if subcat == "Tables":
                discount = random.choices([0.0, 0.15, 0.20, 0.30, 0.40, 0.50], weights=[0.10, 0.15, 0.25, 0.25, 0.15, 0.10])[0]
            elif region == "Central":
                discount = random.choices([0.0, 0.10, 0.20, 0.30, 0.40], weights=[0.25, 0.25, 0.25, 0.15, 0.10])[0]
            else:
                discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.55, 0.20, 0.12, 0.08, 0.05])[0]

            sales_val = round(qty * price * (1.0 - discount), 2)
            # Total cost is unit cost * quantity, plus handling/shipping factor
            total_cost = round(qty * cost, 2)
            profit_val = round(sales_val - total_cost, 2)

            records.append({
                "Row ID": row_counter,
                "Order ID": oid,
                "Order Date": cur_date.strftime("%Y-%m-%d"),
                "Ship Date": ship_date.strftime("%Y-%m-%d"),
                "Ship Mode": ship_mode,
                "Customer ID": cust_id,
                "Customer Name": cust_name,
                "Segment": segment,
                "Country": "United States",
                "City": city,
                "State": state,
                "Postal Code": str(postal_code),
                "Region": region,
                "Product ID": pid,
                "Category": cat,
                "Sub-Category": subcat,
                "Product Name": pname,
                "Sales": sales_val,
                "Quantity": qty,
                "Discount": discount,
                "Profit": profit_val
            })
            row_counter += 1

    df = pd.DataFrame(records)

    # -------------------------------------------------------------
    # Inject Controlled Real-World Data Quality Issues:
    # -------------------------------------------------------------
    # 1. Trailing / leading whitespace in Category and Sub-Category (12 rows)
    dirty_cats = [15, 42, 105, 220, 350, 480, 600, 750, 920, 1100, 1340, 1500]
    for idx in dirty_cats:
        if idx < len(df):
            val = df.loc[idx, "Category"]
            df.loc[idx, "Category"] = f"  {val}  " if idx % 2 == 0 else f"{val} "

    # 2. Inconsistent Date formats in Order Date (8 rows, e.g., DD/MM/YYYY or YYYY/MM/DD)
    dirty_dates = [25, 88, 160, 310, 520, 810, 1040, 1290]
    for idx in dirty_dates:
        if idx < len(df):
            dt_obj = datetime.strptime(df.loc[idx, "Order Date"], "%Y-%m-%d")
            df.loc[idx, "Order Date"] = dt_obj.strftime("%d/%m/%Y") if idx % 2 == 0 else dt_obj.strftime("%Y/%m/%d")

    # 3. Missing Postal Code (15 rows)
    missing_postal = [30, 75, 140, 260, 410, 590, 780, 990, 1200, 1450, 1680, 1890, 2050, 2220, 2390]
    for idx in missing_postal:
        if idx < len(df):
            df.loc[idx, "Postal Code"] = np.nan

    # 4. Duplicate transaction rows (5 exact duplicates appended at the end to simulate ETL double-ingestion)
    dup_rows = df.iloc[[10, 45, 120, 250, 500]].copy()
    df = pd.concat([df, dup_rows], ignore_index=True)

    # 5. Erroneous / Outlier records (2 invalid records to demonstrate business validation logic)
    # Row with negative quantity (-1)
    df.loc[len(df) - 2, "Quantity"] = -1
    # Row with impossible discount (1.5 = 150% discount)
    df.loc[len(df) - 1, "Discount"] = 1.50
    df.loc[len(df) - 1, "Sales"] = round(df.loc[len(df) - 1, "Quantity"] * 100 * (1 - 1.50), 2)  # negative sales

    # Save to data/raw/ecommerce_sales_raw.csv
    output_path = os.path.join("data", "raw", "ecommerce_sales_raw.csv")
    df.to_csv(output_path, index=False)
    print(f"Successfully generated raw dataset: {output_path}")
    print(f"Total raw rows: {len(df)}")
    print(f"Total raw columns: {len(df.columns)}")
    print("Columns:", list(df.columns))

if __name__ == "__main__":
    generate_dataset()

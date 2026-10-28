-- ============================================================================
-- Script: 02_data_import.sql
-- Description: Instructions and commands to import cleaned CSV into PostgreSQL.
-- Author: Senior Data Analyst & Technical Mentor
-- ============================================================================

-- METHOD 1: Using psql command line (\copy client command)
-- Run this directly inside psql connected to ecommerce_db:
-- Note: Replace with your absolute or relative path to cleaned_sales_data.csv.
\copy sales_orders FROM 'data/processed/cleaned_sales_data.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- METHOD 2: Using server-side COPY (Requires superuser / absolute path)
-- COPY sales_orders FROM 'C:/Users/mahes/OneDrive/Desktop/ecommerce-sales-analysis/data/processed/cleaned_sales_data.csv'
-- WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- METHOD 3: Using pgAdmin GUI Import Tool
-- 1. In pgAdmin Object Tree, expand Databases > ecommerce_db > Schemas > public > Tables.
-- 2. Right-click on 'sales_orders' and select 'Import/Export Data...'.
-- 3. Toggle switch to 'Import'.
-- 4. Filename: Browse to 'data/processed/cleaned_sales_data.csv'.
-- 5. Format: select 'csv'.
-- 6. In 'Options' tab: Header = Yes, Delimiter = ','.
-- 7. Click 'OK'.

-- METHOD 4: Automated Python Ingestion
-- Run: python python/run_sql_analysis.py
-- This script reads cleaned_sales_data.csv and loads it directly using SQLAlchemy!

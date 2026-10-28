-- ============================================================================
-- Script: 01_schema_setup.sql
-- Description: Creates the e-commerce sales database schema in PostgreSQL.
-- Author: Senior Data Analyst & Technical Mentor
-- ============================================================================

-- 1. Create Database (Run in psql / pgAdmin postgres database)
-- CREATE DATABASE ecommerce_db;
-- \c ecommerce_db;

-- 2. Drop existing table if recreating
DROP TABLE IF EXISTS sales_orders CASCADE;

-- 3. Create cleaned sales orders table
-- Chosen Schema Design: A clean, denormalized transactional fact table.
-- Why? For high-performance read-heavy analytical dashboards and reporting,
-- a denormalized schema avoids complex multi-table joins and simplifies analytical queries.
CREATE TABLE sales_orders (
    row_id              INT PRIMARY KEY,
    order_id            VARCHAR(30) NOT NULL,
    order_date          DATE NOT NULL,
    ship_date           DATE NOT NULL,
    ship_mode           VARCHAR(30) NOT NULL,
    customer_id         VARCHAR(30) NOT NULL,
    customer_name       VARCHAR(100) NOT NULL,
    segment             VARCHAR(50) NOT NULL,
    country             VARCHAR(50) NOT NULL,
    city                VARCHAR(50) NOT NULL,
    state               VARCHAR(50) NOT NULL,
    postal_code         VARCHAR(20),
    region              VARCHAR(30) NOT NULL,
    product_id          VARCHAR(50) NOT NULL,
    category            VARCHAR(50) NOT NULL,
    sub_category        VARCHAR(50) NOT NULL,
    product_name        VARCHAR(200) NOT NULL,
    sales               NUMERIC(10, 2) NOT NULL,
    quantity            INT NOT NULL CHECK (quantity > 0),
    discount            NUMERIC(4, 2) NOT NULL CHECK (discount >= 0.0 AND discount < 1.0),
    profit              NUMERIC(10, 2) NOT NULL,
    order_year          INT NOT NULL,
    order_month         VARCHAR(7) NOT NULL,     -- Format 'YYYY-MM'
    order_month_name    VARCHAR(20) NOT NULL,    -- E.g. 'January'
    order_quarter       VARCHAR(5) NOT NULL,     -- E.g. 'Q1'
    cost                NUMERIC(10, 2) NOT NULL,
    profit_margin_pct   NUMERIC(6, 2) NOT NULL,
    shipping_days       INT NOT NULL
);

-- 4. Create indexes to optimize analytical query performance
CREATE INDEX idx_orders_order_date ON sales_orders (order_date);
CREATE INDEX idx_orders_category ON sales_orders (category);
CREATE INDEX idx_orders_region ON sales_orders (region);
CREATE INDEX idx_orders_customer ON sales_orders (customer_id);
CREATE INDEX idx_orders_order_id ON sales_orders (order_id);

COMMENT ON TABLE sales_orders IS 'Cleaned retail e-commerce sales transactions (2023-2024)';
COMMENT ON COLUMN sales_orders.sales IS 'Net transaction revenue after discount in USD';
COMMENT ON COLUMN sales_orders.profit IS 'Net profit margin in USD (can be negative on discounted items)';

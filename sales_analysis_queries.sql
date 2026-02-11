-- =====================================================
-- SALES PERFORMANCE DASHBOARD - SQL QUERIES
-- Database: SQLite / MySQL / PostgreSQL Compatible
-- =====================================================

-- =====================================================
-- SECTION 1: DATABASE SETUP
-- =====================================================

-- Create the main table
CREATE TABLE IF NOT EXISTS superstore (
    row_id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode TEXT,
    customer_id TEXT NOT NULL,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    product_id TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales DECIMAL(10,2),
    quantity INTEGER,
    discount DECIMAL(3,2),
    profit DECIMAL(10,2)
);

-- Create indexes for better query performance
CREATE INDEX idx_order_date ON superstore(order_date);
CREATE INDEX idx_region ON superstore(region);
CREATE INDEX idx_category ON superstore(category);
CREATE INDEX idx_customer_id ON superstore(customer_id);
CREATE INDEX idx_product_id ON superstore(product_id);

-- =====================================================
-- SECTION 2: KEY PERFORMANCE INDICATORS (KPIs)
-- =====================================================

-- Query 1: Overall Business Summary
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT product_id) AS unique_products,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_order_value,
    SUM(quantity) AS total_quantity_sold
FROM superstore;

-- Query 2: KPIs by Year
SELECT 
    strftime('%Y', order_date) AS year,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY strftime('%Y', order_date)
ORDER BY year;

-- =====================================================
-- SECTION 3: REGIONAL ANALYSIS
-- =====================================================

-- Query 3: Sales Performance by Region
SELECT 
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_order_value,
    SUM(quantity) AS total_quantity
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;

-- Query 4: Top 10 States by Sales
SELECT 
    state,
    region,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY state, region
ORDER BY total_sales DESC
LIMIT 10;

-- Query 5: Top 10 Cities by Sales
SELECT 
    city,
    state,
    region,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY city, state, region
ORDER BY total_sales DESC
LIMIT 10;

-- =====================================================
-- SECTION 4: PRODUCT ANALYSIS
-- =====================================================

-- Query 6: Sales by Category
SELECT 
    category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    SUM(quantity) AS units_sold,
    ROUND(AVG(sales), 2) AS avg_sale_amount
FROM superstore
GROUP BY category
ORDER BY total_sales DESC;

-- Query 7: Sales by Sub-Category
SELECT 
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY category, sub_category
ORDER BY category, total_sales DESC;

-- Query 8: Top 20 Products by Sales
SELECT 
    product_name,
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS times_ordered,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold,
    ROUND(AVG(discount), 2) AS avg_discount
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 20;

-- Query 9: Top 20 Products by Profit
SELECT 
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 20;

-- Query 10: Products with Negative Profit (Loss-Making)
SELECT 
    product_name,
    category,
    sub_category,
    COUNT(*) AS loss_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_loss,
    ROUND(AVG(discount), 2) AS avg_discount
FROM superstore
WHERE profit < 0
GROUP BY product_name, category, sub_category
ORDER BY total_loss ASC
LIMIT 20;

-- =====================================================
-- SECTION 5: CUSTOMER ANALYSIS
-- =====================================================

-- Query 11: Customer Segment Analysis
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND((COUNT(DISTINCT order_id) * 1.0 / COUNT(DISTINCT customer_id)), 2) AS orders_per_customer
FROM superstore
GROUP BY segment
ORDER BY total_sales DESC;

-- Query 12: Top 30 Customers by Sales
SELECT 
    customer_name,
    customer_id,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value,
    SUM(quantity) AS items_purchased
FROM superstore
GROUP BY customer_name, customer_id, segment
ORDER BY total_sales DESC
LIMIT 30;

-- Query 13: Top 30 Customers by Profit
SELECT 
    customer_name,
    customer_id,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY customer_name, customer_id, segment
ORDER BY total_profit DESC
LIMIT 30;

-- Query 14: Customer Purchase Frequency Distribution
SELECT 
    order_frequency,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_sales), 2) AS avg_customer_value
FROM (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS order_frequency,
        SUM(sales) AS total_sales
    FROM superstore
    GROUP BY customer_id
)
GROUP BY order_frequency
ORDER BY order_frequency;

-- =====================================================
-- SECTION 6: TIME-BASED ANALYSIS
-- =====================================================

-- Query 15: Monthly Sales Trend
SELECT 
    strftime('%Y-%m', order_date) AS year_month,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY strftime('%Y-%m', order_date)
ORDER BY year_month;

-- Query 16: Quarterly Performance
SELECT 
    strftime('%Y', order_date) AS year,
    CASE 
        CAST(strftime('%m', order_date) AS INTEGER)
        WHEN 1 THEN 'Q1' WHEN 2 THEN 'Q1' WHEN 3 THEN 'Q1'
        WHEN 4 THEN 'Q2' WHEN 5 THEN 'Q2' WHEN 6 THEN 'Q2'
        WHEN 7 THEN 'Q3' WHEN 8 THEN 'Q3' WHEN 9 THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS quarterly_sales,
    ROUND(SUM(profit), 2) AS quarterly_profit
FROM superstore
GROUP BY year, quarter
ORDER BY year, quarter;

-- Query 17: Day of Week Analysis
SELECT 
    CASE CAST(strftime('%w', order_date) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        ELSE 'Saturday'
    END AS day_of_week,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY day_of_week
ORDER BY 
    CASE CAST(strftime('%w', order_date) AS INTEGER)
        WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 3
        WHEN 4 THEN 4 WHEN 5 THEN 5 WHEN 6 THEN 6 ELSE 7
    END;

-- Query 18: Year-over-Year Growth
SELECT 
    current_year.year,
    current_year.sales AS current_year_sales,
    previous_year.sales AS previous_year_sales,
    ROUND(((current_year.sales - previous_year.sales) / previous_year.sales) * 100, 2) AS yoy_growth_pct,
    current_year.profit AS current_year_profit,
    previous_year.profit AS previous_year_profit,
    ROUND(((current_year.profit - previous_year.profit) / previous_year.profit) * 100, 2) AS profit_growth_pct
FROM (
    SELECT 
        strftime('%Y', order_date) AS year,
        ROUND(SUM(sales), 2) AS sales,
        ROUND(SUM(profit), 2) AS profit
    FROM superstore
    GROUP BY strftime('%Y', order_date)
) current_year
LEFT JOIN (
    SELECT 
        strftime('%Y', order_date) AS year,
        ROUND(SUM(sales), 2) AS sales,
        ROUND(SUM(profit), 2) AS profit
    FROM superstore
    GROUP BY strftime('%Y', order_date)
) previous_year ON CAST(current_year.year AS INTEGER) = CAST(previous_year.year AS INTEGER) + 1
ORDER BY current_year.year;

-- =====================================================
-- SECTION 7: SHIPPING ANALYSIS
-- =====================================================

-- Query 19: Shipping Mode Performance
SELECT 
    ship_mode,
    COUNT(*) AS total_shipments,
    ROUND(AVG(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS avg_shipping_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM superstore)), 2) AS pct_of_orders
FROM superstore
GROUP BY ship_mode
ORDER BY total_sales DESC;

-- Query 20: Average Shipping Time by Region
SELECT 
    region,
    ship_mode,
    ROUND(AVG(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS avg_shipping_days,
    COUNT(*) AS shipments
FROM superstore
GROUP BY region, ship_mode
ORDER BY region, avg_shipping_days;

-- =====================================================
-- SECTION 8: DISCOUNT ANALYSIS
-- =====================================================

-- Query 21: Impact of Discount on Sales and Profit
SELECT 
    CASE 
        WHEN discount = 0 THEN '0% (No Discount)'
        WHEN discount <= 0.1 THEN '1-10%'
        WHEN discount <= 0.2 THEN '11-20%'
        WHEN discount <= 0.3 THEN '21-30%'
        WHEN discount <= 0.4 THEN '31-40%'
        ELSE '41%+'
    END AS discount_range,
    COUNT(*) AS orders,
    ROUND(AVG(sales), 2) AS avg_sales,
    ROUND(AVG(profit), 2) AS avg_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 1) AS avg_discount_pct
FROM superstore
GROUP BY discount_range
ORDER BY 
    CASE 
        WHEN discount = 0 THEN 0
        WHEN discount <= 0.1 THEN 1
        WHEN discount <= 0.2 THEN 2
        WHEN discount <= 0.3 THEN 3
        WHEN discount <= 0.4 THEN 4
        ELSE 5
    END;

-- Query 22: Discount Analysis by Category
SELECT 
    category,
    COUNT(*) AS orders_with_discount,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM superstore
WHERE discount > 0
GROUP BY category
ORDER BY avg_discount_pct DESC;

-- =====================================================
-- SECTION 9: CROSS-DIMENSIONAL ANALYSIS
-- =====================================================

-- Query 23: Region vs Category Performance Matrix
SELECT 
    region,
    category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY region, category
ORDER BY region, sales DESC;

-- Query 24: Segment vs Region Performance
SELECT 
    segment,
    region,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY segment, region
ORDER BY segment, sales DESC;

-- Query 25: Category Performance Over Time
SELECT 
    strftime('%Y', order_date) AS year,
    category,
    ROUND(SUM(sales), 2) AS yearly_sales,
    ROUND(SUM(profit), 2) AS yearly_profit,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY strftime('%Y', order_date), category
ORDER BY year, yearly_sales DESC;

-- =====================================================
-- SECTION 10: ADVANCED ANALYTICS
-- =====================================================

-- Query 26: Customer Lifetime Value (Top 50)
SELECT 
    customer_name,
    customer_id,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    ROUND(JULIANDAY(MAX(order_date)) - JULIANDAY(MIN(order_date)), 0) AS customer_lifetime_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY customer_name, customer_id, segment
HAVING total_orders > 1
ORDER BY total_sales DESC
LIMIT 50;

-- Query 27: Product Performance Ranking
SELECT 
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS times_ordered,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank,
    RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 100;

-- Query 28: Seasonal Analysis
SELECT 
    CASE CAST(strftime('%m', order_date) AS INTEGER)
        WHEN 12 THEN 'Winter' WHEN 1 THEN 'Winter' WHEN 2 THEN 'Winter'
        WHEN 3 THEN 'Spring' WHEN 4 THEN 'Spring' WHEN 5 THEN 'Spring'
        WHEN 6 THEN 'Summer' WHEN 7 THEN 'Summer' WHEN 8 THEN 'Summer'
        ELSE 'Fall'
    END AS season,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY season
ORDER BY 
    CASE season
        WHEN 'Spring' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Fall' THEN 3
        ELSE 4
    END;

-- Query 29: Cohort Analysis - Customer Acquisition by Year
SELECT 
    acquisition_year,
    COUNT(DISTINCT customer_id) AS new_customers,
    ROUND(AVG(first_order_value), 2) AS avg_first_order,
    ROUND(SUM(total_sales), 2) AS cohort_total_sales,
    ROUND(SUM(total_profit), 2) AS cohort_total_profit
FROM (
    SELECT 
        customer_id,
        strftime('%Y', MIN(order_date)) AS acquisition_year,
        SUM(CASE WHEN order_date = MIN(order_date) THEN sales ELSE 0 END) AS first_order_value,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit
    FROM superstore
    GROUP BY customer_id
)
GROUP BY acquisition_year
ORDER BY acquisition_year;

-- Query 30: RFM Analysis - Recency, Frequency, Monetary
SELECT 
    customer_name,
    customer_id,
    segment,
    JULIANDAY('2017-12-31') - JULIANDAY(MAX(order_date)) AS recency_days,
    COUNT(DISTINCT order_id) AS frequency,
    ROUND(SUM(sales), 2) AS monetary_value,
    ROUND(SUM(profit), 2) AS total_profit,
    CASE 
        WHEN JULIANDAY('2017-12-31') - JULIANDAY(MAX(order_date)) <= 90 THEN 'Active'
        WHEN JULIANDAY('2017-12-31') - JULIANDAY(MAX(order_date)) <= 180 THEN 'At Risk'
        ELSE 'Lost'
    END AS customer_status
FROM superstore
GROUP BY customer_name, customer_id, segment
ORDER BY monetary_value DESC
LIMIT 100;

-- =====================================================
-- END OF SQL QUERIES
-- =====================================================

-- Export results (example for SQLite)
-- .mode csv
-- .output region_analysis.csv
-- [Run your query here]
-- .output stdout

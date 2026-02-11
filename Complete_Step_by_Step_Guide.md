# Sales Performance Dashboard - Complete Step-by-Step Guide

## Project Overview
This project creates a comprehensive Sales Performance Dashboard using the Superstore dataset. We'll use multiple tools (Excel, SQL, Python/Pandas, and Power BI) to analyze and visualize sales data.

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Data Understanding](#data-understanding)
3. [Excel Analysis](#excel-analysis)
4. [SQL Analysis](#sql-analysis)
5. [Python/Pandas Analysis](#pythonpandas-analysis)
6. [Power BI Dashboard](#power-bi-dashboard)
7. [Key Insights](#key-insights)

---

## 1. Project Setup

### Prerequisites
- **Excel**: Microsoft Excel 2016 or later (or Google Sheets)
- **SQL**: SQLite, MySQL, or PostgreSQL
- **Python**: Python 3.8+ with libraries (pandas, numpy, matplotlib, seaborn, plotly)
- **Power BI**: Power BI Desktop (free download from Microsoft)

### Dataset Information
**File**: Sample_Superstore.csv
**Rows**: 9,994 records
**Columns**: 21 fields

**Column Descriptions**:
- `Row ID`: Unique identifier for each row
- `Order ID`: Unique order identifier
- `Order Date`: Date when order was placed
- `Ship Date`: Date when order was shipped
- `Ship Mode`: Shipping method (Second Class, Standard Class, First Class, Same Day)
- `Customer ID`: Unique customer identifier
- `Customer Name`: Name of the customer
- `Segment`: Customer segment (Consumer, Corporate, Home Office)
- `Country`: Country (United States)
- `City`: City name
- `State`: State name
- `Postal Code`: Postal code
- `Region`: Geographic region (South, Central, East, West)
- `Product ID`: Unique product identifier
- `Category`: Product category (Furniture, Office Supplies, Technology)
- `Sub-Category`: Product sub-category
- `Product Name`: Full product name
- `Sales`: Sales amount in dollars
- `Quantity`: Number of items sold
- `Discount`: Discount percentage (0-0.8)
- `Profit`: Profit amount in dollars

---

## 2. Data Understanding

### Initial Data Exploration
Before building the dashboard, understand your data:

**Key Questions to Answer**:
1. What is the date range of the data? (2014-2017)
2. How many unique customers? (~800)
3. How many unique products? (~1,800+)
4. What are the sales trends over time?
5. Which regions/categories perform best?
6. What is the overall profitability?

### Data Quality Check
- **Missing Values**: Check for NULL values
- **Duplicates**: Verify Row ID uniqueness
- **Data Types**: Ensure dates are in date format, numbers are numeric
- **Outliers**: Identify unusual sales or profit values

---

## 3. Excel Analysis

### Step 3.1: Import and Clean Data

1. **Open Excel** and import the CSV file:
   - Go to `Data` → `Get Data` → `From File` → `From Text/CSV`
   - Select `Sample_Superstore.csv`
   - Click `Transform Data` to open Power Query Editor

2. **Data Cleaning in Power Query**:
   - Change `Order Date` and `Ship Date` to Date type
   - Change `Sales`, `Quantity`, `Discount`, and `Profit` to Currency/Number
   - Remove any rows with errors
   - Click `Close & Load`

### Step 3.2: Create Calculated Columns

Add new columns for analysis:

1. **Profit Margin**:
   ```
   =Profit/Sales
   ```

2. **Order Year**:
   ```
   =YEAR(Order Date)
   ```

3. **Order Month**:
   ```
   =TEXT(Order Date, "MMM-YYYY")
   ```

4. **Shipping Days**:
   ```
   =Ship Date - Order Date
   ```

### Step 3.3: Create Pivot Tables

**Pivot Table 1: Sales by Region**
- Rows: Region
- Values: Sum of Sales, Sum of Profit
- Add Profit Margin calculated field

**Pivot Table 2: Sales by Category**
- Rows: Category, Sub-Category
- Values: Sum of Sales, Count of Order ID

**Pivot Table 3: Monthly Sales Trend**
- Rows: Order Month
- Values: Sum of Sales, Sum of Profit

**Pivot Table 4: Top 10 Customers**
- Rows: Customer Name
- Values: Sum of Sales
- Sort: Descending by Sales

### Step 3.4: Create Charts

1. **Line Chart**: Monthly sales trend
2. **Bar Chart**: Sales by region
3. **Pie Chart**: Sales distribution by category
4. **Column Chart**: Top 10 products by profit

### Step 3.5: Build Dashboard in Excel

1. Create a new worksheet named "Dashboard"
2. Copy all charts to the dashboard
3. Add slicers for:
   - Year
   - Region
   - Category
   - Segment
4. Format with consistent colors and styling
5. Add KPI cards showing:
   - Total Sales
   - Total Profit
   - Profit Margin %
   - Total Orders

---

## 4. SQL Analysis

### Step 4.1: Import Data to SQL Database

**Using SQLite** (easiest option):

```sql
-- Create database and import CSV
-- Use SQLite Studio or command line

CREATE TABLE superstore (
    row_id INTEGER,
    order_id TEXT,
    order_date DATE,
    ship_date DATE,
    ship_mode TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL
);

-- Import CSV file using SQLite import command
```

### Step 4.2: Key SQL Queries for Analysis

**Query 1: Total Sales and Profit by Region**
```sql
SELECT 
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;
```

**Query 2: Top 10 Products by Profit**
```sql
SELECT 
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS total_quantity
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 10;
```

**Query 3: Monthly Sales Trend**
```sql
SELECT 
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit,
    COUNT(DISTINCT order_id) AS orders
FROM superstore
GROUP BY month
ORDER BY month;
```

**Query 4: Customer Segment Analysis**
```sql
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY segment
ORDER BY total_sales DESC;
```

**Query 5: Category Performance by Region**
```sql
SELECT 
    region,
    category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY region, category
ORDER BY region, sales DESC;
```

**Query 6: Shipping Analysis**
```sql
SELECT 
    ship_mode,
    COUNT(*) AS shipments,
    ROUND(AVG(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS avg_shipping_days,
    ROUND(SUM(sales), 2) AS total_sales
FROM superstore
GROUP BY ship_mode
ORDER BY total_sales DESC;
```

**Query 7: Year-over-Year Growth**
```sql
SELECT 
    strftime('%Y', order_date) AS year,
    ROUND(SUM(sales), 2) AS yearly_sales,
    ROUND(SUM(profit), 2) AS yearly_profit
FROM superstore
GROUP BY year
ORDER BY year;
```

**Query 8: Discount Impact Analysis**
```sql
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.2 THEN '1-20%'
        WHEN discount <= 0.4 THEN '21-40%'
        ELSE '41%+'
    END AS discount_range,
    COUNT(*) AS orders,
    ROUND(AVG(sales), 2) AS avg_sales,
    ROUND(AVG(profit), 2) AS avg_profit
FROM superstore
GROUP BY discount_range
ORDER BY discount_range;
```

---

## 5. Python/Pandas Analysis

### Step 5.1: Setup Python Environment

```bash
# Install required libraries
pip install pandas numpy matplotlib seaborn plotly openpyxl
```

### Step 5.2: Load and Explore Data

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load data
df = pd.read_csv('Sample_Superstore.csv', encoding='latin-1')

# Display basic info
print(df.info())
print(df.head())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Check data types
print(df.dtypes)
```

### Step 5.3: Data Cleaning and Preprocessing

```python
# Convert date columns
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')

# Create new calculated columns
df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Quarter'] = df['Order Date'].dt.quarter
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Year-Month'] = df['Order Date'].dt.to_period('M')

# Remove any duplicates
df = df.drop_duplicates()

print(f"Total Records: {len(df)}")
print(f"Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")
```

### Step 5.4: Comprehensive Analysis

```python
# 1. Overall KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()
avg_profit_margin = (total_profit / total_sales) * 100

print(f"""
=== KEY PERFORMANCE INDICATORS ===
Total Sales: ${total_sales:,.2f}
Total Profit: ${total_profit:,.2f}
Profit Margin: {avg_profit_margin:.2f}%
Total Orders: {total_orders:,}
Total Customers: {total_customers:,}
Unique Products: {df['Product ID'].nunique():,}
""")

# 2. Sales by Region
region_analysis = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Customer ID': 'nunique'
}).round(2)
region_analysis['Profit Margin %'] = (region_analysis['Profit'] / region_analysis['Sales'] * 100).round(2)
print("\n=== SALES BY REGION ===")
print(region_analysis)

# 3. Sales by Category
category_analysis = df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'nunique'
}).round(2)
print("\n=== SALES BY CATEGORY ===")
print(category_analysis)

# 4. Monthly Sales Trend
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M')).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
print("\n=== MONTHLY SALES TREND (Sample) ===")
print(monthly_sales.tail(12))

# 5. Top 10 Customers
top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
print("\n=== TOP 10 CUSTOMERS ===")
print(top_customers)

# 6. Top 10 Products by Profit
top_products = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
print("\n=== TOP 10 PRODUCTS BY PROFIT ===")
print(top_products)

# 7. Segment Analysis
segment_analysis = df.groupby('Segment').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Customer ID': 'nunique',
    'Order ID': 'nunique'
}).round(2)
segment_analysis['Avg Order Value'] = (segment_analysis['Sales'] / segment_analysis['Order ID']).round(2)
print("\n=== CUSTOMER SEGMENT ANALYSIS ===")
print(segment_analysis)
```

### Step 5.5: Create Visualizations

```python
# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 1. Sales by Region (Bar Chart)
plt.figure(figsize=(10, 6))
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
plt.bar(region_sales.index, region_sales.values, color='steelblue')
plt.title('Total Sales by Region', fontsize=16, fontweight='bold')
plt.xlabel('Region', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.xticks(rotation=0)
for i, v in enumerate(region_sales.values):
    plt.text(i, v + 10000, f'${v:,.0f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('sales_by_region.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Sales by Category (Pie Chart)
plt.figure(figsize=(10, 8))
category_sales = df.groupby('Category')['Sales'].sum()
colors = ['#ff9999', '#66b3ff', '#99ff99']
plt.pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%', 
        startangle=90, colors=colors, textprops={'fontsize': 12})
plt.title('Sales Distribution by Category', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('sales_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Monthly Sales Trend (Line Chart)
plt.figure(figsize=(14, 6))
monthly_data = df.groupby(df['Order Date'].dt.to_period('M')).agg({
    'Sales': 'sum',
    'Profit': 'sum'
})
monthly_data.index = monthly_data.index.to_timestamp()

plt.plot(monthly_data.index, monthly_data['Sales'], marker='o', linewidth=2, 
         label='Sales', color='blue')
plt.plot(monthly_data.index, monthly_data['Profit'], marker='s', linewidth=2, 
         label='Profit', color='green')
plt.title('Monthly Sales and Profit Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Amount ($)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Top 10 Sub-Categories (Horizontal Bar Chart)
plt.figure(figsize=(10, 8))
top_subcats = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=True).tail(10)
plt.barh(range(len(top_subcats)), top_subcats.values, color='coral')
plt.yticks(range(len(top_subcats)), top_subcats.index)
plt.title('Top 10 Sub-Categories by Sales', fontsize=16, fontweight='bold')
plt.xlabel('Sales ($)', fontsize=12)
plt.ylabel('Sub-Category', fontsize=12)
for i, v in enumerate(top_subcats.values):
    plt.text(v + 5000, i, f'${v:,.0f}', va='center')
plt.tight_layout()
plt.savefig('top_subcategories.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Profit Margin Distribution (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(df['Profit Margin'], bins=50, color='skyblue', edgecolor='black')
plt.title('Profit Margin Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Profit Margin (%)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df['Profit Margin'].mean(), color='red', linestyle='--', 
            linewidth=2, label=f'Mean: {df["Profit Margin"].mean():.1f}%')
plt.legend()
plt.tight_layout()
plt.savefig('profit_margin_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Sales Heatmap by Region and Category
plt.figure(figsize=(10, 6))
heatmap_data = df.pivot_table(values='Sales', index='Region', 
                                columns='Category', aggfunc='sum')
sns.heatmap(heatmap_data, annot=True, fmt=',.0f', cmap='YlOrRd', 
            linewidths=0.5, cbar_kws={'label': 'Sales ($)'})
plt.title('Sales Heatmap: Region vs Category', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('sales_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nAll visualizations saved successfully!")
```

### Step 5.6: Export Analysis Results

```python
# Create summary Excel file with multiple sheets
with pd.ExcelWriter('Sales_Analysis_Results.xlsx', engine='openpyxl') as writer:
    # Sheet 1: Overall Summary
    summary_df = pd.DataFrame({
        'Metric': ['Total Sales', 'Total Profit', 'Profit Margin %', 
                   'Total Orders', 'Total Customers', 'Unique Products'],
        'Value': [f'${total_sales:,.2f}', f'${total_profit:,.2f}', 
                  f'{avg_profit_margin:.2f}%', total_orders, 
                  total_customers, df['Product ID'].nunique()]
    })
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Sheet 2: Region Analysis
    region_analysis.to_excel(writer, sheet_name='Region Analysis')
    
    # Sheet 3: Category Analysis
    category_analysis.to_excel(writer, sheet_name='Category Analysis')
    
    # Sheet 4: Monthly Trend
    monthly_sales.to_excel(writer, sheet_name='Monthly Trend')
    
    # Sheet 5: Top Customers
    top_customers.to_excel(writer, sheet_name='Top Customers')
    
    # Sheet 6: Segment Analysis
    segment_analysis.to_excel(writer, sheet_name='Segment Analysis')

print("Analysis exported to 'Sales_Analysis_Results.xlsx'")
```

---

## 6. Power BI Dashboard

### Step 6.1: Import Data into Power BI

1. **Open Power BI Desktop**
2. Click **Get Data** → **Text/CSV**
3. Select `Sample_Superstore.csv`
4. Click **Transform Data** to open Power Query Editor

### Step 6.2: Data Transformation in Power Query

1. **Change Data Types**:
   - Order Date, Ship Date → Date
   - Sales, Profit, Discount → Decimal Number
   - Quantity → Whole Number

2. **Add Custom Columns**:
   - **Profit Margin**: `[Profit] / [Sales]`
   - **Order Year**: `Date.Year([Order Date])`
   - **Order Month Name**: `Date.MonthName([Order Date])`
   - **Shipping Days**: `Duration.Days([Ship Date] - [Order Date])`

3. **Click Close & Apply**

### Step 6.3: Create DAX Measures

In Power BI, create these calculated measures:

```dax
Total Sales = SUM(Superstore[Sales])

Total Profit = SUM(Superstore[Profit])

Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0) * 100

Total Orders = DISTINCTCOUNT(Superstore[Order ID])

Total Customers = DISTINCTCOUNT(Superstore[Customer ID])

Avg Order Value = DIVIDE([Total Sales], [Total Orders], 0)

YTD Sales = TOTALYTD([Total Sales], Superstore[Order Date])

Previous Year Sales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Superstore[Order Date]))

YoY Growth % = DIVIDE([Total Sales] - [Previous Year Sales], [Previous Year Sales], 0) * 100
```

### Step 6.4: Build Dashboard Visuals

**Page 1: Executive Summary**

1. **KPI Cards** (Top row):
   - Total Sales
   - Total Profit
   - Profit Margin %
   - Total Orders

2. **Line Chart**: Monthly Sales Trend
   - X-axis: Order Date (Month)
   - Y-axis: Total Sales
   - Legend: Category (optional)

3. **Donut Chart**: Sales by Category
   - Values: Total Sales
   - Legend: Category

4. **Map Visual**: Sales by State
   - Location: State
   - Size: Total Sales
   - Color: Total Profit

5. **Bar Chart**: Sales by Region
   - Axis: Region
   - Values: Total Sales

6. **Table**: Top 10 Products
   - Columns: Product Name, Sales, Profit, Quantity
   - Sorted by Profit (descending)

**Page 2: Customer Analysis**

1. **KPI Cards**:
   - Total Customers
   - Avg Customer Value
   - Repeat Customer Rate

2. **Bar Chart**: Sales by Segment
   - Axis: Segment
   - Values: Total Sales, Total Profit

3. **Table**: Top 20 Customers
   - Customer Name, Total Sales, Total Orders, Avg Order Value

4. **Scatter Chart**: Customer Value vs Order Frequency
   - X-axis: Number of Orders
   - Y-axis: Total Sales
   - Details: Customer Name

**Page 3: Product Performance**

1. **Matrix Visual**: Sales by Category and Sub-Category
2. **Treemap**: Sales Distribution by Sub-Category
3. **Column Chart**: Top Products by Profit
4. **Line Chart**: Product Performance Over Time

**Page 4: Regional Analysis**

1. **Filled Map**: Sales by State
2. **Clustered Bar Chart**: Top States by Sales
3. **Matrix**: Region vs Category Sales
4. **Cards**: Region-specific KPIs

### Step 6.5: Add Interactivity

1. **Slicers**:
   - Date Range (Order Date)
   - Region
   - Category
   - Segment
   - Ship Mode

2. **Drill-Through Pages**:
   - Product Details
   - Customer Details
   - Regional Deep Dive

3. **Bookmarks**:
   - Sales View
   - Profit View
   - Quantity View

4. **Buttons**:
   - Navigation between pages
   - Reset filters
   - Export data

### Step 6.6: Formatting and Design

1. **Choose a consistent color theme**
2. **Add company branding/logo**
3. **Use consistent fonts** (Segoe UI recommended)
4. **Add titles and descriptions** to each visual
5. **Enable tooltips** for additional context
6. **Set page background** for professional look
7. **Align and distribute** visuals evenly

### Step 6.7: Publish Dashboard

1. **Save the .pbix file**
2. **Sign in to Power BI Service**
3. Click **Publish** → Select workspace
4. **Share dashboard** with stakeholders
5. **Set up scheduled refresh** if connected to live data

---

## 7. Key Insights

Based on the analysis of the Superstore dataset:

### Overall Performance
- **Total Sales**: ~$2.3 Million
- **Total Profit**: ~$286K
- **Profit Margin**: ~12.5%
- **Total Orders**: ~5,000
- **Total Customers**: ~800

### Regional Insights
- **West region** generates highest sales
- **Central region** has lowest profit margin
- Opportunity to improve operations in underperforming regions

### Product Insights
- **Technology** category has highest profit margin
- **Office Supplies** has highest order volume
- **Furniture** has mixed profitability (some items lose money)
- Need to review discount strategy for low-margin products

### Customer Insights
- **Consumer segment** represents largest customer base
- **Corporate segment** has higher average order value
- Potential to grow Home Office segment

### Temporal Trends
- Sales show seasonal patterns (Q4 typically strong)
- Year-over-year growth trend
- Consistent monthly sales with some volatility

### Operational Insights
- Standard Class shipping most common
- Average shipping time varies by mode
- Discount levels significantly impact profitability

---

## Best Practices

### Data Analysis
1. Always validate data before analysis
2. Document assumptions and calculations
3. Cross-check results across multiple tools
4. Keep data sources updated

### Dashboard Design
1. Put most important KPIs at top
2. Use appropriate chart types for data
3. Maintain consistent color scheme
4. Enable filtering and drill-down
5. Test dashboard with end users

### Performance Optimization
1. Minimize calculated columns in Power BI
2. Use measures instead of calculated columns
3. Optimize SQL queries with indexes
4. Use efficient pandas operations

### Maintenance
1. Schedule regular data refreshes
2. Monitor dashboard performance
3. Gather user feedback
4. Update based on changing requirements

---

## Conclusion

This comprehensive Sales Performance Dashboard provides actionable insights into:
- Sales trends and patterns
- Product and category performance
- Regional distribution
- Customer behavior
- Profitability analysis

Use these insights to make data-driven decisions for business growth!

---

## Additional Resources

- **Power BI Documentation**: https://docs.microsoft.com/power-bi/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **SQL Tutorial**: https://www.w3schools.com/sql/
- **Excel Power Query Guide**: https://support.microsoft.com/excel

---

**Project Created By**: Data Analytics Team
**Last Updated**: February 2026
**Version**: 1.0

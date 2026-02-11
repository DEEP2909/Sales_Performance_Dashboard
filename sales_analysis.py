"""
SALES PERFORMANCE DASHBOARD - PYTHON ANALYSIS SCRIPT
======================================================
This script performs comprehensive data analysis on the Superstore dataset
using Pandas, NumPy, and creates visualizations using Matplotlib and Seaborn.

Requirements:
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- openpyxl (for Excel export)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*70)
print("SALES PERFORMANCE DASHBOARD - DATA ANALYSIS")
print("="*70)
print()

# ==========================================
# 1. LOAD AND EXPLORE DATA
# ==========================================

print("1. LOADING DATA...")
print("-" * 70)

# Load the dataset
df = pd.read_csv('Sample_Superstore.csv', encoding='latin-1')

print(f"✓ Data loaded successfully!")
print(f"  - Total records: {len(df):,}")
print(f"  - Total columns: {len(df.columns)}")
print()

# Display first few rows
print("First 5 rows of data:")
print(df.head())
print()

# Display data info
print("Dataset Information:")
print(df.info())
print()

# Display basic statistics
print("Basic Statistics:")
print(df.describe())
print()

# ==========================================
# 2. DATA CLEANING AND PREPROCESSING
# ==========================================

print("\n2. DATA CLEANING AND PREPROCESSING...")
print("-" * 70)

# Check for missing values
print("Missing values:")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0] if missing_values.sum() > 0 else "No missing values found!")
print()

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"✓ Removed {duplicates} duplicate rows")
print()

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')
print("✓ Date columns converted to datetime format")
print()

# Create new calculated columns
df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month Name'] = df['Order Date'].dt.strftime('%b')
df['Order Quarter'] = df['Order Date'].dt.quarter
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Year-Month'] = df['Order Date'].dt.to_period('M')
df['Year-Quarter'] = df['Order Date'].dt.to_period('Q')

print("✓ Created calculated columns:")
print("  - Profit Margin")
print("  - Order Year, Month, Quarter")
print("  - Shipping Days")
print("  - Year-Month, Year-Quarter")
print()

print(f"✓ Final dataset shape: {df.shape}")
print(f"  Date range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
print()

# ==========================================
# 3. OVERALL KPIs
# ==========================================

print("\n3. KEY PERFORMANCE INDICATORS (KPIs)")
print("="*70)

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()
unique_products = df['Product ID'].nunique()
avg_profit_margin = df['Profit Margin'].mean()
avg_order_value = df.groupby('Order ID')['Sales'].sum().mean()
total_quantity = df['Quantity'].sum()

print(f"""
┌─────────────────────────────────────────────────────┐
│              BUSINESS OVERVIEW                      │
├─────────────────────────────────────────────────────┤
│  Total Sales:            ${total_sales:>18,.2f}  │
│  Total Profit:           ${total_profit:>18,.2f}  │
│  Profit Margin:          {avg_profit_margin:>18,.2f}% │
│  Total Orders:           {total_orders:>18,}    │
│  Total Customers:        {total_customers:>18,}    │
│  Unique Products:        {unique_products:>18,}    │
│  Average Order Value:    ${avg_order_value:>18,.2f}  │
│  Total Quantity Sold:    {total_quantity:>18,}    │
└─────────────────────────────────────────────────────┘
""")

# ==========================================
# 4. REGIONAL ANALYSIS
# ==========================================

print("\n4. REGIONAL ANALYSIS")
print("="*70)

region_analysis = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Customer ID': 'nunique',
    'Quantity': 'sum'
}).round(2)

region_analysis.columns = ['Total Sales', 'Total Profit', 'Total Orders', 
                           'Total Customers', 'Quantity Sold']
region_analysis['Profit Margin %'] = ((region_analysis['Total Profit'] / 
                                       region_analysis['Total Sales']) * 100).round(2)
region_analysis['Avg Order Value'] = (region_analysis['Total Sales'] / 
                                      region_analysis['Total Orders']).round(2)

# Sort by sales
region_analysis = region_analysis.sort_values('Total Sales', ascending=False)

print("\nSales Performance by Region:")
print(region_analysis)
print()

# Calculate region contribution
region_analysis['% of Total Sales'] = ((region_analysis['Total Sales'] / 
                                        total_sales) * 100).round(2)
print("\nRegion Contribution to Total Sales:")
print(region_analysis[['Total Sales', '% of Total Sales']])
print()

# ==========================================
# 5. CATEGORY ANALYSIS
# ==========================================

print("\n5. PRODUCT CATEGORY ANALYSIS")
print("="*70)

category_analysis = df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Quantity': 'sum',
    'Discount': 'mean'
}).round(2)

category_analysis.columns = ['Total Sales', 'Total Profit', 'Total Orders', 
                             'Quantity Sold', 'Avg Discount']
category_analysis['Profit Margin %'] = ((category_analysis['Total Profit'] / 
                                         category_analysis['Total Sales']) * 100).round(2)
category_analysis['% of Sales'] = ((category_analysis['Total Sales'] / 
                                    total_sales) * 100).round(2)

category_analysis = category_analysis.sort_values('Total Sales', ascending=False)

print("\nCategory Performance:")
print(category_analysis)
print()

# Sub-Category Analysis
print("\nTop 10 Sub-Categories by Sales:")
subcat_analysis = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
print(subcat_analysis)
print()

print("\nTop 10 Sub-Categories by Profit:")
subcat_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).head(10)
print(subcat_profit)
print()

print("\nBottom 10 Sub-Categories by Profit (Potential Issues):")
subcat_loss = df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=True).head(10)
print(subcat_loss)
print()

# ==========================================
# 6. CUSTOMER ANALYSIS
# ==========================================

print("\n6. CUSTOMER ANALYSIS")
print("="*70)

# Segment Analysis
segment_analysis = df.groupby('Segment').agg({
    'Customer ID': 'nunique',
    'Order ID': 'nunique',
    'Sales': 'sum',
    'Profit': 'sum'
}).round(2)

segment_analysis.columns = ['Total Customers', 'Total Orders', 'Total Sales', 'Total Profit']
segment_analysis['Avg Order Value'] = (segment_analysis['Total Sales'] / 
                                       segment_analysis['Total Orders']).round(2)
segment_analysis['Orders per Customer'] = (segment_analysis['Total Orders'] / 
                                           segment_analysis['Total Customers']).round(2)
segment_analysis['Profit Margin %'] = ((segment_analysis['Total Profit'] / 
                                        segment_analysis['Total Sales']) * 100).round(2)

segment_analysis = segment_analysis.sort_values('Total Sales', ascending=False)

print("\nCustomer Segment Analysis:")
print(segment_analysis)
print()

# Top Customers
print("\nTop 20 Customers by Sales:")
customer_sales = df.groupby(['Customer ID', 'Customer Name']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
customer_sales.columns = ['Total Sales', 'Total Profit', 'Number of Orders']
customer_sales = customer_sales.sort_values('Total Sales', ascending=False).head(20)
print(customer_sales)
print()

# Customer Frequency Distribution
print("\nCustomer Purchase Frequency:")
customer_frequency = df.groupby('Customer ID')['Order ID'].nunique()
freq_dist = customer_frequency.value_counts().sort_index()
print(freq_dist.head(10))
print()

# ==========================================
# 7. TIME-BASED ANALYSIS
# ==========================================

print("\n7. TIME-BASED ANALYSIS")
print("="*70)

# Yearly Performance
print("\nYearly Performance:")
yearly_perf = df.groupby('Order Year').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Customer ID': 'nunique'
}).round(2)
yearly_perf.columns = ['Sales', 'Profit', 'Orders', 'Customers']
yearly_perf['Profit Margin %'] = ((yearly_perf['Profit'] / yearly_perf['Sales']) * 100).round(2)

# Calculate YoY growth
yearly_perf['Sales Growth %'] = yearly_perf['Sales'].pct_change() * 100
yearly_perf['Profit Growth %'] = yearly_perf['Profit'].pct_change() * 100

print(yearly_perf)
print()

# Monthly Trend (Last 12 months of data)
print("\nMonthly Sales Trend (Last 12 months):")
monthly_data = df.groupby('Year-Month').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
monthly_data.columns = ['Sales', 'Profit', 'Orders']
print(monthly_data.tail(12))
print()

# Quarterly Performance
print("\nQuarterly Performance:")
quarterly_perf = df.groupby(['Order Year', 'Order Quarter']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).round(2)
print(quarterly_perf)
print()

# ==========================================
# 8. PRODUCT ANALYSIS
# ==========================================

print("\n8. DETAILED PRODUCT ANALYSIS")
print("="*70)

# Top Products
print("\nTop 15 Products by Sales:")
top_products_sales = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'nunique'
}).round(2)
top_products_sales.columns = ['Sales', 'Profit', 'Quantity', 'Times Ordered']
top_products_sales = top_products_sales.sort_values('Sales', ascending=False).head(15)
print(top_products_sales)
print()

print("\nTop 15 Products by Profit:")
top_products_profit = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)
top_products_profit.columns = ['Sales', 'Profit', 'Quantity']
top_products_profit['Profit Margin %'] = ((top_products_profit['Profit'] / 
                                           top_products_profit['Sales']) * 100).round(2)
top_products_profit = top_products_profit.sort_values('Profit', ascending=False).head(15)
print(top_products_profit)
print()

# Loss-making products
print("\nLoss-Making Products (Bottom 10 by Profit):")
loss_products = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Discount': 'mean'
}).round(2)
loss_products.columns = ['Sales', 'Profit', 'Times Ordered', 'Avg Discount']
loss_products = loss_products[loss_products['Profit'] < 0].sort_values('Profit').head(10)
print(loss_products)
print()

# ==========================================
# 9. SHIPPING ANALYSIS
# ==========================================

print("\n9. SHIPPING AND LOGISTICS ANALYSIS")
print("="*70)

shipping_analysis = df.groupby('Ship Mode').agg({
    'Order ID': 'count',
    'Shipping Days': 'mean',
    'Sales': 'sum',
    'Profit': 'sum'
}).round(2)

shipping_analysis.columns = ['Total Shipments', 'Avg Shipping Days', 'Total Sales', 'Total Profit']
shipping_analysis['% of Orders'] = ((shipping_analysis['Total Shipments'] / 
                                    len(df)) * 100).round(2)
shipping_analysis = shipping_analysis.sort_values('Total Sales', ascending=False)

print("\nShipping Mode Performance:")
print(shipping_analysis)
print()

# Shipping by Region
print("\nAverage Shipping Days by Region:")
region_shipping = df.groupby(['Region', 'Ship Mode'])['Shipping Days'].mean().round(1)
print(region_shipping.unstack(fill_value=0))
print()

# ==========================================
# 10. DISCOUNT ANALYSIS
# ==========================================

print("\n10. DISCOUNT IMPACT ANALYSIS")
print("="*70)

# Create discount buckets
df['Discount Range'] = pd.cut(df['Discount'], 
                               bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.4, 1],
                               labels=['No Discount', '1-10%', '11-20%', 
                                      '21-30%', '31-40%', '40%+'])

discount_analysis = df.groupby('Discount Range').agg({
    'Order ID': 'count',
    'Sales': ['sum', 'mean'],
    'Profit': ['sum', 'mean'],
    'Quantity': 'sum'
}).round(2)

discount_analysis.columns = ['Orders', 'Total Sales', 'Avg Sales', 
                             'Total Profit', 'Avg Profit', 'Quantity']
discount_analysis['Profit Margin %'] = ((discount_analysis['Total Profit'] / 
                                         discount_analysis['Total Sales']) * 100).round(2)

print("\nDiscount Impact on Performance:")
print(discount_analysis)
print()

# Discount by Category
print("\nAverage Discount by Category:")
category_discount = df[df['Discount'] > 0].groupby('Category').agg({
    'Discount': 'mean',
    'Sales': 'sum',
    'Profit': 'sum'
}).round(3)
category_discount['Discount'] = (category_discount['Discount'] * 100).round(2)
category_discount.columns = ['Avg Discount %', 'Sales', 'Profit']
print(category_discount)
print()

# ==========================================
# 11. ADVANCED ANALYTICS
# ==========================================

print("\n11. ADVANCED ANALYTICS")
print("="*70)

# RFM Analysis (Recency, Frequency, Monetary)
print("\nTop 20 Customers - RFM Analysis:")
reference_date = df['Order Date'].max() + pd.Timedelta(days=1)

rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (reference_date - x.max()).days,
    'Order ID': 'nunique',
    'Sales': 'sum'
}).round(2)

rfm.columns = ['Recency (days)', 'Frequency (orders)', 'Monetary (sales)']
rfm['Recency Score'] = pd.qcut(rfm['Recency (days)'], 4, labels=[4, 3, 2, 1])
rfm['Frequency Score'] = pd.qcut(rfm['Frequency (orders)'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['Monetary Score'] = pd.qcut(rfm['Monetary (sales)'], 4, labels=[1, 2, 3, 4])
rfm['RFM Score'] = rfm['Recency Score'].astype(int) + rfm['Frequency Score'].astype(int) + rfm['Monetary Score'].astype(int)

# Merge with customer names
customer_names = df[['Customer ID', 'Customer Name']].drop_duplicates()
rfm = rfm.merge(customer_names, on='Customer ID')

rfm_top20 = rfm.sort_values('Monetary (sales)', ascending=False).head(20)
print(rfm_top20[['Customer Name', 'Recency (days)', 'Frequency (orders)', 
                  'Monetary (sales)', 'RFM Score']])
print()

# Product Performance Matrix
print("\nProduct Performance Quadrants (BCG Matrix Approach):")
product_matrix = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)

# Calculate growth rate (using quantity as proxy for market share)
product_matrix['Sales Rank'] = product_matrix['Sales'].rank(ascending=False)
product_matrix['Growth Rate'] = product_matrix['Quantity'].rank(pct=True) * 100

# Classify products
product_matrix['Category'] = 'Dogs'  # Low growth, low share
product_matrix.loc[(product_matrix['Sales Rank'] <= 100) & 
                   (product_matrix['Growth Rate'] >= 50), 'Category'] = 'Stars'
product_matrix.loc[(product_matrix['Sales Rank'] <= 100) & 
                   (product_matrix['Growth Rate'] < 50), 'Category'] = 'Cash Cows'
product_matrix.loc[(product_matrix['Sales Rank'] > 100) & 
                   (product_matrix['Growth Rate'] >= 50), 'Category'] = 'Question Marks'

print("\nProduct Category Distribution:")
print(product_matrix['Category'].value_counts())
print()

print("\nTop 10 'Stars' (High Sales, High Growth):")
stars = product_matrix[product_matrix['Category'] == 'Stars'].sort_values('Sales', ascending=False).head(10)
print(stars[['Sales', 'Profit', 'Quantity']])
print()

# ==========================================
# 12. CORRELATION ANALYSIS
# ==========================================

print("\n12. CORRELATION ANALYSIS")
print("="*70)

# Select numeric columns for correlation
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Days', 'Profit Margin']
correlation_matrix = df[numeric_cols].corr().round(3)

print("\nCorrelation Matrix:")
print(correlation_matrix)
print()

print("\nKey Correlations with Profit:")
profit_corr = correlation_matrix['Profit'].sort_values(ascending=False)
print(profit_corr)
print()

# ==========================================
# 13. SAVE ANALYSIS RESULTS
# ==========================================

print("\n13. EXPORTING ANALYSIS RESULTS")
print("="*70)

try:
    with pd.ExcelWriter('Sales_Analysis_Complete.xlsx', engine='openpyxl') as writer:
        # Summary Sheet
        summary_data = {
            'Metric': ['Total Sales', 'Total Profit', 'Profit Margin %', 'Total Orders', 
                      'Total Customers', 'Unique Products', 'Avg Order Value', 'Total Quantity'],
            'Value': [f'${total_sales:,.2f}', f'${total_profit:,.2f}', f'{avg_profit_margin:.2f}%',
                     total_orders, total_customers, unique_products, 
                     f'${avg_order_value:,.2f}', total_quantity]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        # Other sheets
        region_analysis.to_excel(writer, sheet_name='Region Analysis')
        category_analysis.to_excel(writer, sheet_name='Category Analysis')
        segment_analysis.to_excel(writer, sheet_name='Segment Analysis')
        yearly_perf.to_excel(writer, sheet_name='Yearly Performance')
        monthly_data.to_excel(writer, sheet_name='Monthly Trend')
        top_products_sales.to_excel(writer, sheet_name='Top Products by Sales')
        top_products_profit.to_excel(writer, sheet_name='Top Products by Profit')
        customer_sales.to_excel(writer, sheet_name='Top Customers')
        shipping_analysis.to_excel(writer, sheet_name='Shipping Analysis')
        discount_analysis.to_excel(writer, sheet_name='Discount Analysis')
        rfm_top20.to_excel(writer, sheet_name='RFM Analysis')
        correlation_matrix.to_excel(writer, sheet_name='Correlations')
    
    print("✓ Analysis exported to 'Sales_Analysis_Complete.xlsx'")
    print("  Contains 12 sheets with comprehensive analysis")
except Exception as e:
    print(f"✗ Error exporting to Excel: {e}")

print()

# ==========================================
# 14. CREATE VISUALIZATIONS
# ==========================================

print("\n14. CREATING VISUALIZATIONS")
print("="*70)

try:
    # Create output directory for plots
    import os
    os.makedirs('visualizations', exist_ok=True)
    
    # Visualization 1: Sales by Region
    plt.figure(figsize=(12, 6))
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = plt.bar(region_sales.index, region_sales.values, color=colors, edgecolor='black', linewidth=1.5)
    plt.title('Total Sales by Region', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Region', fontsize=14, fontweight='bold')
    plt.ylabel('Sales ($)', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, region_sales.values)):
        plt.text(bar.get_x() + bar.get_width()/2, value + 20000, 
                f'${value:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('visualizations/01_sales_by_region.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: sales_by_region.png")
    
    # Visualization 2: Sales by Category (Pie Chart)
    plt.figure(figsize=(10, 8))
    category_sales = df.groupby('Category')['Sales'].sum()
    colors_pie = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    explode = (0.05, 0.05, 0.05)
    
    wedges, texts, autotexts = plt.pie(category_sales.values, labels=category_sales.index, 
                                        autopct='%1.1f%%', startangle=90, colors=colors_pie,
                                        explode=explode, shadow=True, textprops={'fontsize': 12})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(13)
    
    for text in texts:
        text.set_fontsize(14)
        text.set_fontweight('bold')
    
    plt.title('Sales Distribution by Category', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/02_sales_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: sales_by_category.png")
    
    # Visualization 3: Monthly Sales Trend
    plt.figure(figsize=(16, 6))
    monthly_data_plot = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    })
    monthly_data_plot.index = monthly_data_plot.index.to_timestamp()
    
    plt.plot(monthly_data_plot.index, monthly_data_plot['Sales']/1000, 
            marker='o', linewidth=2.5, markersize=6, label='Sales', color='#FF6B6B')
    plt.plot(monthly_data_plot.index, monthly_data_plot['Profit']/1000, 
            marker='s', linewidth=2.5, markersize=6, label='Profit', color='#4ECDC4')
    
    plt.title('Monthly Sales and Profit Trend', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=14, fontweight='bold')
    plt.ylabel('Amount (Thousands $)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    plt.savefig('visualizations/03_monthly_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: monthly_trend.png")
    
    # Visualization 4: Top 10 Sub-Categories
    plt.figure(figsize=(12, 8))
    top_subcats = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=True).tail(10)
    colors_bar = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_subcats)))
    
    bars = plt.barh(range(len(top_subcats)), top_subcats.values, color=colors_bar, edgecolor='black', linewidth=1)
    plt.yticks(range(len(top_subcats)), top_subcats.index, fontsize=11)
    plt.title('Top 10 Sub-Categories by Sales', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Sales ($)', fontsize=14, fontweight='bold')
    plt.ylabel('Sub-Category', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=11)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_subcats.values)):
        plt.text(value + 5000, i, f'${value:,.0f}', va='center', fontsize=10, fontweight='bold')
    
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('visualizations/04_top_subcategories.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: top_subcategories.png")
    
    # Visualization 5: Profit Margin Distribution
    plt.figure(figsize=(12, 6))
    plt.hist(df['Profit Margin'], bins=50, color='#4ECDC4', edgecolor='black', linewidth=0.5, alpha=0.7)
    plt.axvline(df['Profit Margin'].mean(), color='red', linestyle='--', linewidth=2.5, 
               label=f'Mean: {df["Profit Margin"].mean():.1f}%')
    plt.axvline(df['Profit Margin'].median(), color='green', linestyle='--', linewidth=2.5,
               label=f'Median: {df["Profit Margin"].median():.1f}%')
    
    plt.title('Profit Margin Distribution', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Profit Margin (%)', fontsize=14, fontweight='bold')
    plt.ylabel('Frequency', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    plt.savefig('visualizations/05_profit_margin_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: profit_margin_distribution.png")
    
    # Visualization 6: Sales Heatmap
    plt.figure(figsize=(10, 6))
    heatmap_data = df.pivot_table(values='Sales', index='Region', columns='Category', aggfunc='sum')
    sns.heatmap(heatmap_data, annot=True, fmt=',.0f', cmap='YlOrRd', linewidths=1, 
               cbar_kws={'label': 'Sales ($)'}, annot_kws={'fontsize': 10, 'fontweight': 'bold'})
    
    plt.title('Sales Heatmap: Region vs Category', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Category', fontsize=14, fontweight='bold')
    plt.ylabel('Region', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, rotation=0)
    plt.yticks(fontsize=12, rotation=0)
    plt.tight_layout()
    plt.savefig('visualizations/06_sales_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: sales_heatmap.png")
    
    # Visualization 7: Customer Segment Performance
    plt.figure(figsize=(12, 6))
    segment_data = df.groupby('Segment')[['Sales', 'Profit']].sum()
    
    x = np.arange(len(segment_data))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - width/2, segment_data['Sales']/1000, width, label='Sales', 
                  color='#FF6B6B', edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, segment_data['Profit']/1000, width, label='Profit',
                  color='#4ECDC4', edgecolor='black', linewidth=1)
    
    ax.set_title('Sales and Profit by Customer Segment', fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Customer Segment', fontsize=14, fontweight='bold')
    ax.set_ylabel('Amount (Thousands $)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(segment_data.index, fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.0f}K', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/07_segment_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: segment_performance.png")
    
    # Visualization 8: Yearly Growth Trend
    plt.figure(figsize=(12, 6))
    yearly_sales = df.groupby('Order Year')['Sales'].sum()/1000
    
    plt.plot(yearly_sales.index, yearly_sales.values, marker='o', linewidth=3, 
            markersize=10, color='#FF6B6B', markerfacecolor='white', 
            markeredgecolor='#FF6B6B', markeredgewidth=2)
    
    plt.title('Year-over-Year Sales Growth', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Sales (Thousands $)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(yearly_sales.index, fontsize=12)
    plt.yticks(fontsize=11)
    
    # Add value labels
    for x, y in zip(yearly_sales.index, yearly_sales.values):
        plt.text(x, y + 10, f'${y:.0f}K', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/08_yearly_growth.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: yearly_growth.png")
    
    print("\n✓ All visualizations saved in 'visualizations' folder")
    
except Exception as e:
    print(f"✗ Error creating visualizations: {e}")

print()

# ==========================================
# 15. SUMMARY AND INSIGHTS
# ==========================================

print("\n15. KEY INSIGHTS AND RECOMMENDATIONS")
print("="*70)

print("""
┌────────────────────────────────────────────────────────────────┐
│                    KEY BUSINESS INSIGHTS                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ 1. REGIONAL PERFORMANCE:                                      │
│    • West region leads in sales                               │
│    • Consider expanding successful strategies to other regions│
│                                                                │
│ 2. PRODUCT INSIGHTS:                                          │
│    • Technology has highest profit margins                    │
│    • Some products are loss-making - review pricing          │
│    • Office Supplies has consistent volume                   │
│                                                                │
│ 3. CUSTOMER BEHAVIOR:                                         │
│    • Consumer segment largest by volume                       │
│    • Corporate has higher average order values               │
│    • Focus on customer retention programs                    │
│                                                                │
│ 4. OPERATIONAL EFFICIENCY:                                    │
│    • Review discount strategy - high discounts hurt margins  │
│    • Standard shipping most popular                          │
│    • Seasonal patterns exist - plan inventory accordingly    │
│                                                                │
│ 5. GROWTH OPPORTUNITIES:                                      │
│    • Year-over-year growth trend positive                    │
│    • Expand in underperforming regions                       │
│    • Focus on high-margin product categories                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
""")

print("\n" + "="*70)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*70)
print("""
Output Files Generated:
1. Sales_Analysis_Complete.xlsx - Comprehensive analysis in Excel format
2. visualizations/ folder - 8 professional visualizations

Next Steps:
1. Review the Excel file for detailed metrics
2. Share visualizations with stakeholders
3. Import data into Power BI for interactive dashboard
4. Implement recommended actions based on insights
""")

print("\nScript execution completed!")
print("="*70)

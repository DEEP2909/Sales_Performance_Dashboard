# POWER BI DASHBOARD - COMPLETE SETUP GUIDE

## Table of Contents
1. [Getting Started](#getting-started)
2. [Data Import and Transformation](#data-import-and-transformation)
3. [DAX Measures](#dax-measures)
4. [Dashboard Design](#dashboard-design)
5. [Visualizations](#visualizations)
6. [Publishing](#publishing)

---

## 1. Getting Started

### Prerequisites
- Power BI Desktop (Download from: https://powerbi.microsoft.com/desktop/)
- Sample_Superstore.csv file

### Opening Power BI
1. Launch Power BI Desktop
2. Sign in with your Microsoft account
3. Close the welcome screen

---

## 2. Data Import and Transformation

### Step 2.1: Import CSV File

1. Click **Get Data** → **Text/CSV**
2. Navigate to `Sample_Superstore.csv`
3. Click **Open**
4. Preview window appears - Click **Transform Data**

### Step 2.2: Data Cleaning in Power Query

```powerquery
// Power Query M Code

// Step 1: Promote first row to headers (if needed)
= Table.PromoteHeaders(Source)

// Step 2: Change data types
= Table.TransformColumnTypes(#"Promoted Headers",{
    {"Row ID", Int64.Type},
    {"Order ID", type text},
    {"Order Date", type date},
    {"Ship Date", type date},
    {"Ship Mode", type text},
    {"Customer ID", type text},
    {"Customer Name", type text},
    {"Segment", type text},
    {"Country", type text},
    {"City", type text},
    {"State", type text},
    {"Postal Code", type text},
    {"Region", type text},
    {"Product ID", type text},
    {"Category", type text},
    {"Sub-Category", type text},
    {"Product Name", type text},
    {"Sales", Currency.Type},
    {"Quantity", Int64.Type},
    {"Discount", Percentage.Type},
    {"Profit", Currency.Type}
})

// Step 3: Remove any errors
= Table.RemoveRowsWithErrors(#"Changed Type")

// Step 4: Add custom columns
```

### Step 2.3: Add Calculated Columns

**Add these columns in Power Query:**

1. **Profit Margin**
```powerquery
= Table.AddColumn(#"Previous Step", "Profit Margin", 
    each [Profit] / [Sales], type number)
```

2. **Order Year**
```powerquery
= Table.AddColumn(#"Added Profit Margin", "Order Year", 
    each Date.Year([Order Date]), Int64.Type)
```

3. **Order Month**
```powerquery
= Table.AddColumn(#"Added Order Year", "Order Month", 
    each Date.Month([Order Date]), Int64.Type)
```

4. **Order Month Name**
```powerquery
= Table.AddColumn(#"Added Order Month", "Order Month Name", 
    each Date.MonthName([Order Date]), type text)
```

5. **Order Quarter**
```powerquery
= Table.AddColumn(#"Added Month Name", "Order Quarter", 
    each "Q" & Text.From(Date.QuarterOfYear([Order Date])), type text)
```

6. **Shipping Days**
```powerquery
= Table.AddColumn(#"Added Quarter", "Shipping Days", 
    each Duration.Days([Ship Date] - [Order Date]), Int64.Type)
```

7. **Year-Month**
```powerquery
= Table.AddColumn(#"Added Shipping Days", "Year-Month", 
    each Date.ToText([Order Date], "yyyy-MM"), type text)
```

Click **Close & Apply** when done.

---

## 3. DAX Measures

### Create a Measures Table

1. Go to **Modeling** tab → **New Table**
2. Enter: `Measures = ROW("Dummy", 1)`
3. Right-click on the table → Hide

### Basic KPI Measures

```dax
// Total Sales
Total Sales = SUM(Superstore[Sales])

// Total Profit
Total Profit = SUM(Superstore[Profit])

// Total Orders
Total Orders = DISTINCTCOUNT(Superstore[Order ID])

// Total Customers
Total Customers = DISTINCTCOUNT(Superstore[Customer ID])

// Total Quantity
Total Quantity = SUM(Superstore[Quantity])

// Average Order Value
Avg Order Value = DIVIDE([Total Sales], [Total Orders], 0)

// Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0) * 100

// Number of Products
Number of Products = DISTINCTCOUNT(Superstore[Product ID])
```

### Time Intelligence Measures

```dax
// Year-to-Date Sales
YTD Sales = TOTALYTD([Total Sales], Superstore[Order Date])

// Year-to-Date Profit
YTD Profit = TOTALYTD([Total Profit], Superstore[Order Date])

// Previous Year Sales
PY Sales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Superstore[Order Date]))

// Previous Year Profit
PY Profit = CALCULATE([Total Profit], SAMEPERIODLASTYEAR(Superstore[Order Date]))

// Year-over-Year Sales Growth
YoY Sales Growth = 
VAR CurrentSales = [Total Sales]
VAR PreviousSales = [PY Sales]
RETURN
    DIVIDE(CurrentSales - PreviousSales, PreviousSales, 0)

// Year-over-Year Sales Growth %
YoY Sales Growth % = [YoY Sales Growth] * 100

// Month-over-Month Sales Growth
MoM Sales Growth % = 
VAR CurrentSales = [Total Sales]
VAR PreviousMonthSales = CALCULATE([Total Sales], DATEADD(Superstore[Order Date], -1, MONTH))
RETURN
    DIVIDE(CurrentSales - PreviousMonthSales, PreviousMonthSales, 0) * 100

// Quarter-to-Date Sales
QTD Sales = TOTALQTD([Total Sales], Superstore[Order Date])

// Quarter-to-Date Profit
QTD Profit = TOTALQTD([Total Profit], Superstore[Order Date])

// Month-to-Date Sales
MTD Sales = TOTALMTD([Total Sales], Superstore[Order Date])

// Month-to-Date Profit
MTD Profit = TOTALMTD([Total Profit], Superstore[Order Date])
```

### Ranking and Top N Measures

```dax
// Sales Rank (by Region)
Sales Rank by Region = 
RANKX(
    ALL(Superstore[Region]),
    [Total Sales],
    ,
    DESC,
    Dense
)

// Top 10 Products by Sales
Top 10 Products Sales = 
IF(
    RANKX(ALL(Superstore[Product Name]), [Total Sales], , DESC) <= 10,
    [Total Sales],
    BLANK()
)

// Top 20 Customers Flag
Is Top 20 Customer = 
IF(
    RANKX(ALL(Superstore[Customer Name]), [Total Sales], , DESC) <= 20,
    "Top 20",
    "Others"
)
```

### Conditional Measures

```dax
// High Value Orders
High Value Orders = 
CALCULATE(
    [Total Orders],
    FILTER(Superstore, Superstore[Sales] > 1000)
)

// Low Profit Margin Orders
Low Margin Orders = 
CALCULATE(
    [Total Orders],
    FILTER(Superstore, DIVIDE(Superstore[Profit], Superstore[Sales]) < 0.1)
)

// Discount Impact
Avg Discount % = AVERAGE(Superstore[Discount]) * 100

// Orders with Discount
Orders with Discount = 
CALCULATE(
    [Total Orders],
    FILTER(Superstore, Superstore[Discount] > 0)
)

// Discount % of Total
Discount Rate = DIVIDE([Orders with Discount], [Total Orders], 0) * 100
```

### Customer Analytics Measures

```dax
// Average Customer Lifetime Value
Avg Customer Value = DIVIDE([Total Sales], [Total Customers], 0)

// Repeat Customers
Repeat Customers = 
CALCULATE(
    DISTINCTCOUNT(Superstore[Customer ID]),
    FILTER(
        VALUES(Superstore[Customer ID]),
        CALCULATE(DISTINCTCOUNT(Superstore[Order ID])) > 1
    )
)

// Repeat Customer Rate
Repeat Customer Rate % = DIVIDE([Repeat Customers], [Total Customers], 0) * 100

// Average Orders per Customer
Avg Orders per Customer = DIVIDE([Total Orders], [Total Customers], 0)
```

### Product Performance Measures

```dax
// Products Sold
Products Sold = DISTINCTCOUNT(Superstore[Product ID])

// Average Product Price
Avg Product Price = DIVIDE([Total Sales], [Total Quantity], 0)

// Best Selling Product
Best Selling Product = 
CALCULATE(
    FIRSTNONBLANK(Superstore[Product Name], 1),
    TOPN(1, ALL(Superstore[Product Name]), [Total Sales], DESC)
)

// Most Profitable Product
Most Profitable Product = 
CALCULATE(
    FIRSTNONBLANK(Superstore[Product Name], 1),
    TOPN(1, ALL(Superstore[Product Name]), [Total Profit], DESC)
)
```

### Shipping and Logistics Measures

```dax
// Average Shipping Days
Avg Shipping Days = AVERAGE(Superstore[Shipping Days])

// Same Day Shipments
Same Day Shipments = 
CALCULATE(
    [Total Orders],
    Superstore[Ship Mode] = "Same Day"
)

// Standard Shipments
Standard Shipments = 
CALCULATE(
    [Total Orders],
    Superstore[Ship Mode] = "Standard Class"
)

// On-Time Delivery Rate (assuming <= 4 days is on-time)
On Time Deliveries = 
CALCULATE(
    [Total Orders],
    FILTER(Superstore, Superstore[Shipping Days] <= 4)
)

// On-Time Rate %
On Time Rate % = DIVIDE([On Time Deliveries], [Total Orders], 0) * 100
```

### Advanced Analytics Measures

```dax
// Sales Contribution %
Sales Contribution % = 
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(Superstore)),
    0
) * 100

// Profit Contribution %
Profit Contribution % = 
DIVIDE(
    [Total Profit],
    CALCULATE([Total Profit], ALL(Superstore)),
    0
) * 100

// Running Total Sales
Running Total Sales = 
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Superstore[Order Date]),
        Superstore[Order Date] <= MAX(Superstore[Order Date])
    )
)

// Cumulative Profit
Cumulative Profit = 
CALCULATE(
    [Total Profit],
    FILTER(
        ALL(Superstore[Order Date]),
        Superstore[Order Date] <= MAX(Superstore[Order Date])
    )
)

// 3-Month Moving Average Sales
3M Avg Sales = 
CALCULATE(
    [Total Sales],
    DATESINPERIOD(
        Superstore[Order Date],
        LASTDATE(Superstore[Order Date]),
        -3,
        MONTH
    )
) / 3

// Sales Target (Example: 10% more than previous year)
Sales Target = [PY Sales] * 1.1

// Sales vs Target
Sales vs Target = [Total Sales] - [Sales Target]

// Target Achievement %
Target Achievement % = DIVIDE([Total Sales], [Sales Target], 0) * 100
```

---

## 4. Dashboard Design

### Dashboard Structure

**Page 1: Executive Summary**
- Purpose: High-level overview for executives
- Layout: 4 KPI cards at top, 4-5 key visuals below

**Page 2: Sales Analysis**
- Purpose: Detailed sales breakdown
- Layout: Trends, comparisons, and drill-downs

**Page 3: Product Performance**
- Purpose: Product-level insights
- Layout: Category analysis, top/bottom products

**Page 4: Customer Analytics**
- Purpose: Customer behavior and segmentation
- Layout: Customer metrics, RFM analysis

**Page 5: Regional Analysis**
- Purpose: Geographic performance
- Layout: Maps, regional comparisons

### Color Scheme Recommendations

**Primary Colors:**
- Sales: #FF6B6B (Coral Red)
- Profit: #4ECDC4 (Turquoise)
- Quantity: #45B7D1 (Light Blue)
- Accent: #FFA07A (Light Salmon)

**Backgrounds:**
- Page Background: #F7F9FC (Light Gray-Blue)
- Card Background: #FFFFFF (White)
- Header: #2C3E50 (Dark Blue-Gray)

---

## 5. Visualizations

### Page 1: Executive Summary

**Visual 1: KPI Cards (Top Row)**
```
Card 1: Total Sales
- Field: [Total Sales]
- Format: Currency, $#,##0

Card 2: Total Profit
- Field: [Total Profit]
- Format: Currency, $#,##0

Card 3: Profit Margin %
- Field: [Profit Margin %]
- Format: Percentage, #0.00%

Card 4: Total Orders
- Field: [Total Orders]
- Format: Whole Number, #,##0
```

**Visual 2: Monthly Sales Trend (Line Chart)**
```
X-axis: Order Date (Month)
Y-axis: Total Sales
Legend: (Optional) Category
Tooltips: Total Profit, Profit Margin %
```

**Visual 3: Sales by Region (Bar Chart)**
```
Axis: Region
Values: Total Sales, Total Profit
Data Labels: On
Sort: By Total Sales, Descending
```

**Visual 4: Sales by Category (Donut Chart)**
```
Legend: Category
Values: Total Sales
Details: Show percentage
Labels: Category name and value
```

**Visual 5: Top 10 Products (Table)**
```
Columns:
- Product Name
- Total Sales
- Total Profit
- Profit Margin %
Sort: By Total Profit, Descending
Top N Filter: 10
```

**Visual 6: Geographic Sales (Filled Map)**
```
Location: State
Size: Total Sales
Color Saturation: Total Profit
Tooltips: City, Orders, Customers
```

### Page 2: Sales Analysis

**Visual 1: YoY Sales Comparison (Clustered Column)**
```
Axis: Order Year
Values: Total Sales, PY Sales
Legend: Measure names
Data Labels: On
```

**Visual 2: Sales by Segment (Clustered Bar)**
```
Axis: Segment
Values: Total Sales, Total Profit
Colors: Custom (use color scheme)
```

**Visual 3: Sales Trend with Forecast (Line Chart)**
```
X-axis: Order Date
Y-axis: Total Sales
Analytics: Add forecast (6 months)
Analytics: Add average line
```

**Visual 4: Sales by Sub-Category (Matrix)**
```
Rows: Category, Sub-Category
Values: Total Sales, Total Profit, Profit Margin %
Conditional Formatting: On Profit Margin %
```

### Page 3: Product Performance

**Visual 1: Category Performance (Stacked Bar)**
```
Axis: Category
Values: Total Sales
Legend: Order Year
```

**Visual 2: Product Treemap**
```
Group: Category
Details: Sub-Category
Values: Total Sales
Color Saturation: Profit Margin %
```

**Visual 3: Top 20 Products Table**
```
Product Name, Sales, Profit, Quantity, Profit Margin %
Conditional formatting on Profit
Top N: 20
```

**Visual 4: Bottom 10 Products (by Profit)**
```
Product Name, Sales, Profit, Discount %
Shows loss-making products
```

### Page 4: Customer Analytics

**Visual 1: Customer Segment KPIs (Cards)**
```
- Total Customers
- Avg Customer Value
- Repeat Customer Rate %
```

**Visual 2: Top Customers (Table)**
```
Customer Name, Segment, Total Sales, Orders
Top N: 30
```

**Visual 3: RFM Scatter Plot**
```
X-axis: Frequency (Orders)
Y-axis: Monetary (Sales)
Size: Recency
Color: Segment
```

**Visual 4: Customer Distribution (Histogram)**
```
Show customer count by purchase value ranges
```

### Page 5: Regional Analysis

**Visual 1: Sales by State (Filled Map)**
```
Location: State
Size: Total Sales
Color: Profit Margin %
```

**Visual 2: Regional Matrix**
```
Rows: Region, State
Values: Sales, Profit, Orders, Customers
Drill-down enabled
```

**Visual 3: Region vs Category Heatmap**
```
Rows: Region
Columns: Category
Values: Total Sales
Color Scale: High = Green, Low = Red
```

### Common Slicers (All Pages)

```
Slicer 1: Date Range
- Field: Order Date
- Style: Between

Slicer 2: Region
- Field: Region
- Style: Dropdown

Slicer 3: Category
- Field: Category
- Style: List

Slicer 4: Segment
- Field: Segment
- Style: Button

Slicer 5: Ship Mode
- Field: Ship Mode
- Style: Dropdown
```

---

## 6. Publishing

### Step 1: Save Your Work
- File → Save As
- Name: "Sales_Performance_Dashboard.pbix"
- Location: Choose appropriate folder

### Step 2: Publish to Power BI Service

1. Click **Publish** button (Home tab)
2. Sign in to Power BI Service
3. Select workspace (My Workspace or team workspace)
4. Click **Select**
5. Wait for upload to complete

### Step 3: Configure Refresh (if using live data)

1. Go to powerbi.com
2. Navigate to your dataset
3. Click Settings (gear icon)
4. Schedule refresh:
   - Frequency: Daily
   - Time: Select appropriate time
   - Time zone: Your time zone
   - Email notifications: On (for failures)

### Step 4: Share Dashboard

**Option 1: Share Link**
1. Open report in Power BI Service
2. Click **Share** button
3. Enter email addresses
4. Set permissions
5. Click **Share**

**Option 2: Publish to Web (Public)**
1. File → Publish to web
2. Create embed code
3. Copy and share link
⚠️ Warning: Anyone with link can view

**Option 3: Create App**
1. Create an app from workspace
2. Add dashboard to app
3. Publish app
4. Share app with users

---

## 7. Best Practices

### Performance Optimization

1. **Use Measures Instead of Calculated Columns**
   - Calculated columns stored in memory
   - Measures calculated on-demand
   - Measures more efficient for large datasets

2. **Minimize Use of CALCULATE**
   - Use filter context when possible
   - Avoid nested CALCULATE functions
   - Consider creating intermediate measures

3. **Optimize Relationships**
   - Use star schema design
   - Avoid many-to-many relationships
   - Hide unnecessary columns

4. **Data Model Best Practices**
   - Remove unused columns
   - Use appropriate data types
   - Create date table for time intelligence

### Design Guidelines

1. **Consistency**
   - Use same color scheme throughout
   - Maintain consistent font sizes
   - Align visuals properly

2. **Clarity**
   - Use clear, descriptive titles
   - Add helpful tooltips
   - Include legends when needed

3. **Interactivity**
   - Enable cross-filtering
   - Add drill-down capabilities
   - Use bookmarks for different views

4. **Mobile Optimization**
   - Create mobile layout
   - Test on mobile devices
   - Use large touch targets

---

## 8. Troubleshooting

### Common Issues

**Issue 1: Relationships Not Working**
- Solution: Check cardinality and cross-filter direction
- Go to Model view → Manage relationships

**Issue 2: Measures Showing Wrong Values**
- Solution: Check filter context
- Use CALCULATE with ALL() to override filters

**Issue 3: Slow Performance**
- Solution: Reduce data size or optimize DAX
- Use performance analyzer tool

**Issue 4: Date Intelligence Not Working**
- Solution: Ensure continuous date table exists
- Mark as date table in model view

---

## 9. Additional Resources

- **Microsoft Power BI Documentation**: https://docs.microsoft.com/power-bi/
- **DAX Guide**: https://dax.guide/
- **Power BI Community**: https://community.powerbi.com/
- **SQLBI (Advanced DAX)**: https://www.sqlbi.com/

---

**Created by**: Data Analytics Team
**Version**: 1.0
**Last Updated**: February 2026

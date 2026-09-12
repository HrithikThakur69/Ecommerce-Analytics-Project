# E-Commerce Sales & Customer Analytics - Final Capstone Project

## Project Overview
This is the final capstone project for the InternNova Data Analytics internship, applying every skill covered across the program - data cleaning, exploratory data analysis (EDA), statistical analysis, data visualization, Power BI dashboarding, and Git/GitHub version control - to a single, real-world-style dataset from start to finish.

## Problem Statement
An e-commerce business wants to understand its sales performance: which product categories and cities drive the most revenue, what factors influence order value and customer satisfaction, where returns are concentrated, and what data-driven actions could improve revenue and reduce return-related losses. This project analyzes 400 cleaned customer orders to answer those questions.

## Dataset Description
**`data/ecommerce_orders_cleaned.csv`** - 400 order-level records, 15 columns:

| Column | Description |
|---|---|
| order_id | Unique order identifier |
| order_date | Date the order was placed (2024) |
| customer_id | Unique customer identifier (161 distinct customers) |
| customer_age | Customer's age |
| customer_gender | Male / Female |
| customer_city | One of 8 Indian cities |
| product_category | Electronics, Apparel, Home & Kitchen, Sports, Beauty, or Books |
| product_price | Unit price (INR) |
| quantity | Units purchased in the order |
| discount_pct | Discount applied (%) |
| total_amount | Final order value after discount (INR) |
| payment_method | Credit Card, Debit Card, UPI, Net Banking, or Cash on Delivery |
| delivery_days | Days from order to delivery |
| customer_rating | Customer's rating of the order (1-5) |
| is_returned | Whether the order was returned |

The original raw file (`data/ecommerce_orders_raw.csv`, 403 rows) intentionally included missing values, duplicate rows, and an inconsistent negative value, to give the cleaning process in Task 3 real issues to solve.

## Tools Used
- **Python** (pandas, numpy, scipy) - data cleaning, EDA, statistical analysis
- **Matplotlib & Seaborn** - data visualization
- **Power BI Desktop** - interactive dashboard (see note below)
- **Git & GitHub** - version control and project hosting

> **Note on Power BI:** this project's Python development environment cannot run Power BI Desktop (a Windows-only application). The `powerbi/` folder contains everything needed to build the real dashboard yourself: the cleaned dataset, exact DAX formulas with independently validated expected results, a target-layout mockup image, and a full step-by-step guide (`powerbi/powerbi_stepbystep.md`).

## Data Cleaning Process (Task 3)
Performed in `notebooks/task3_data_preparation.py`:
1. Inspected the raw dataset (403 rows, 15 columns) - checked shape, dtypes, and missing values
2. Filled missing values in `customer_age`, `customer_rating`, `delivery_days`, and `total_amount` with each column's median
3. Identified and removed 3 duplicate rows
4. Found and corrected 1 inconsistent value (a negative `delivery_days` entry)
5. Corrected data types (`order_date` to datetime, `customer_age` to integer, `is_returned` to boolean)

**Result:** 403 rows -> 400 clean rows, 0 missing values, 0 duplicates.

## Exploratory Data Analysis (Task 4)
Performed in `notebooks/task4_eda.py`. Highlights:
- Descriptive statistics and category/city/payment-method breakdowns
- Correlation analysis across all numeric variables (see `visualizations/chart7_correlation_heatmap.png`)
- **Key finding:** order quantity correlates with order value (r=0.72) far more strongly than unit price does (r=0.26)
- Outlier detection using the IQR method, done **per product category** rather than globally - this avoided falsely flagging normal Electronics purchases (which are naturally higher-priced) while still catching genuine high-quantity outliers in cheaper categories

## Visualizations (Task 5)
7 charts in `visualizations/` (exceeds the required 5):
1. Line chart - Monthly Sales Trend
2. Bar chart - Total Sales by Category
3. Histogram - Order Value Distribution
4. Scatter plot - Product Price vs Total Amount (by category)
5. Box plot - Delivery Time by Category
6. Pie chart - Orders by Payment Method
7. Heatmap - Correlation between numeric variables

## Power BI Dashboard (Task 6)
See `powerbi/` for the DAX measures, validated expected results, target dashboard mockup (`dashboard_mockup.png`), and step-by-step build guide.

**Dashboard includes:** 4 KPI cards (Total Sales, Total Orders, Average Order Value, Return Rate), 5 visualizations (bar, line, donut, table, bar), and 2 slicers (Category, Payment Method).

**Key metrics:**
| Metric | Value |
|---|---|
| Total Sales | Rs.2,905,382 |
| Total Orders | 400 |
| Average Order Value | Rs.7,263 |
| Return Rate | 9.2% |

## Key Insights (Task 7)
1. **Electronics dominates revenue** (Rs.1,519,856) despite lower order volume than other categories - driven by high per-unit prices.
2. **Quantity purchased matters more than unit price** for order value (r=0.72 vs r=0.26) - bundling strategies likely outperform price discounting.
3. **Sales are geographically concentrated** - Delhi alone leads all cities at Rs.570,617.
4. **Sports has a notably high return rate** (20.0%) versus the 9.2% company average, well above every other category.
5. **UPI is the dominant payment method** (32% of orders), ahead of all card and cash options.
6. Sales show a **volatile but generally healthy trend** across the year, with March's spike partly driven by a single large bulk order.

Full details with supporting figures: `notebooks/task7_insights_recommendations.py` and its output in `outputs/task7_insights_recommendations.txt`.

## Business Recommendations
1. **Promote bundle deals and multi-buy discounts** rather than relying on per-item price discounting, since order quantity drives order value far more than price does.
2. **Investigate the elevated Sports return rate** before scaling marketing spend in that category, to protect margin rather than just top-line sales.
3. **Double down on Delhi while piloting targeted campaigns** in lower-performing cities to test whether the gap is a demand or an awareness issue.

## Conclusion
This project took a raw, imperfect e-commerce dataset through the complete analytics lifecycle: cleaning, exploration, visualization, dashboarding, and business storytelling. The most actionable finding - that basket size predicts order value far better than pricing does - directly challenges an intuitive assumption (that pricing strategy is the primary revenue lever) and points toward a concrete, testable business action: bundling over discounting.

## Repository Structure
```
project_repo/
├── README.md
├── GIT_WORKFLOW.md
├── data/
│   ├── ecommerce_orders_raw.csv
│   └── ecommerce_orders_cleaned.csv
├── notebooks/
│   ├── task3_data_preparation.py
│   ├── task4_eda.py
│   ├── task5_visualizations.py
│   ├── task6_powerbi_dashboard.py
│   └── task7_insights_recommendations.py
├── visualizations/
│   └── chart1_*.png ... chart7_*.png
├── powerbi/
│   ├── dashboard_mockup.png
│   └── powerbi_stepbystep.md
└── presentation/
    └── Capstone_Presentation.pptx
```

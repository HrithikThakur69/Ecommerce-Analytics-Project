# Power BI Dashboard - Step-by-Step Instructions

> **Important note:** Power BI Desktop is a Windows-only application and
> cannot run in this project's sandboxed development environment. This guide,
> together with `ecommerce_orders_cleaned.csv` and the validated DAX results
> in `outputs/task6_powerbi_dashboard.txt`, gives you everything needed to
> build the real, interactive dashboard in Power BI Desktop and produce
> genuine screenshots for submission. `dashboard_mockup.png` shows the
> target layout.

## 1. Import the Data

**Get Data > Text/CSV >** `ecommerce_orders_cleaned.csv`. Rename the table
to `Orders` in the Fields pane. Confirm data types: `order_date` as Date,
`customer_rating`/`product_price`/`total_amount`/`delivery_days` as Decimal
Number, `is_returned` as True/False, everything else as Text or Whole Number.

## 2. Create the DAX Measures

**Modeling > New Measure**, one at a time:

```
Total Sales = SUM(Orders[total_amount])
Average Order Value = AVERAGE(Orders[total_amount])
Total Orders = COUNTROWS(Orders)
Total Customers = DISTINCTCOUNT(Orders[customer_id])
Return Rate % = DIVIDE(CALCULATE(COUNTROWS(Orders), Orders[is_returned] = TRUE), [Total Orders], 0)
Average Rating = AVERAGE(Orders[customer_rating])
Average Delivery Days = AVERAGE(Orders[delivery_days])
```

Expected results (validated independently in Python - confirm your Power BI
cards match):

| Measure | Expected Value |
|---|---|
| Total Sales | Rs.2,905,382 |
| Average Order Value | Rs.7,263.45 |
| Total Orders | 400 |
| Total Customers | 161 |
| Return Rate % | 9.2% |
| Average Rating | 4.01 / 5 |
| Average Delivery Days | 4.0 days |

## 3. Build the Dashboard

On a new report page titled **"E-Commerce Sales & Customer Dashboard"**:

**KPI Cards (4):** Total Sales, Total Orders, Average Order Value, Return Rate %

**Visualizations (5):**
| Visual | Fields |
|---|---|
| Bar Chart | Axis = `product_category`, Values = `[Total Sales]` — title "Total Sales by Category" |
| Line Chart | Axis = `order_date` (by Month), Values = `[Total Sales]` — title "Monthly Sales Trend" |
| Donut Chart | Legend = `payment_method`, Values = `[Total Orders]` — title "Orders by Payment Method" |
| Table | Rows = `customer_city`, Values = `[Total Sales]`, Top N filter = 5 — title "Top 5 Cities by Sales" |
| Bar Chart | Axis = `product_category`, Values = `[Return Rate %]` — title "Return Rate % by Category" |

**Slicers (2):** `product_category` and `payment_method`

Arrange KPI cards along the top, slicers top-right, 5 visuals in a grid
below — no overlaps, consistent spacing, clear titles on every visual.

## 4. Test Interactivity

Click a slicer option (e.g., Category = "Electronics") and confirm every
KPI and chart updates. Click a bar in one chart and confirm the others
cross-highlight. This live filtering only works in the real Power BI
Desktop app, not in the static mockup image.

**Screenshot to capture:** The full dashboard page, ideally with a slicer
selection applied so interactivity is visible.

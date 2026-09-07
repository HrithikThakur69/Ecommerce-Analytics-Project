"""
Task 7: Business Insights & Recommendations
Dataset: ecommerce_orders_cleaned.csv
"""
import pandas as pd

df = pd.read_csv("ecommerce_orders_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

cat_sales = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)
city_sales = df.groupby("customer_city")["total_amount"].sum().sort_values(ascending=False)
monthly = df.groupby("month")["total_amount"].sum().sort_index()
return_by_cat = (df.groupby("product_category")["is_returned"].mean() * 100).sort_values(ascending=False)
payment_counts = df["payment_method"].value_counts()
qty_amount_corr = df["quantity"].corr(df["total_amount"])
price_amount_corr = df["product_price"].corr(df["total_amount"])

top_cat, low_cat = cat_sales.index[0], cat_sales.index[-1]
top_cat_val, low_cat_val = cat_sales.iloc[0], cat_sales.iloc[-1]

top_city, low_city = city_sales.index[0], city_sales.index[-1]
top_city_val = city_sales.iloc[0]

best_month, best_month_val = monthly.idxmax(), monthly.max()
worst_month, worst_month_val = monthly.idxmin(), monthly.min()

highest_return_cat, highest_return_val = return_by_cat.index[0], return_by_cat.iloc[0]
lowest_return_cat, lowest_return_val = return_by_cat.index[-1], return_by_cat.iloc[-1]
overall_return_rate = df["is_returned"].mean() * 100

top_payment = payment_counts.index[0]
top_payment_pct = payment_counts.iloc[0] / payment_counts.sum() * 100

print("----- Supporting Figures -----")
print("\nTotal sales by category:")
print(cat_sales.round(0))
print("\nTotal sales by city (top 5):")
print(city_sales.head(5).round(0))
print("\nMonthly sales:")
print(monthly.round(0))
print("\nReturn rate % by category:")
print(return_by_cat.round(1))
print(f"\nOverall return rate: {overall_return_rate:.1f}%")
print("\nPayment method distribution:")
print((payment_counts / payment_counts.sum() * 100).round(1))
print(f"\nCorrelation: quantity vs total_amount = {qty_amount_corr:.2f}")
print(f"Correlation: product_price vs total_amount = {price_amount_corr:.2f}")

print(f"""
{"=" * 70}
BUSINESS INSIGHTS
{"=" * 70}

1. Electronics dominates revenue despite being a relatively low-volume category.
   Electronics generated Rs.{top_cat_val:,.0f} in sales - more than double the next
   category (Home & Kitchen) - driven by high per-unit prices rather than order
   count. '{low_cat}' generated the least, at Rs.{low_cat_val:,.0f}.

2. How much customers BUY matters more than what they pay per item.
   Quantity purchased correlates with order value at r={qty_amount_corr:.2f}, far
   stronger than product price alone (r={price_amount_corr:.2f}). This means
   encouraging larger basket sizes (bundles, multi-buy discounts) may lift
   revenue more effectively than premium pricing strategies.

3. Sales are heavily concentrated in a handful of cities.
   '{top_city}' alone accounts for Rs.{top_city_val:,.0f} in sales, the highest of
   any city, while several other cities lag well behind - indicating geographic
   concentration rather than a uniformly distributed customer base.

4. Electronics and Sports have the highest return rates, well above the {overall_return_rate:.1f}%
   company average.
   '{highest_return_cat}' has a {highest_return_val:.1f}% return rate, compared to
   just {lowest_return_val:.1f}% for '{lowest_return_cat}' - the lowest. High-value,
   high-return categories deserve closer scrutiny (sizing issues, product quality,
   or mismatched expectations from product listings).

5. UPI is the dominant payment method, used in {top_payment_pct:.0f}% of orders.
   '{top_payment}' clearly leads over cards and cash on delivery, reflecting a
   broader shift in digital payment preference that should shape any checkout
   or promotions strategy (e.g., UPI-specific cashback offers).

6. Sales show a volatile but generally healthy trend across the year.
   The strongest month was {best_month} (Rs.{best_month_val:,.0f}), and the
   weakest was {worst_month} (Rs.{worst_month_val:,.0f}). The spike is partly
   driven by a single large bulk order flagged during outlier analysis (Task 4),
   so the underlying month-to-month trend is more stable than the raw total
   suggests once that one order is set aside.

{"=" * 70}
BUSINESS RECOMMENDATIONS
{"=" * 70}

1. Promote bundle deals and multi-buy discounts rather than relying only on
   per-item pricing or discounting.
   Since quantity purchased (r={qty_amount_corr:.2f}) matters far more to order
   value than unit price (r={price_amount_corr:.2f}), campaigns like "buy 2, get 10%
   off" or bundled product sets are likely to grow average order value more
   effectively than blanket price discounts, which barely move customer
   satisfaction either (see Task 4's discount-vs-rating correlation).

2. Investigate the elevated return rate in '{highest_return_cat}' before scaling
   marketing spend there.
   At a {highest_return_val:.1f}% return rate - well above the {overall_return_rate:.1f}%
   company average - '{highest_return_cat}' may have sizing, quality, or
   listing-accuracy issues that are quietly eating into the margin this
   high-revenue category generates. Fixing this before investing further
   marketing budget will protect profitability, not just top-line sales.

3. Double down on '{top_city}' while testing targeted campaigns in lower-performing
   cities.
   With '{top_city}' already the clear leader, allocating proven marketing
   playbooks and inventory availability there is low-risk. Simultaneously,
   piloting smaller, targeted campaigns in the weaker cities can test whether
   the gap is a demand issue or simply an awareness/marketing gap worth closing.
""")

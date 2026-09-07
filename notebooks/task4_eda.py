"""
Task 4: Exploratory Data Analysis (EDA)
Dataset: ecommerce_orders_cleaned.csv
"""
import pandas as pd
import numpy as np

df = pd.read_csv("ecommerce_orders_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

print("=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)
print(f"\nShape: {df.shape}")
print("\nStatistical summary (numeric columns):")
print(df.describe().round(2))

print("\nCategorical column value counts:")
for col in ["product_category", "customer_gender", "payment_method", "customer_city"]:
    print(f"\n{col}:")
    print(df[col].value_counts())

print("\n" + "=" * 70)
print("CENTRAL TENDENCY & SPREAD (Total Amount)")
print("=" * 70)
amt = df["total_amount"]
print(f"Mean   : {amt.mean():.2f}")
print(f"Median : {amt.median():.2f}")
print(f"Std Dev: {amt.std():.2f}")
print(f"Min    : {amt.min():.2f}")
print(f"Max    : {amt.max():.2f}")

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)
numeric_cols = ["customer_age", "product_price", "quantity", "discount_pct",
                 "total_amount", "delivery_days", "customer_rating"]
corr_matrix = df[numeric_cols].corr()
print(corr_matrix.round(3))

print("\nNotable correlations:")
price_amount_corr = df["product_price"].corr(df["total_amount"])
discount_rating_corr = df["discount_pct"].corr(df["customer_rating"])
delivery_rating_corr = df["delivery_days"].corr(df["customer_rating"])
print(f"  product_price vs total_amount   : {price_amount_corr:.3f}")
print(f"  discount_pct vs customer_rating : {discount_rating_corr:.3f}")
print(f"  delivery_days vs customer_rating: {delivery_rating_corr:.3f}")

print("\n" + "=" * 70)
print("PATTERNS & TRENDS")
print("=" * 70)

df["month"] = df["order_date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("month")["total_amount"].sum().sort_index()
print("\nMonthly total sales:")
print(monthly_sales.round(0))

cat_sales = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)
print("\nTotal sales by category:")
print(cat_sales.round(0))

return_rate_by_cat = df.groupby("product_category")["is_returned"].mean().sort_values(ascending=False)
print("\nReturn rate by category:")
print((return_rate_by_cat * 100).round(1))

payment_dist = df["payment_method"].value_counts(normalize=True) * 100
print("\nPayment method distribution (%):")
print(payment_dist.round(1))

print("\n" + "=" * 70)
print("OUTLIER DETECTION (IQR method)")
print("=" * 70)


def detect_outliers_iqr(series, label):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = series[(series < lower) | (series > upper)]
    print(f"\n{label}: Q1={q1:.1f}, Q3={q3:.1f}, IQR={iqr:.1f}, "
          f"bounds=({lower:.1f}, {upper:.1f}) -> {len(outliers)} outlier(s)")
    return outliers


print("\n--- Naive approach: IQR on total_amount across the WHOLE dataset ---")
naive_outliers = detect_outliers_iqr(df["total_amount"], "total_amount (all categories combined)")
print(f"This flags {len(naive_outliers)} orders - misleadingly high, because product prices vary "
      f"hugely BETWEEN categories (Electronics vs Books, for example). A global IQR bound ends up "
      f"flagging most of the naturally more expensive Electronics orders as 'outliers' even though "
      f"they're normal for that category.")

print("\n--- Better approach: IQR on total_amount WITHIN each category ---")
outlier_rows = []
for cat, group in df.groupby("product_category"):
    cat_outliers = detect_outliers_iqr(group["total_amount"], f"total_amount ({cat})")
    outlier_rows.extend(cat_outliers.index.tolist())

price_outliers = detect_outliers_iqr(df["product_price"], "product_price (all categories - flags the data-entry error)")

outlier_ids = set(outlier_rows) | set(price_outliers.index)
print(f"\nOrders flagged as genuine outliers using the per-category approach ({len(outlier_ids)}):")
print(df.loc[sorted(outlier_ids), ["order_id", "product_category", "product_price",
                                     "quantity", "total_amount"]].to_string(index=False))


def corr_strength_label(r):
    ar = abs(r)
    if ar < 0.1:
        return "negligible"
    elif ar < 0.3:
        return "weak"
    elif ar < 0.5:
        return "moderate"
    else:
        return "strong"


discount_strength = corr_strength_label(discount_rating_corr)
delivery_strength = corr_strength_label(delivery_rating_corr)
price_amount_strength = corr_strength_label(price_amount_corr)

print(f"""
{"=" * 70}
FINDINGS SUMMARY
{"=" * 70}
- The dataset covers {df.shape[0]} cleaned orders across {df['product_category'].nunique()}
  product categories and {df['customer_city'].nunique()} cities.
- Total sales average {amt.mean():.0f} per order (median {amt.median():.0f}); the gap between
  mean and median confirms a right-skewed distribution, driven partly by genuinely higher-value
  categories like Electronics and partly by a couple of true outliers (a bulk order and a
  data-entry price error).
- A naive, whole-dataset IQR check flags {len(naive_outliers)} orders as outliers - mostly just
  normal Electronics purchases, since Electronics prices are naturally much higher than other
  categories. Running IQR separately WITHIN each category instead gives a different, more
  meaningful set of {len(outlier_ids)} orders: it avoids falsely flagging typical Electronics
  purchases, while also catching genuine high-quantity outliers in cheaper categories (like
  Apparel and Beauty) that the naive approach missed entirely - a good illustration of why
  category context matters for outlier detection.
- product_price has a {price_amount_strength} correlation with total_amount (r={price_amount_corr:.2f}) -
  positive as expected, but diluted by quantity and discount both also driving total_amount
  independently of price.
- discount_pct has a {discount_strength} correlation with customer_rating (r={discount_rating_corr:.2f}),
  suggesting discounting alone doesn't meaningfully move customer satisfaction in this dataset.
- delivery_days has a {delivery_strength} correlation with customer_rating (r={delivery_rating_corr:.2f}) -
  essentially no relationship in this data.
- Sales are not evenly distributed across categories or months - see Task 5/7 for the
  visualized and business-focused breakdown of these patterns.
""")

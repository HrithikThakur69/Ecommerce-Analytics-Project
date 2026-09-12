"""
Task 5: Data Visualization
Dataset: ecommerce_orders_cleaned.csv
Creates 6 visualizations (exceeds the required 5) covering sales trends,
category comparison, distribution, relationships, and returns.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("ecommerce_orders_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"

# ---------------- 1. Line Chart: Monthly Sales Trend ----------------
monthly = df.groupby("month")["total_amount"].sum().sort_index()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(monthly.index, monthly.values, marker="o", color="#2E8B57", linewidth=2)
ax.set_title("Monthly Total Sales Trend (2024)", fontsize=13, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales (INR)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("chart1_monthly_sales_trend.png", dpi=150)
plt.close()
print("Chart 1 (Line): Monthly Sales Trend saved.")

# ---------------- 2. Bar Chart: Total Sales by Category ----------------
cat_sales = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(cat_sales.index, cat_sales.values, color="#4682B4")
ax.set_title("Total Sales by Product Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Category")
ax.set_ylabel("Total Sales (INR)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("chart2_sales_by_category.png", dpi=150)
plt.close()
print("Chart 2 (Bar): Total Sales by Category saved.")

# ---------------- 3. Histogram: Order Value Distribution ----------------
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.hist(df["total_amount"], bins=25, color="#CD853F", edgecolor="black")
ax.set_title("Distribution of Order Values", fontsize=13, fontweight="bold")
ax.set_xlabel("Total Amount (INR)")
ax.set_ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("chart3_order_value_distribution.png", dpi=150)
plt.close()
print("Chart 3 (Histogram): Order Value Distribution saved.")

# ---------------- 4. Scatter Plot: Product Price vs Total Amount ----------------
fig, ax = plt.subplots(figsize=(7, 4.5))
categories = df["product_category"].unique()
palette = sns.color_palette("Set2", len(categories))
for cat, color in zip(categories, palette):
    subset = df[df["product_category"] == cat]
    ax.scatter(subset["product_price"], subset["total_amount"], label=cat,
               color=color, s=35, edgecolor="black", alpha=0.75)
ax.set_title("Product Price vs Order Total Amount", fontsize=13, fontweight="bold")
ax.set_xlabel("Product Price (INR)")
ax.set_ylabel("Total Amount (INR)")
ax.legend(title="Category", fontsize=8, title_fontsize=9)
plt.tight_layout()
plt.savefig("chart4_price_vs_total_scatter.png", dpi=150)
plt.close()
print("Chart 4 (Scatter): Product Price vs Total Amount saved.")

# ---------------- 5. Box Plot: Delivery Days by Category ----------------
fig, ax = plt.subplots(figsize=(7.5, 4.5))
sns.boxplot(data=df, x="product_category", y="delivery_days", hue="product_category",
            palette="Blues", legend=False, ax=ax)
ax.set_title("Delivery Time Distribution by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Category")
ax.set_ylabel("Delivery Days")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("chart5_delivery_days_boxplot.png", dpi=150)
plt.close()
print("Chart 5 (Box Plot): Delivery Time by Category saved.")

# ---------------- 6. Pie Chart: Payment Method Share ----------------
payment_counts = df["payment_method"].value_counts()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(payment_counts.values, labels=payment_counts.index, autopct="%1.1f%%",
       colors=sns.color_palette("Set3", len(payment_counts)), startangle=90)
ax.set_title("Orders by Payment Method", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("chart6_payment_method_pie.png", dpi=150)
plt.close()
print("Chart 6 (Pie): Orders by Payment Method saved.")
print("\nAll 6 visualizations saved.")





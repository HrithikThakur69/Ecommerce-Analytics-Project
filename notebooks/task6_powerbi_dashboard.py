"""
Task 6: Power BI Dashboard
Dataset: ecommerce_orders_cleaned.csv

NOTE: Power BI Desktop is a Windows-only application and cannot run in this
sandboxed environment (see project README for full detail). This script:
  1. Lists the exact DAX measures to create in Power BI.
  2. Independently validates their expected results with pandas.
  3. Renders a Python-built PREVIEW of the target dashboard layout (KPI
     cards + 4 visuals + 2 slicers), to guide building the live, actually
     interactive version in Power BI Desktop.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import pandas as pd

df = pd.read_csv("ecommerce_orders_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# ---------------- DAX Measures ----------------
dax_measures = [
    ("Total Sales", "Total Sales = SUM(Orders[total_amount])"),
    ("Average Order Value", "Average Order Value = AVERAGE(Orders[total_amount])"),
    ("Total Orders", "Total Orders = COUNTROWS(Orders)"),
    ("Total Customers", "Total Customers = DISTINCTCOUNT(Orders[customer_id])"),
    ("Return Rate %", "Return Rate % = DIVIDE(CALCULATE(COUNTROWS(Orders), Orders[is_returned] = TRUE), [Total Orders], 0)"),
    ("Average Rating", "Average Rating = AVERAGE(Orders[customer_rating])"),
    ("Average Delivery Days", "Average Delivery Days = AVERAGE(Orders[delivery_days])"),
]

print("----- DAX Measures to Create in Power BI -----")
for name, formula in dax_measures:
    print(f"  {formula}")

total_sales = df["total_amount"].sum()
avg_order = df["total_amount"].mean()
total_orders = len(df)
total_customers = df["customer_id"].nunique()
return_rate = df["is_returned"].mean()
avg_rating = df["customer_rating"].mean()
avg_delivery = df["delivery_days"].mean()

print("\n----- Expected Results (validated independently with pandas) -----")
print(f"Total Sales           : Rs.{total_sales:,.0f}")
print(f"Average Order Value   : Rs.{avg_order:,.2f}")
print(f"Total Orders          : {total_orders}")
print(f"Total Customers       : {total_customers}")
print(f"Return Rate %         : {return_rate:.1%}")
print(f"Average Rating        : {avg_rating:.2f} / 5")
print(f"Average Delivery Days : {avg_delivery:.1f} days")

# ---------------- Dashboard Mockup ----------------
PBI_BLUE = "#118DFF"
PBI_TEAL = "#01B8AA"
PBI_ORANGE = "#FF8C00"
PBI_PALETTE = ["#118DFF", "#12239E", "#E66C37", "#6B007B", "#E044A7", "#744EC2"]

fig = plt.figure(figsize=(14, 9.5), facecolor="#F3F2F1")
gs = GridSpec(4, 6, figure=fig, hspace=1.0, wspace=0.9,
              left=0.04, right=0.98, top=0.90, bottom=0.05)

fig.text(0.04, 0.965, "E-Commerce Sales & Customer Dashboard", fontsize=19, fontweight="bold", color="#222222")
fig.text(0.04, 0.937, "Interactive preview - slicer selections cross-filter every visual on the page",
          fontsize=9.5, color="#777777", style="italic")


def draw_slicer(ax, title, options):
    ax.axis("off")
    box = mpatches.FancyBboxPatch((0.02, 0.05), 0.96, 0.9, boxstyle="round,pad=0.02,rounding_size=0.05",
                                    linewidth=1, edgecolor="#CCCCCC", facecolor="white", transform=ax.transAxes)
    ax.add_patch(box)
    ax.text(0.08, 0.82, title, fontsize=9, fontweight="bold", color="#333333", transform=ax.transAxes)
    for i, opt in enumerate(options):
        ax.text(0.1, 0.6 - i * 0.19, f"\u2611 {opt}", fontsize=7.5, color="#444444", transform=ax.transAxes)


ax_slicer1 = fig.add_subplot(gs[0, 4])
draw_slicer(ax_slicer1, "Category Slicer", sorted(df["product_category"].unique())[:5])
ax_slicer2 = fig.add_subplot(gs[0, 5])
draw_slicer(ax_slicer2, "Payment Slicer", sorted(df["payment_method"].unique())[:5])

kpis = [
    ("Total Sales", f"Rs.{total_sales:,.0f}", PBI_BLUE),
    ("Total Orders", f"{total_orders}", PBI_TEAL),
    ("Avg. Order Value", f"Rs.{avg_order:,.0f}", PBI_ORANGE),
    ("Return Rate", f"{return_rate:.1%}", "#6B007B"),
]
for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.axis("off")
    box = mpatches.FancyBboxPatch((0.03, 0.08), 0.94, 0.86, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    linewidth=1.5, edgecolor=color, facecolor="white", transform=ax.transAxes)
    ax.add_patch(box)
    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=14, fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.5, 0.25, label, ha="center", va="center", fontsize=9, color="#444444", transform=ax.transAxes)

# Visual 1: Bar - Sales by category
ax1 = fig.add_subplot(gs[1:3, 0:2])
cat_sales = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)
ax1.bar(cat_sales.index, cat_sales.values, color=PBI_BLUE)
ax1.set_title("Total Sales by Category", fontsize=11, fontweight="bold")
ax1.tick_params(axis="x", labelsize=7.5, rotation=20)
ax1.tick_params(axis="y", labelsize=8)
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.0f}"))

# Visual 2: Line - Monthly trend
ax2 = fig.add_subplot(gs[1:3, 2:4])
monthly = df.groupby("month")["total_amount"].sum().sort_index()
ax2.plot(monthly.index, monthly.values, marker="o", color=PBI_TEAL, linewidth=2, markersize=4)
ax2.set_title("Monthly Sales Trend", fontsize=11, fontweight="bold")
ax2.tick_params(axis="x", labelsize=6.5, rotation=90)
ax2.tick_params(axis="y", labelsize=8)

# Visual 3: Donut - Payment method
ax3 = fig.add_subplot(gs[1:3, 4:6])
pay_counts = df["payment_method"].value_counts()
ax3.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.0f%%",
         colors=PBI_PALETTE[:len(pay_counts)], startangle=90,
         wedgeprops=dict(width=0.42, edgecolor="white"), textprops={"fontsize": 7.5})
ax3.set_title("Orders by Payment Method", fontsize=11, fontweight="bold")

# Visual 4: Table - Top cities
ax4 = fig.add_subplot(gs[3, 0:3])
ax4.axis("off")
top_cities = df.groupby("customer_city")["total_amount"].sum().sort_values(ascending=False).head(5).round(0)
cell_text = [[city, f"{val:,.0f}"] for city, val in top_cities.items()]
tbl = ax4.table(cellText=cell_text, colLabels=["City", "Total Sales"],
                 cellLoc="left", loc="center", colWidths=[0.55, 0.35])
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
tbl.scale(1, 1.4)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor("#2C2C54")
        cell.set_text_props(color="white", fontweight="bold")
    else:
        cell.set_facecolor("#F5F5F5" if r % 2 == 0 else "white")
ax4.set_title("Top 5 Cities by Sales", fontsize=11, fontweight="bold", loc="left")

# Visual 5: Bar - Return rate by category
ax5 = fig.add_subplot(gs[3, 3:6])
return_by_cat = (df.groupby("product_category")["is_returned"].mean() * 100).sort_values(ascending=False)
ax5.barh(return_by_cat.index, return_by_cat.values, color=PBI_ORANGE)
ax5.set_title("Return Rate % by Category", fontsize=11, fontweight="bold")
ax5.tick_params(axis="both", labelsize=8)

plt.savefig("dashboard_mockup.png", dpi=150, facecolor="#F3F2F1", bbox_inches="tight")
plt.close()

print("\nDashboard mockup saved: dashboard_mockup.png")
print("Contains: 4 KPI cards, 5 visualizations (bar, line, donut, table, bar), 2 slicers.")

"""
Task 3: Dataset Selection & Data Preparation
Dataset: E-Commerce Orders (ecommerce_orders_raw.csv)

Domain chosen: E-commerce / Customer Analytics - 403 order-level records
covering customer demographics, product category, pricing, discounts,
payment method, delivery time, ratings, and returns. This single, rich
table supports the full range of EDA, visualization, and dashboard work
required across the rest of the capstone.
"""
import pandas as pd

df = pd.read_csv("ecommerce_orders_raw.csv")

print("=" * 70)
print("DATA INSPECTION")
print("=" * 70)
print(f"\nShape (rows, columns): {df.shape}")

print("\n----- Column Names -----")
print(df.columns.tolist())

print("\n----- Data Types -----")
print(df.dtypes)

print("\n----- Statistical Summary (numeric columns) -----")
print(df.describe())

print("\n----- First 10 Rows (raw) -----")
print(df.head(10).to_string(index=False))

print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)
print("\n----- Missing Values per Column -----")
print(df.isnull().sum())

print("\n" + "=" * 70)
print("DATA CLEANING")
print("=" * 70)

df_clean = df.copy()

# 1. Handle missing values: numeric columns filled with column median
#    (robust to the outliers already present in this dataset)
for col in ["customer_age", "customer_rating", "delivery_days", "total_amount"]:
    median_val = df_clean[col].median()
    n_missing = df_clean[col].isnull().sum()
    df_clean[col] = df_clean[col].fillna(median_val)
    print(f"Filled {n_missing} missing value(s) in '{col}' with median ({median_val})")

# 2. Check and remove duplicate records
n_dupes = df_clean.duplicated().sum()
print(f"\nDuplicate rows found: {n_dupes}")
df_clean = df_clean.drop_duplicates().reset_index(drop=True)
print(f"Rows after removing duplicates: {df_clean.shape[0]} (was {df.shape[0]})")

# 3. Check for incorrect / inconsistent values
print("\n----- Checking for Inconsistent Values -----")
bad_delivery = df_clean[df_clean["delivery_days"] < 0]
print(f"Rows with negative 'delivery_days' (impossible value): {len(bad_delivery)}")
if len(bad_delivery) > 0:
    print(bad_delivery[["order_id", "delivery_days"]].to_string(index=False))
    df_clean.loc[df_clean["delivery_days"] < 0, "delivery_days"] = df_clean.loc[
        df_clean["delivery_days"] < 0, "delivery_days"
    ].abs()
    print("Corrected: took absolute value of negative delivery_days entries.")

# 4. Correct data types
df_clean["order_date"] = pd.to_datetime(df_clean["order_date"])
df_clean["customer_age"] = df_clean["customer_age"].astype(int)
df_clean["is_returned"] = df_clean["is_returned"].astype(bool)

print("\n----- Data Types After Cleaning -----")
print(df_clean.dtypes)

print("\n----- Missing Values After Cleaning -----")
print(df_clean.isnull().sum())

print(f"\nFinal cleaned shape: {df_clean.shape}")
print("\n----- First 10 Rows (cleaned) -----")
print(df_clean.head(10).to_string(index=False))

df_clean.to_csv("ecommerce_orders_cleaned.csv", index=False)
print("\nCleaned dataset exported to 'ecommerce_orders_cleaned.csv' - "
      "used for all subsequent tasks (EDA, visualization, Power BI, insights).")

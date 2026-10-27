from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Find the CSV beside this Python file.
project_folder = Path(__file__).parent
csv_file = project_folder / "data_analytics_practice.csv"
output_folder = project_folder / "analysis_results"
output_folder.mkdir(exist_ok=True)

# ---------- TASK 1: LOAD AND INSPECT ----------
raw = pd.read_csv(csv_file)

print("\nFIRST FIVE ROWS")
print(raw.head())

print("\nNUMBER OF ROWS AND COLUMNS")
print(raw.shape)

print("\nCOLUMN TYPES AND NON-MISSING COUNTS")
raw.info()

print("\nMISSING VALUES IN EACH COLUMN")
print(raw.isna().sum())

print("\nEXACT DUPLICATE ROWS")
print(raw.duplicated().sum())

print("\nCITY VALUES BEFORE CLEANING")
print(raw["City"].value_counts(dropna=False))

# Keep the original data unchanged and clean a copy.
data = raw.copy()

# Standardize text by removing extra spaces and fixing capitalization.
for column in ["City", "Product", "Category"]:
    data[column] = (
        data[column]
        .astype("string")
        .str.strip()
        .str.title()
    )

# Mark missing cities clearly rather than guessing a city.
data["City"] = data["City"].fillna("Unknown")

# Correct the written-out quantity, then convert quantities to numbers.
data["Quantity"] = (
    data["Quantity"]
    .astype("string")
    .str.strip()
    .str.lower()
    .replace({"five": "5"})
)
data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")

# Convert age to a number. Fill missing ages with the median age.
data["Age"] = pd.to_numeric(data["Age"], errors="coerce")
data["Age"] = data["Age"].fillna(data["Age"].median()).round().astype(int)

# Fill a missing quantity with the median quantity.
data["Quantity"] = (
    data["Quantity"]
    .fillna(data["Quantity"].median())
    .round()
    .astype(int)
)

# Remove the rupee symbol and thousands comma before converting price.
data["UnitPrice"] = (
    data["UnitPrice"]
    .astype("string")
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)
data["UnitPrice"] = pd.to_numeric(data["UnitPrice"], errors="coerce")

# Convert dates to real dates. Invalid dates become missing values.
data["OrderDate"] = pd.to_datetime(
    data["OrderDate"],
    format="mixed",
    errors="coerce"
)

# OrderID should be unique, so keep one row per order ID.
data = data.drop_duplicates(subset=["OrderID"], keep="first")

# Create useful columns for analysis.
data["Sales"] = data["Quantity"] * data["UnitPrice"]
data["Month"] = data["OrderDate"].dt.to_period("M").astype(str)

# Save a new cleaned file. The original CSV is left untouched.
cleaned_file = output_folder / "sales_cleaned.csv"
data.to_csv(cleaned_file, index=False)

print("\nCLEANED DATA SAVED TO:")
print(cleaned_file)

print("\nMISSING VALUES AFTER CLEANING")
print(data.isna().sum())

print("\nCLEANED DATA TYPES")
print(data.dtypes)

# ---------- TASK 2: EXPLORATORY DATA ANALYSIS ----------
print("\nNUMERIC SUMMARY")
print(data[["Age", "Quantity", "UnitPrice", "Sales"]].describe())

print("\nTOTAL SALES BY PRODUCT")
product_sales = data.groupby("Product")["Sales"].sum().sort_values(ascending=False)
print(product_sales)

print("\nTOTAL SALES BY CITY")
city_sales = data.groupby("City")["Sales"].sum().sort_values(ascending=False)
print(city_sales)

print("\nTOTAL SALES BY MONTH")
monthly_sales = data.groupby("Month")["Sales"].sum().sort_index()
print(monthly_sales)

print("\nSALES BY PAYMENT METHOD")
print(data.groupby("PaymentMethod")["Sales"].sum().sort_values(ascending=False))

# Find possible outliers using the IQR rule.
q1 = data["Sales"].quantile(0.25)
q3 = data["Sales"].quantile(0.75)
iqr = q3 - q1
low_limit = q1 - 1.5 * iqr
high_limit = q3 + 1.5 * iqr

possible_outliers = data[
    (data["Sales"] < low_limit) | (data["Sales"] > high_limit)
]

print("\nPOSSIBLE SALES OUTLIERS TO REVIEW")
print(possible_outliers[["OrderID", "Product", "Sales"]])

print("\nBUSINESS QUESTION: WHICH PRODUCT HAS THE MOST SALES?")
print(product_sales.idxmax(), "with total sales of", product_sales.max())

print("\nBUSINESS QUESTION: WHICH CITY HAS THE MOST SALES?")
print(city_sales.idxmax(), "with total sales of", city_sales.max())
# ---------- TASK 3: CHARTS ----------
sns.set_theme(style="whitegrid")

# Bar chart: compare total sales by product.
plt.figure(figsize=(9, 5))
product_sales.sort_values().plot(kind="barh", color="steelblue")
plt.title("Total Sales by Product")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(output_folder / "sales_by_product.png")
plt.close()

# Line chart: show how sales change month to month.
plt.figure(figsize=(9, 5))
monthly_sales.plot(marker="o", color="darkorange")
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "monthly_sales.png")
plt.close()

# Pie chart: show each category's share of sales.
category_sales = data.groupby("Category")["Sales"].sum()
plt.figure(figsize=(7, 7))
category_sales.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Share of Sales by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig(output_folder / "sales_by_category.png")
plt.close()

# Histogram: show the spread of customer ages.
plt.figure(figsize=(8, 5))
sns.histplot(data["Age"], bins=8, color="seagreen")
plt.title("Distribution of Customer Ages")
plt.xlabel("Age")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(output_folder / "customer_ages.png")
plt.close()

# Scatter plot: compare quantity with the order's sales amount.
plt.figure(figsize=(8, 5))
sns.scatterplot(data=data, x="Quantity", y="Sales", hue="Category")
plt.title("Quantity and Sales")
plt.xlabel("Quantity Ordered")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(output_folder / "quantity_vs_sales.png")
plt.close()

print("\nCharts saved in:")
print(output_folder)
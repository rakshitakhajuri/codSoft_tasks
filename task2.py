from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent
cleaned_file = project_folder / "analysis_results" / "sales_cleaned.csv"
data = pd.read_csv(cleaned_file)

required_columns = [
    "Age", "Quantity", "UnitPrice", "Sales", "Product",
    "City", "Month", "PaymentMethod", "OrderID"
]
missing_columns = [column for column in required_columns if column not in data.columns]

if missing_columns:
    raise ValueError(f"Cleaned CSV is missing required columns: {missing_columns}")

print("\nNUMERIC SUMMARY")
print(data[["Age", "Quantity", "UnitPrice", "Sales"]].describe())

product_sales = data.groupby("Product")["Sales"].sum().sort_values(ascending=False)
city_sales = data.groupby("City")["Sales"].sum().sort_values(ascending=False)
monthly_sales = data.groupby("Month")["Sales"].sum().sort_index()
payment_sales = data.groupby("PaymentMethod")["Sales"].sum().sort_values(ascending=False)

print("\nTOTAL SALES BY PRODUCT")
print(product_sales)

print("\nTOTAL SALES BY CITY")
print(city_sales)

print("\nTOTAL SALES BY MONTH")
print(monthly_sales)

print("\nSALES BY PAYMENT METHOD")
print(payment_sales)

# Find possible outliers using the IQR rule.
q1 = data["Sales"].quantile(0.25)
q3 = data["Sales"].quantile(0.75)
iqr = q3 - q1

low_limit = q1 - 1.5 * iqr
high_limit = q3 + 1.5 * iqr

possible_outliers = data.loc[
    (data["Sales"] < low_limit) | (data["Sales"] > high_limit),
    ["OrderID", "Product", "Sales"]
]

print("\nPOSSIBLE SALES OUTLIERS TO REVIEW")
if possible_outliers.empty:
    print("No possible outliers found.")
else:
    print(possible_outliers)

if not product_sales.empty:
    print("\nPRODUCT WITH MOST SALES")
    print(product_sales.idxmax(), "with total sales of", product_sales.max())

if not city_sales.empty:
    print("\nCITY WITH MOST SALES")
    print(city_sales.idxmax(), "with total sales of", city_sales.max())
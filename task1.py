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
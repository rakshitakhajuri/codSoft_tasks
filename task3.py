from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

project_folder = Path(__file__).resolve().parent
output_folder = project_folder / "analysis_results"
cleaned_file = output_folder / "sales_cleaned.csv"

data = pd.read_csv(cleaned_file)

sns.set_theme(style="whitegrid")

product_sales = data.groupby("Product")["Sales"].sum().sort_values()
monthly_sales = data.groupby("Month")["Sales"].sum().sort_index()
category_sales = data.groupby("Category")["Sales"].sum()

# Bar chart: total sales by product.
plt.figure(figsize=(9, 5))
product_sales.plot(kind="barh", color="steelblue")
plt.title("Total Sales by Product")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(output_folder / "sales_by_product.png")
plt.close()

# Line chart: sales by month.
plt.figure(figsize=(9, 5))
monthly_sales.plot(marker="o", color="darkorange")
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "monthly_sales.png")
plt.close()

# Pie chart: share of sales by category.
if not category_sales.empty:
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

# Histogram: customer age distribution.
plt.figure(figsize=(8, 5))
sns.histplot(data["Age"].dropna(), bins=8, color="seagreen")
plt.title("Distribution of Customer Ages")
plt.xlabel("Age")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(output_folder / "customer_ages.png")
plt.close()

# Scatter plot: quantity compared with sales.
plt.figure(figsize=(8, 5))
sns.scatterplot(data=data, x="Quantity", y="Sales", hue="Category")
plt.title("Quantity and Sales")
plt.xlabel("Quantity Ordered")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(output_folder / "quantity_vs_sales.png")
plt.close()

print("Charts saved in:")
print(output_folder)
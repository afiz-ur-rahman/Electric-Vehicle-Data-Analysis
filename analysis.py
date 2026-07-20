from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
base_dir = Path(__file__).resolve().parent
excel_path = base_dir / "jewellery_sales_6months.xlsx"
if not excel_path.exists():
    raise FileNotFoundError(f"Could not find Excel file: {excel_path}")
# Load Excel file
df = pd.read_excel(excel_path)
# Normalize data types for analysis and plotting
for col in ["Sales_Amount", "Units_Sold", "Stock_Level"]:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(r"[^0-9.\-]", "", regex=True),
        errors="coerce",
    )
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Month"] = df["Date"].dt.to_period("M").astype(str)
# --- 1. Total Sales by Product Category ---
category_sales = df.groupby("Product_Category")["Sales_Amount"].sum().reset_index()
plt.figure(figsize=(8,5))
sns.barplot(data=category_sales, x="Sales_Amount", y="Product_Category", palette="viridis", hue="Product_Category", dodge=False, legend=False)
plt.title("Total Sales by Product Category (6 Months)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(base_dir / "category_sales.png")
plt.close()
# --- 2. Monthly Sales Trend ---
monthly_sales = df.groupby("Month")["Sales_Amount"].sum().reset_index()
plt.figure(figsize=(10,5))
sns.lineplot(data=monthly_sales, x="Month", y="Sales_Amount", marker="o")
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(base_dir / "monthly_sales.png")
plt.close()
# --- 3. Top 10 Best-Selling Products ---
product_sales = df.groupby("Product_Name")["Sales_Amount"].sum().reset_index()
top_products = product_sales.sort_values(by="Sales_Amount", ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(data=top_products, x="Sales_Amount", y="Product_Name", palette="magma", hue="Product_Name", dodge=False, legend=False)
plt.title("Top 10 Best-Selling Products")
plt.tight_layout()
plt.savefig(base_dir / "top_products.png")
plt.close()
# --- 4. Stock vs Sales (Inventory Risk) ---
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="Stock_Level", y="Units_Sold", hue="Product_Category", alpha=0.7)
plt.title("Stock Level vs Units Sold")
plt.tight_layout()
plt.savefig(base_dir / "stock_vs_sales.png")
plt.close()
print("Analysis complete. Charts saved as PNG files.")
#result
#PS C:\Users\USER\OneDrive\Desktop\sales and inventory analyst> python analysis.py
#Analysis complete. Charts saved as PNG files.
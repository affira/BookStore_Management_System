import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv("data/raw_sales_data.csv")

# 1️⃣ Display initial overview
print("Before Cleaning:\n", df.head())
print("\nData Info:\n", df.info())

# 2️⃣ Remove duplicate rows
# Identify duplicates before removal
print("\nChecking for Duplicates Before Removal:")
print(df[df.duplicated(subset=["BookID", "CustomerID", "Quantity", "Date"], keep=False)])
# Drop duplicates based on selected columns
df = df.drop_duplicates(subset=["BookID", "CustomerID", "Quantity", "Date"])
# Verify duplicates after removal
print("\nDuplicates after removal:", df.duplicated().sum())

# 3️⃣ Handle missing values
df = df.assign(
    Price=df["Price"].fillna(df["Price"].mean()),
    Quantity=df["Quantity"].fillna(1)
)

# 4️⃣ Add a new column: "High Value Purchase" (True if price > 40, else False)
df["High_Value_Purchase"] = df["Price"] > 40

# 5️⃣ Save cleaned data
df.to_csv("data/cleaned_sales_data.csv", index=False)

print("\nData Cleaning Completed! Cleaned file saved.")
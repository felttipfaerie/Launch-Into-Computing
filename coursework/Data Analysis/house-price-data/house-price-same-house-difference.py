import os
import pandas as pd
import matplotlib.pyplot as plt

data_folder = r"C:\Users\elmak\Documents\Launch Into Computing\coursework\house-price-data"

# find csv files
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

print("Files found:", csv_files)

dataframes = []

for file in csv_files:
    path = os.path.join(data_folder, file)
    temp_df = pd.read_csv(path, header=None)
    dataframes.append(temp_df)

# combine all years
df = pd.concat(dataframes, ignore_index=True)

print("Total rows:", len(df))
print("Total columns:", df.shape[1])


# column names
df.columns = [
    "transaction_id",
    "price",
    "date",
    "postcode",
    "property_type",
    "new_build",
    "tenure",
    "paon",
    "saon",
    "street",
    "locality",
    "town",
    "district",
    "county",
    "ppd_category",
    "record_status"
]

# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["paon"] = df["paon"].astype(str).str.strip().str.upper()
df["saon"] = df["saon"].astype(str).str.strip().str.upper()
df["street"] = df["street"].astype(str).str.strip().str.upper()
df["postcode"] = df["postcode"].astype(str).str.strip().str.upper()

df["paon"] = df["paon"].replace(["NAN", "NONE"], "")
df["saon"] = df["saon"].replace(["NAN", "NONE"], "")
df["street"] = df["street"].replace(["NAN", "NONE"], "")
df["postcode"] = df["postcode"].replace(["NAN", "NONE"], "")

df = df[
    (df["paon"] != "") &
    (df["street"] != "") &
    (df["postcode"] != "") &
    (df["date"].notna())
].copy()

# --------------------------------------------------
# CREATE PROPERTY ID
# --------------------------------------------------

df["property_id"] = (
    df["paon"] + " | " +
    df["saon"] + " | " +
    df["street"] + " | " +
    df["postcode"]
)

# --------------------------------------------------
# FIND HOUSES SOLD MORE THAN ONCE
# --------------------------------------------------

sale_counts = df.groupby("property_id").size().reset_index(name="times_sold")
repeat_ids = sale_counts[sale_counts["times_sold"] > 1]["property_id"]

repeat_sales = df[df["property_id"].isin(repeat_ids)].copy()

# --------------------------------------------------
# GET FIRST AND LAST SALE FOR EACH PROPERTY
# --------------------------------------------------

repeat_sales = repeat_sales.sort_values(["property_id", "date"])

first_sales = repeat_sales.groupby("property_id").first().reset_index()
last_sales = repeat_sales.groupby("property_id").last().reset_index()

price_comparison = pd.DataFrame({
    "property_id": first_sales["property_id"],
    "first_price": first_sales["price"],
    "last_price": last_sales["price"],
    "first_date": first_sales["date"],
    "last_date": last_sales["date"]
})

# optional: remove cases where first and last transaction happened on the same date
price_comparison = price_comparison[
    price_comparison["first_date"] < price_comparison["last_date"]
].copy()

# optional: sort by price change
price_comparison["price_change"] = (
    price_comparison["last_price"] - price_comparison["first_price"]
)

price_comparison = price_comparison.sort_values("price_change", ascending=False)

print("\nProperties sold more than once:")
print(price_comparison.head(10))

# --------------------------------------------------
# CHART
# --------------------------------------------------
# IMPORTANT:
# Plotting every repeated property may be too crowded.
# This plots the first 50 properties after sorting.

plot_data = price_comparison.head(50).copy()

x = range(len(plot_data))

plt.figure(figsize=(14, 7))
plt.plot(x, plot_data["first_price"], marker="o", label="First price")
plt.plot(x, plot_data["last_price"], marker="o", label="Last price")

plt.title("First and Last Sale Price for Properties Sold More Than Once")
plt.xlabel("Property")
plt.ylabel("Price")
plt.legend()

# hide long property labels to keep the chart readable
plt.xticks(x, [""] * len(plot_data))

plt.tight_layout()
plt.show()
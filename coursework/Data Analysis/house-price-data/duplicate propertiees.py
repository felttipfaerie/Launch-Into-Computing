import os
import pandas as pd

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
# CLEAN ADDRESS DATA
# --------------------------------------------------

# make sure address columns are treated as text
df["paon"] = df["paon"].astype(str)
df["saon"] = df["saon"].astype(str)
df["street"] = df["street"].astype(str)
df["postcode"] = df["postcode"].astype(str)

# remove extra spaces and standardise capital letters
df["paon"] = df["paon"].str.strip().str.upper()
df["saon"] = df["saon"].str.strip().str.upper()
df["street"] = df["street"].str.strip().str.upper()
df["postcode"] = df["postcode"].str.strip().str.upper()

# replace missing-style text values with empty strings
df["paon"] = df["paon"].replace(["NAN", "NONE"], "")
df["saon"] = df["saon"].replace(["NAN", "NONE"], "")
df["street"] = df["street"].replace(["NAN", "NONE"], "")
df["postcode"] = df["postcode"].replace(["NAN", "NONE"], "")

# remove rows where the key address information is missing
df = df[
    (df["paon"] != "") &
    (df["street"] != "") &
    (df["postcode"] != "")
]

print("\nRows after cleaning:", len(df))

# convert date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# remove transactions for the same property on the same day
df = df.drop_duplicates(
    subset=["paon", "saon", "street", "postcode", "date"]
)

print("\nRows after removing same-day duplicate transactions:", len(df))


# --------------------------------------------------
# FIND HOUSES SOLD MULTIPLE TIMES
# --------------------------------------------------

# group by house identity and count how many times each house was sold
house_sale_counts = (
    df.groupby(["paon", "saon", "street", "postcode"])
      .size()
      .reset_index(name="times_sold")
)

# keep only houses sold more than once
duplicate_houses = house_sale_counts[house_sale_counts["times_sold"] > 1]

print("\nHouses sold more than once:")
print(duplicate_houses.head())

# --------------------------------------------------
# COUNT HOW MANY HOUSES WERE SOLD 2, 3, 4, ... N TIMES
# --------------------------------------------------

sales_frequency = (
    duplicate_houses["times_sold"]
    .value_counts()
    .sort_index()
)

print("\nNumber of houses sold exactly 2, 3, 4, ... times:")
print(sales_frequency)


import pandas as pd
import os

folder = r"C:\Users\elmak\Documents\Launch Into Computing\coursework\UK census data 2021"

files = [f for f in os.listdir(folder) if f.endswith(".csv") and "combined" not in f]

dataframes = []

total_rows_before = 0
total_rows_after = 0

for file in files:
    path = os.path.join(folder, file)
    df = pd.read_csv(path)

    rows_before = len(df)

    # remove duplicates
    df = df.drop_duplicates(
        subset=[
            "geography",
            "geography code",
            "Highest level of qualification: Total: All usual residents aged 16 years and over"
        ]
    )

    rows_after = len(df)

    total_rows_before += rows_before
    total_rows_after += rows_after

    print(f"{file}")
    print(f"Rows before cleaning: {rows_before}")
    print(f"Rows after cleaning : {rows_after}")
    print(f"Duplicates removed  : {rows_before - rows_after}\n")

    df["source_file"] = file
    dataframes.append(df)

# combine datasets
combined = pd.concat(dataframes, ignore_index=True)

print("\n----------------------------------")
print("DATASET SUMMARY")
print("----------------------------------")

print("Total rows before cleaning:", total_rows_before)
print("Total rows after cleaning :", total_rows_after)
print("Total duplicates removed  :", total_rows_before - total_rows_after)

print("\nFinal combined dataset:")
print("Rows:", combined.shape[0])
print("Columns:", combined.shape[1])

print("\nFirst 5 rows:")
print(combined.head())

print("\nNull values:")
print(combined.isnull().sum())

# export dataset
output = os.path.join(folder, "combined_census_data_clean.csv")
combined.to_csv(output, index=False)

print("\nCombined dataset saved to:", output)
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

file_path = Path(__file__).parent / "combined_census_data_clean.csv"

df = pd.read_csv(file_path)

# --------------------------------------------------
# SHOW ALL COLUMNS
# --------------------------------------------------

print("\nColumns in dataset:")
print(df.columns.tolist())


# --------------------------------------------------
# SHOW UNIQUE CLASSES IN EACH COLUMN
# --------------------------------------------------

for col in df.columns:
    print("\n----------------------------------")
    print(f"Column: {col}")

    # show unique values
    unique_values = df[col].unique()
    print(f"\nUnique values ({len(unique_values)}):")
    print(unique_values)

    # show counts of each class
    print("\nValue counts:")
    print(df[col].value_counts())
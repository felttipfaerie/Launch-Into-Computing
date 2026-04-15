
# --------------------------------------------------
# added to allow for data import
# --------------------------------------------------

import pandas as pd
import os
import pathlib
from pathlib import Path
import matplotlib.pyplot as plt

# --------------------------------------------------
# mostly original code for cleaning names
# --------------------------------------------------

def process_names(names):
    unique_names = set()  # using a set to store unique names
    for name in names:
        unique_names.add(name.title())  # convert to title case and add to set
    unique_names = list(unique_names)  # convert set back to list
    unique_names.sort()  # sorts alphabetically
    return unique_names

# --------------------------------------------------
# added to allow for data validation
# --------------------------------------------------

def validate_names(names):
    invalid_names = []
    
    for name in names:
        # Skip NaN (already handled, but safe check)
        if pd.isna(name):
            continue
        
        name_str = str(name).strip()
        
        # Check 1: Empty string
        if name_str == "":
            invalid_names.append(name)
            continue
        
        # Check 2: Contains non-alphabetic characters
        if not name_str.replace("-", "").replace("'", "").isalpha():
            invalid_names.append(name)
            continue
        
        # Check 3: Length check (optional but useful)
        if len(name_str) < 2 or len(name_str) > 30:
            invalid_names.append(name)
    
    return invalid_names

# --------------------------------------------------
# Get external data for testing
# Changed to allow different data sources
# --------------------------------------------------

file_path = Path(__file__).parent / "people-100000.csv"

df = pd.read_csv(
    file_path,
    na_values="?",
    skipinitialspace=True
)

print("Initial shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum())

# --------------------------------------------------
# Choose which column to analyse
# --------------------------------------------------

name_column = "Sex" 

# --------------------------------------------------
# Get unique names from the DataFrame (MAIN LOGIC)
# --------------------------------------------------

series = df[name_column].dropna()

# Error checking (moved here)
missing_count = df[name_column].isna().sum()
print("\nMissing {}:".format(name_column), missing_count)

invalid_names = validate_names(series)
print("Invalid values found:", len(invalid_names))
print("Examples of invalid values:", invalid_names[:10])

# Remove invalid values BEFORE unique
valid_series = [name for name in series if name not in invalid_names]

# Unique BEFORE processing
unique_names = pd.Series(valid_series).unique()
print("\nUnique values before processing:", len(unique_names))

# Clean + deduplicate
cleaned_names = process_names(unique_names)

print("\nTotal values (before unique):", len(series)) #show number of invalid entries
print("Valid values:", len(valid_series)) #show number of valid entries
print("Cleaned unique values:", len(cleaned_names)) #display count only

print("\nProcessed list:", cleaned_names)
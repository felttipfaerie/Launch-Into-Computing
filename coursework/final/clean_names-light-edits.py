# clean_names-light-edits.py

import re

# function to remove invalid characters and check for valid names
def is_valid_name(name):
    return bool(re.fullmatch(r"(?=.*[^\W\d_])[\w\u0300-\u036f\s'’-]+", name, re.UNICODE)) and not any(
        ch.isdigit() or ch == "_" for ch in name
    )

def get_invalid_names(names):
    return [n for n in names if not is_valid_name(n)] # returns a list of invalid names for reporting purposes

def print_invalid_names(names):
    invalid = get_invalid_names(names)
    print(f"Invalid names ({len(invalid)}): {', '.join(invalid)}")

def process_names(names):
    valid_names = [name.lower() for name in names if is_valid_name(name)] # removes invalid names and converts to lowercase
    unique_names = sorted(set(valid_names))
    return unique_names

# Test list with duplicates and inconsistent capitalisation
test_names = ["Alice", "bob", "Eleanor-Rose", "McDonald", "O'Conner", "François", "Дмитро́", "محمد", "##:)", "Big D", "!@#", "1234", "alice", "Charlie", "BOB", "dave", "Eve", "charlie"]

print("Original list:", test_names)
print("Processed list:", process_names(test_names))
print_invalid_names(test_names) #prints invalid names to check which ones were removed
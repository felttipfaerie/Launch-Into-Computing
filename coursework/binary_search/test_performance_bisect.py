"""
Performance test for bisect-based binary search implementation.

This script will:
- Load the user's binary-search module (handles hyphenated filename)
- Detect the search function (`binary_search` or `binarySearch`)
- Measure time to find targets for various array sizes
- Append results to `bisect_test_results.txt` in the same folder
"""

import time
import csv
from datetime import datetime
import pathlib
import importlib.util
import sys

HERE = pathlib.Path(__file__).parent

# Find possible module filenames
candidates = ["binary_search_bisect.py", "binary-search.py", "binary_search.py", "binarysearch.py"]
module_path = None
for name in candidates:
    p = HERE / name
    if p.exists():
        module_path = p
        break

if module_path is None:
    # Fallback: try any file that starts with 'binary' in the directory
    for p in HERE.glob("binary*.py"):
        module_path = p
        break

if module_path is None:
    raise SystemExit("Could not find binary search module file in the scripts folder.")

# Load module from file
spec = importlib.util.spec_from_file_location("bisect_binary_module", str(module_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Find a usable function
if hasattr(module, "binary_search_bisect"):
    search_fn = module.binary_search_bisect
elif hasattr(module, "binary_search"):
    search_fn = module.binary_search
elif hasattr(module, "binarySearch"):
    search_fn = module.binarySearch
else:
    raise SystemExit("No suitable binary search function found in module.")


def run_performance_tests():
    results = []

    # Test cases: (array_size, target_index_to_search)
    test_cases = [
        (100, 50),
        (1000, 500),
        (10000, 5000),
        (100000, 50000),
        (1000000, 500000),
    ]

    print("Running Bisect-based Binary Search Performance Tests...")
    print("-" * 60)

    # Prepare CSV summary file
    summary = HERE / "performance_summary.csv"
    if not summary.exists():
        with summary.open("w", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)
            writer.writerow(["timestamp","module","function","array_size","target","index","time_us"]) 

    for array_size, target_value in test_cases:
        arr = list(range(1, array_size + 1))

        start = time.perf_counter()
        result = search_fn(arr, target_value)
        end = time.perf_counter()

        elapsed_us = (end - start) * 1_000_000

        line = (
            f"Array Size: {array_size:>10} | Target: {target_value:>10} | "
            f"Found at Index: {result:>10} | Time: {elapsed_us:>10.4f} µs"
        )
        print(line)
        results.append(line)

    print("-" * 60)

    # Append results to CSV summary only
    with summary.open("a", newline="", encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        for i, (array_size, target_value) in enumerate(test_cases):
            line = results[i]
            parts = line.split("|")
            array_size_str = parts[0].split(":")[1].strip()
            target_str = parts[1].split(":")[1].strip()
            index_str = parts[2].split(":")[1].strip()
            time_str = parts[3].split(":")[1].strip().split()[0]
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), module_path.name, search_fn.__name__, array_size_str, target_str, index_str, time_str])

    print(f"\nResults appended to performance_summary.csv")


if __name__ == "__main__":
    run_performance_tests()

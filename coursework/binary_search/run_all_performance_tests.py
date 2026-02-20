"""
Combined performance runner for available search implementations in this folder.

- Detects modules: files starting with 'binary' or 'linear'
- Finds search function(s) inside each module (`binary_search`, `binarySearch`, `linearSearch`)
- Runs performance tests (same test cases used previously)
- Appends per-module results to their existing log files (if any)
- Appends rows to `performance_summary.csv` with columns:
    timestamp,module_name,function_name,array_size,target,index,time_us

Run with:
    python run_all_performance_tests.py
"""

import time
import csv
from datetime import datetime
import pathlib
import importlib.util

HERE = pathlib.Path(__file__).parent
TEST_CASES = [
    (100, 50),
    (1000, 500),
    (10000, 5000),
    (100000, 50000),
    (1000000, 500000),
]

# Helper: import module from path
def load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Discover candidate files
modules = []
for p in HERE.glob("binary*.py"):
    modules.append(p)
for p in HERE.glob("linear*.py"):
    modules.append(p)

if not modules:
    raise SystemExit("No binary*/linear* modules found in scripts folder.")

summary_file = HERE / "performance_summary.csv"
# Ensure CSV header exists
if not summary_file.exists():
    with summary_file.open("w", newline="", encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["timestamp","module","function","array_size","target","index","time_us"]) 

all_results = []

for mod_path in modules:
    try:
        mod = load_module(mod_path, mod_path.stem)
    except Exception as e:
        print(f"Skipping {mod_path.name}: failed to import ({e})")
        continue

    # Find candidate function names
    fn = None
    candidate_names = [
        "binary_search_bisect",
        "binary_search_iterative",
        "binary_search",
        "binarySearch",
        "linearSearch",
        "linear_search",
    ]
    for name in candidate_names:
        if hasattr(mod, name):
            fn = getattr(mod, name)
            fn_name = name
            break

    if fn is None:
        print(f"No known search function found in {mod_path.name}, skipping.")
        continue

    print(f"Running tests for {mod_path.name} -> function {fn_name}")

    # Prepare per-module log file name
    module_log = HERE / (mod_path.stem + "_results.txt")

    per_module_lines = []
    for array_size, target_value in TEST_CASES:
        arr = list(range(1, array_size + 1))
        start = time.perf_counter()
        try:
            idx = fn(arr, target_value)
        except Exception as e:
            idx = f"error:{e}"
        end = time.perf_counter()
        elapsed_us = (end - start) * 1_000_000

        line = (
            f"Array Size: {array_size:>10} | Target: {target_value:>10} | "
            f"Found at Index: {str(idx):>10} | Time: {elapsed_us:>10.4f} µs"
        )
        print(line)
        per_module_lines.append(line)

        # Add to summary rows
        all_results.append({
            "timestamp": datetime.now().isoformat(sep=' '),
            "module": mod_path.name,
            "function": fn_name,
            "array_size": array_size,
            "target": target_value,
            "index": idx,
            "time_us": f"{elapsed_us:.4f}",
        })

    # Per-module text logs removed — results are stored only in CSV summary

# Append summary CSV rows
with summary_file.open("a", newline="", encoding="utf-8") as csvf:
    writer = csv.writer(csvf)
    for row in all_results:
        writer.writerow([row["timestamp"], row["module"], row["function"], row["array_size"], row["target"], row["index"], row["time_us"]])

print(f"\nSummary appended to {summary_file.name}")

if __name__ == "__main__":
    pass

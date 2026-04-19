import pandas as pd
import os
import json
import re

folder = r"C:\Users\elmak\Documents\Launch Into Computing\coursework\marriages-births-deaths"

files = [
    f for f in os.listdir(folder)
    if f.lower().endswith((".xls", ".xlsx")) and not f.lower().endswith(".json")
]


def clean_column_name(col):
    """Clean ugly column names."""
    if pd.isna(col):
        return None

    col = str(col).strip()

    if not col:
        return None

    # remove [note 1], [note 2], etc.
    col = re.sub(r"\[.*?\]", "", col)

    # remove worksheet/table prefixes
    col = re.sub(r"^(worksheet|table)\s*[0-9a-z]+:?\s*", "", col, flags=re.IGNORECASE)

    # remove repeated whitespace
    col = re.sub(r"\s+", " ", col).strip()

    # remove obvious junk
    junk_values = {
        "",
        "notes",
        "contents",
        "commentary",
        "unnamed",
        "nan"
    }

    if col.lower() in junk_values:
        return None

    if col.lower().startswith("unnamed:"):
        return None

    return col


def looks_like_bad_header(row_values):
    """Reject rows that are probably titles, notes, or contents."""
    text = " ".join([str(v).strip() for v in row_values if pd.notna(v)]).lower()

    if not text.strip():
        return True

    bad_patterns = [
        "worksheet",
        "table ",
        "contents",
        "notes",
        "commentary for worksheets",
        "marriages in england and wales",
        "correction notice",
    ]

    return any(p in text for p in bad_patterns)


def find_best_header_row(df_raw, max_rows=15):
    """
    Look through the first few rows and choose the first row
    that looks like a real header.
    """
    rows_to_check = min(max_rows, len(df_raw))

    for i in range(rows_to_check):
        row = df_raw.iloc[i].tolist()

        if looks_like_bad_header(row):
            continue

        cleaned = [clean_column_name(x) for x in row]
        cleaned = [x for x in cleaned if x is not None]

        # good header should have at least 2 usable columns
        if len(cleaned) >= 2:
            return i

    return None


def make_unique_columns(columns):
    """Ensure duplicate column names become unique."""
    seen = {}
    unique = []

    for col in columns:
        if col is None:
            col = "unknown"

        if col not in seen:
            seen[col] = 0
            unique.append(col)
        else:
            seen[col] += 1
            unique.append(f"{col}_{seen[col]}")

    return unique


print("Workbooks found:")
for f in files:
    print("-", f)

for file in files:
    path = os.path.join(folder, file)
    print("\nProcessing:", file)

    try:
        workbook = pd.ExcelFile(path)
    except Exception as e:
        print("Could not open workbook:", e)
        continue

    document = {
        "file_name": file,
        "year": None,
        "source_type": "marriages",
        "sheets": []
    }

    match = re.search(r"\d{4}", file)
    if match:
        document["year"] = int(match.group())

    for sheet in workbook.sheet_names:
        try:
            # read sheet with no assumed header
            df_raw = pd.read_excel(workbook, sheet_name=sheet, header=None)

            # remove fully empty rows/cols
            df_raw = df_raw.dropna(how="all").dropna(axis=1, how="all")

            if df_raw.empty:
                continue

            # skip obvious non-data sheets by sheet name
            if any(x in str(sheet).lower() for x in ["contents", "notes", "commentary"]):
                print(f"Skipping non-data sheet: {sheet}")
                continue

            header_row = find_best_header_row(df_raw)

            if header_row is None:
                print(f"Skipping sheet with no usable header: {sheet}")
                continue

            # split header and data
            raw_columns = df_raw.iloc[header_row].tolist()
            cleaned_columns = [clean_column_name(c) for c in raw_columns]

            # keep only columns with usable names
            keep_indices = [i for i, c in enumerate(cleaned_columns) if c is not None]
            cleaned_columns = [cleaned_columns[i] for i in keep_indices]
            cleaned_columns = make_unique_columns(cleaned_columns)

            if len(cleaned_columns) < 2:
                print(f"Skipping sheet with too few usable columns: {sheet}")
                continue

            df = df_raw.iloc[header_row + 1:, keep_indices].copy()
            df.columns = cleaned_columns

            # remove fully empty rows
            df = df.dropna(how="all")

            if df.empty:
                print(f"Skipping empty data after cleaning: {sheet}")
                continue

            # remove rows that are clearly title/note rows inside the table
            bad_row_pattern = re.compile(
                r"(worksheet|table\s+\d|contents|notes|commentary|marriages in england and wales|correction notice)",
                flags=re.IGNORECASE
            )

            df = df[
                ~df.astype(str).apply(
                    lambda row: row.str.contains(bad_row_pattern, na=False).any(),
                    axis=1
                )
            ]

            df = df.dropna(how="all")

            if df.empty:
                print(f"Skipping sheet with no real rows left: {sheet}")
                continue

            # convert to records
            rows = df.to_dict(orient="records")

            sheet_data = {
                "sheet_name": sheet,
                "columns": cleaned_columns,
                "rows": rows
            }

            document["sheets"].append(sheet_data)
            print(f"Kept sheet: {sheet} | columns: {len(cleaned_columns)} | rows: {len(rows)}")

        except Exception as e:
            print("Skipping sheet:", sheet, "| Error:", e)

    output_name = os.path.splitext(file)[0] + "_clean.json"
    output_path = os.path.join(folder, output_name)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(document, f, indent=2, ensure_ascii=False)

    print("Saved:", output_name)

print("\nAll files converted to cleaned JSON.")
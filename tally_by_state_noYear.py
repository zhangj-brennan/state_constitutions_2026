import csv
from collections import defaultdict

# =========================
# CONFIG
# =========================
INPUT_CSV = "BOS Amendment Data 2005-2024 BCJ 1.2.1.csv"
OUTPUT_CSV = "tally_by_state.csv"

STATE_COL = "v1"

# Columns you want to count "1"s in
COUNT_COLUMNS = [
   "v9","v10","v11","v12", "v13","v14","v15", "v16","v17","v18","v19","v20","v21","v22","v23"
]

# =========================
# HELPER (clean BOM + whitespace)
# =========================
def clean_string(s):
    if isinstance(s, str):
        return s.replace("\ufeff", "").strip()
    return s

# =========================
# PROCESS
# =========================

# Structure:
# {state: {col: count}}
counts = defaultdict(lambda: {col: 0 for col in COUNT_COLUMNS})

with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    # Clean headers
    reader.fieldnames = [clean_string(h) for h in reader.fieldnames]

    for row in reader:
        row = {clean_string(k): clean_string(v) for k, v in row.items()}

        state = row[STATE_COL]

        for col in COUNT_COLUMNS:
            val = row.get(col, "")

            if val == "1":
                counts[state][col] += 1

# =========================
# WRITE OUTPUT
# =========================

states = sorted(counts.keys())

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    fieldnames = [STATE_COL] + COUNT_COLUMNS
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    for state in states:
        row = {STATE_COL: state}
        row.update(counts[state])
        writer.writerow(row)

print("Done. Output saved to:", OUTPUT_CSV)
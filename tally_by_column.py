import csv
from collections import defaultdict

# =========================
# CONFIG
# =========================
INPUT_CSV = "BOS Amendment Data 2005-2024 BCJ 1.2.1.csv"
OUTPUT_CSV = "tally.csv"

STATE_COL = "v1"
YEAR_COL = "v2"

# Columns you want to count "1"s in
COUNT_COLUMNS = [
    "v16","v17","v18","v19","v20","v21","v22","v23"
]

# =========================
# PROCESS
# =========================

# Structure:
# {(state, year): {col: count}}
counts = defaultdict(lambda: {col: 0 for col in COUNT_COLUMNS})

with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        state = row[STATE_COL]
        year = row[YEAR_COL]

        key = (state, year)

        for col in COUNT_COLUMNS:
            val = row.get(col, "").strip()

            # Treat "1" as true
            if val == "1":
                counts[key][col] += 1

# =========================
# WRITE OUTPUT
# =========================

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    fieldnames = [STATE_COL, YEAR_COL] + COUNT_COLUMNS
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    for (state, year), col_counts in counts.items():
        row = {
            STATE_COL: state,
            YEAR_COL: year,
        }
        row.update(col_counts)

        writer.writerow(row)

print("Done. Output saved to:", OUTPUT_CSV)
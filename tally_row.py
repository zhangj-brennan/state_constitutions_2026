import pandas as pd

# =========================
# CONFIG
# =========================
INPUT_CSV = "BOS Amendment Data 2005-2024 BCJ 1.2.1.csv"
OUTPUT_CSV = "state_year_pivot.csv"

STATE_COL = "v1"
YEAR_COL = "v2"

# Set to 1 for normal years, 2 for 2-year bins, 3 for 3-year bins
YEAR_BIN_SIZE = 2

# If True, labels look like 2000-2001
# If False, labels are just the bin start year like 2000
USE_RANGE_LABELS = True

# =========================
# LOAD
# =========================
df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
df.columns = df.columns.str.replace("\ufeff", "", regex=False).str.strip()

# Clean key fields
df[STATE_COL] = df[STATE_COL].astype(str).str.strip()
df[YEAR_COL] = pd.to_numeric(df[YEAR_COL], errors="coerce")
df = df.dropna(subset=[YEAR_COL])
df[YEAR_COL] = df[YEAR_COL].astype(int)

# =========================
# BUILD YEAR BINS
# =========================
if YEAR_BIN_SIZE <= 1:
    df["year_bin"] = df[YEAR_COL]
else:
    min_year = df[YEAR_COL].min()

    # Put years into bins starting from the minimum year in the file
    bin_start = min_year + ((df[YEAR_COL] - min_year) // YEAR_BIN_SIZE) * YEAR_BIN_SIZE
    bin_end = bin_start + YEAR_BIN_SIZE - 1

    if USE_RANGE_LABELS:
        df["year_bin"] = bin_start.astype(str) + "-" + bin_end.astype(str)
    else:
        df["year_bin"] = bin_start

# =========================
# CREATE PIVOT
# =========================
pivot = (
    df.groupby(["year_bin", STATE_COL])
      .size()
      .unstack(fill_value=0)
)

# Sort states alphabetically
pivot = pivot.sort_index(axis=1)

# Sort rows
if YEAR_BIN_SIZE <= 1 or not USE_RANGE_LABELS:
    pivot = pivot.sort_index()
else:
    # Sort range labels by first year in the label
    pivot = pivot.loc[
        sorted(pivot.index, key=lambda x: int(str(x).split("-")[0]))
    ]

# =========================
# SAVE
# =========================
pivot.to_csv(OUTPUT_CSV)

print("Done. Output saved to:", OUTPUT_CSV)
import pandas as pd

# =========================
# CONFIG
# =========================
INPUT_CSV = "BOS Amendment Data 2005-2024 BCJ 1.2.1.csv"
OUTPUT_CSV = "pivot_single_variable.csv"

STATE_COL = "v1"
YEAR_COL = "v2"

# 👇 Column to count "1"s from
TARGET_COLUMN = "v21"

# Year binning
YEAR_BIN_SIZE = 2         # 1 = no binning, 2 = 2-year bins, 3 = 3-year bins
USE_RANGE_LABELS = True    # True → "2000-2001", False → "2000"

# =========================
# LOAD
# =========================
df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")

# Clean headers
df.columns = df.columns.str.replace("\ufeff", "", regex=False).str.strip()

# Clean key fields
df[STATE_COL] = df[STATE_COL].astype(str).str.strip()
df[YEAR_COL] = pd.to_numeric(df[YEAR_COL], errors="coerce")
df = df.dropna(subset=[YEAR_COL])
df[YEAR_COL] = df[YEAR_COL].astype(int)

# Clean target column → numeric 0/1
df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce").fillna(0)

# =========================
# YEAR BINNING
# =========================
if YEAR_BIN_SIZE <= 1:
    df["year_bin"] = df[YEAR_COL]
else:
    bin_start = (df[YEAR_COL] // YEAR_BIN_SIZE) * YEAR_BIN_SIZE
    bin_end = bin_start + YEAR_BIN_SIZE - 1

    if USE_RANGE_LABELS:
        df["year_bin"] = bin_start.astype(str) + "-" + bin_end.astype(str)
    else:
        df["year_bin"] = bin_start

# =========================
# PIVOT (sum of 1s)
# =========================
pivot = (
    df.groupby(["year_bin", STATE_COL])[TARGET_COLUMN]
      .sum()
      .unstack(fill_value=0)
)

# Sort columns (states)
pivot = pivot.sort_index(axis=1)

# Sort rows (years or bins)
if YEAR_BIN_SIZE <= 1 or not USE_RANGE_LABELS:
    pivot = pivot.sort_index()
else:
    pivot = pivot.loc[
        sorted(pivot.index, key=lambda x: int(str(x).split("-")[0]))
    ]

# =========================
# SAVE
# =========================
pivot.to_csv(OUTPUT_CSV)

print("Done. Output saved to:", OUTPUT_CSV)
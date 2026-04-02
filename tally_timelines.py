import csv
from collections import defaultdict

# =========================
# CONFIG
# =========================
INPUT_CSV = "BOS Amendment Data 2005-2024 BCJ 1.2.1.csv"
OUTPUT_CSV = "year_tally_5.csv"

YEAR_COL = "year"

COUNT_COLUMNS = [
    "v9","v10","v11","v12","v13","v14","v15",
    "v16","v17","v18","v19","v20","v21","v22","v23"
]

# 1 = single years, 2 = 2-year buckets, 3 = 3-year buckets, etc.
YEAR_BIN_SIZE = 5

# True -> labels like 2005-2006
# False -> labels like 2005
USE_RANGE_LABELS = True

LABELS = {
    "v4": "pass",
    "v9":  'Civil rights("right", "domain", "affirmative", "ethnicity", "race")',
    "v10": 'Criminal law("marijuana", "crime", "criminal")',
    "v11": 'Criminal procedure("bail", "felon", "jury", "trial", "bond")',
    "v12": 'Economic and labor rights("work", "wage", "union", "collective")',
    "v13": 'Education("education", "school", "college", "university")',
    "v14": 'Environment("energy", "conservation", "forest", "natural", "parks", "renewable", "resources", "lands")',
    "v15": 'Government structure("legislature", "legislative", "legislator", "senate", "term", "retire", "salary", "commission", "governor", "gubernatorial", "executive", "board", "judicial", "judges", "court", "office", "official", "government")',
    "v16": 'Gun rights("gun", "arms")',
    "v17": 'Judicial selection and administration("court", "judicial", "judge")',
    "v18": 'Reproductive rights("abortion", "parental")',
    "v19": 'Speech and religion("speech", "expression", "religion", "exercise", "establishment")',
    "v20": 'Torts and liability("tort", "liab")',
    "v21": 'Voting rights and elections("voting", "election", "district", "campaign", "voter", "ID", "primaries", "primary", "absentee", "regist")',
    "v22": 'Redistricting("redistrict")',
    "v23": 'LGBTQ+("sex", "marriage", "SSM")'
}

# =========================
# HELPERS
# =========================
def clean_string(s):
    if isinstance(s, str):
        return s.replace("\ufeff", "").strip()
    return s

def is_one(val):
    return str(val).strip() == "1"

def make_year_bin(year_value, bin_size=1, use_range_labels=True):
    try:
        year = int(str(year_value).strip())
    except (ValueError, TypeError):
        return None

    if bin_size <= 1:
        return str(year)

    bin_start = (year // bin_size) * bin_size
    bin_end = bin_start + bin_size - 1

    if use_range_labels:
        return f"{bin_start}-{bin_end}"
    return str(bin_start)

def sort_bin_key(bin_label):
    s = str(bin_label)
    try:
        return int(s.split("-")[0])
    except (ValueError, TypeError):
        return 999999999

# =========================
# PROCESS
# =========================
counts = defaultdict(lambda: {col: 0 for col in COUNT_COLUMNS})

with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [clean_string(h) for h in reader.fieldnames]

    for row in reader:
        row = {clean_string(k): clean_string(v) for k, v in row.items()}

        year_bin = make_year_bin(
            row.get(YEAR_COL),
            bin_size=YEAR_BIN_SIZE,
            use_range_labels=USE_RANGE_LABELS
        )
        if not year_bin:
            continue

        for col in COUNT_COLUMNS:
            if is_one(row.get(col)):
                counts[year_bin][col] += 1

# =========================
# WRITE OUTPUT
# =========================
year_bins = sorted(counts.keys(), key=sort_bin_key)
output_columns = [LABELS.get(col, col) for col in COUNT_COLUMNS]

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    fieldnames = [YEAR_COL] + output_columns
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    for year_bin in year_bins:
        row = {YEAR_COL: year_bin}

        for col in COUNT_COLUMNS:
            label = LABELS.get(col, col)
            row[label] = counts[year_bin][col]

        writer.writerow(row)

print("Done. Output saved to:", OUTPUT_CSV)
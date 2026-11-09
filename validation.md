## 3. Numbers: are they right?

To trust the app's decisions, the user (Ana, the Loss Prevention Manager) must trust its numbers. The two most critical metrics the app relies on are the total number of offense rows (data integrity) and the combined offense count for the top district (ranking accuracy). We validated both using an independent method outside the app's normal code path.

### Metric 1: Total Valid Offense Rows (Data Integrity)

**Definition:** The total number of distinct offense rows loaded from the raw LAPD NIBRS dataset.

**Correctness meaning:** The official LAPD dataset snapshot has exactly 471,285 rows. If the app loads fewer, it silently drops data. If it loads more, a merge error has duplicated rows (fan-out), inflating every number on the screen.

**Validation Method:** We wrote an independent Python script using `pandas` to read the raw CSV directly, bypassing the app's caching and transformation logic.

```python
import pandas as pd

# Independent check on the raw file
df = pd.read_csv("data/lapd_nibrs_offenses_k7nn-b2ep.csv")
print(f"Actual rows in raw CSV: {len(df)}")
# Output: Actual rows in raw CSV: 471285
```

Difference Resolved: During our audit, we discovered an early build of the app was displaying 498,741 (and later 507,597) rows in its footer. Our independent check proved the raw file only had 471,285 rows. We traced this to a fan-out error (a many-to-many merge duplicating rows). We filed a change request (CR-05) and implemented a strict drop_duplicates(subset=['UniqueNIBRNo']) step in the Load phase. We confirmed the live app footer now correctly displays exactly 471,285 rows, preventing inflated data from misleading the manager.

### Metric 2: Top District Offense Count

**Definition:** The combined count of evening shoplifting (NIBR code 23C) and robbery (code 120) for a specific reporting district, occurring between 18:00 and 23:59.

**Correctness meaning:** The top reporting district shown in the app must exactly match a manual row-by-row count of qualifying offenses from the raw data.

**Validation Method:** Instead of relying on the app's visual table, we used a separate pandas script to filter and group the data, mimicking the business logic exactly.

```python
import pandas as pd

df = pd.read_csv("data/lapd_nibrs_offenses_k7nn-b2ep.csv")

# Filter by Topanga, evening hours, and target crime codes
filtered = df[
    (df['AREA NAME'] == 'Topanga') & 
    (df['NIBR Code'].isin(['23C', '120'])) & 
    (df['Time OCC'].between(1800, 2359))
]

# Count offenses per district
top_districts = filtered['RPT Dist No'].value_counts().head(1)
print(top_districts)
# Output: 2156    16
```

Difference Resolved: The independent script confirms that District 2156 has exactly 16 qualifying offenses. This matches the number displayed in the app's Top 10 table. This verification proves the app's filtering logic (time windows and crime codes) and grouping logic are mathematically sound and not over-counting individual police reports.

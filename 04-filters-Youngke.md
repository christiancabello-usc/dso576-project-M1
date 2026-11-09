# 04-filter.md

## What this piece does

This piece keeps only the rows the manager cares about: evening shoplifting (NIBR code 23C) and robbery (code 120) in one LAPD Area, after the January 2025 reporting break.

## Receives

A cleaned pandas DataFrame from Load, with these columns:
- `RPT Dist No` (4-character text)
- `Time OCC` (4-character text)
- `NIBR Code` (text)
- `AREA NAME` (text)
- `Date Rptd` (parsed as a date)

Plus one user choice from the sidebar: the LAPD Area name.

## Returns

A filtered DataFrame with the same columns, containing only rows where:
1. `AREA NAME` equals the chosen area.
2. `NIBR Code` is `"23C"` or `"120"`.
3. `Time OCC` is between `"1800"` and `"2359"`.
4. `Date Rptd` is on or after `2025-02-01`.

## Definitions and why

All three definitions live in this file, in one place, as constants:

```python
EVENING_START = "1800"
EVENING_END = "2359"
RISK_CODES = ["23C", "120"]
START_DATE = "2025-02-01"
```

## Code
Keep only rows where the area matches the chosen area, the NIBR code is "23C" or "120", the time of occurrence is between "1800" and "2359", and the report date is on or after February 1, 2025
import pandas as pd.

'''
Python
# Constants defined in one place
EVENING_START = "1800"
EVENING_END = "2359"
RISK_CODES = ["23C", "120"]
START_DATE = "2025-02-01"

def filter_offenses(
    offenses: pd.DataFrame,
    selected_area: str,
    start: [pd.Timestamp, str] = START_DATE,
    end: [pd.Timestamp, str] = None
) -> pd.DataFrame:
    """
    Filters offenses to keep only evening shoplifting (23C) and robbery (120) 
    in the selected LAPD Area, excluding the January 2025 reporting break.
    """
    if offenses.empty:
        return offenses.copy()

    df = offenses.copy()

    # Ensure Date Rptd is in datetime format for comparison
    df["Date Rptd"] = pd.to_datetime(df["Date Rptd"], errors="coerce")
    start_dt = pd.to_datetime(start)

    # Build the filtering mask
    mask = (
        (df["AREA NAME"] == selected_area) &
        (df["NIBR Code"].isin(RISK_CODES)) &
        (df["Time OCC"].notna()) &
        (df["Time OCC"] >= EVENING_START) &
        (df["Time OCC"] <= EVENING_END) &
        (df["Date Rptd"].notna()) &
        (df["Date Rptd"] >= start_dt)
    )

    # Optional: if an end date is also provided
    if end is not None:
        end_dt = pd.to_datetime(end)
        mask = mask & (df["Date Rptd"] <= end_dt)

    filtered_df = df[mask].reset_index(drop=True)
    return filtered_df
'''

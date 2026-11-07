Team repository: https://github.com/christiancabello-usc/dso576-project-M1

# CVS Evening Loss-Prevention Navigator — One-Shot Build Prompt

## 00 — Vision

The **Regional Loss Prevention Manager at CVS Health** in Los Angeles must decide, each quarter, **which five LAPD reporting districts should be prioritized for a second security guard on the evening shift (18:00–24:00)**. The manager then assigns guards to individual CVS stores within those priority districts using local store knowledge. Today this decision relies on store managers' intuition and monthly total incident counts, which cannot separate evening from daytime risk or distinguish shoplifting from robbery on the reporting-district level.

### What the tool is

A one-screen Streamlit page. The manager selects one LAPD Area from a sidebar dropdown, and the page shows:

- A ranked table of the top 10 RPT Dist Nos in that area by combined evening shoplifting (NIBR code 23C) and robbery (code 120) counts.
- A bar chart of the same top 10.
- A caption under both: "Reported offenses, not actual crime. Evening = 18:00–24:00. January 2025 reporting break excluded."

### What the manager cares about

- Reducing shoplifting and robbery during the evening shift.
- Keeping the guard budget under control by putting the second guard where the risk is highest.
- Defending the allocation to regional leadership with a clear, data-backed shortlist.

### Use cases

1. Rank the top 10 RPT Dist Nos in one LAPD Area by combined evening 23C + 120 counts, to identify the five priority districts for a second guard.
2. Compare LAPD Areas by combined evening counts, to decide which area to prioritise this quarter.
3. Export the ranked table to justify the quarterly guard allocation to regional leadership.
4. Exclude the January 2025 NIBRS reporting break so the ranking is not distorted by the system migration.


## 01 — Design

### Design principles

1. **One piece, one job.** Each piece has one responsibility and can be checked independently using a small sample DataFrame.
2. **Only Load reads the offense CSV; only View renders the screen.** Setup reads only its configuration file. Filter and Rank work on pandas DataFrames in memory.
3. **One place for each definition.** Filter defines the evening window and risk codes, which are reused by Area Summary. Setup owns the reporting-date window.
4. **Load once, filter and rank on selection changes.** The normalized DataFrame is cached with `@st.cache_data`. Changing the selected LAPD Area reruns filtering and district ranking without rereading the CSV.

### Pieces

| Piece | Implementation file | Owner | Receives | Returns |
|---|---|---|---|---|
| 1. Load | `src/data.py` | Christian | LAPD offenses CSV path | Normalized offenses DataFrame |
| 2. Setup | `src/setup.py` | Yutong Wu | `configs/default.toml` | Validated starting defaults |
| 3. Filter | `src/filter.py` | Youngke Li | Normalized DataFrame, selected Area, start/end dates | Filtered offense DataFrame |
| 4. Area Summary | `src/rank.py` | Khushi, Evelyn | Normalized DataFrame, start/end dates | Ranked counts for all 21 LAPD Areas |
| 5. Rank Districts | `src/rank.py` | Khushi | Filtered DataFrame, `k=10` | Ranked top-10 district DataFrame |
| 6. View | `src/view.py` | Deenal | Area Summary and ranked district DataFrames | Streamlit page |

Both Area Summary and Rank Districts live in `src/rank.py`. Area Summary is written by Evelyn, Rank Districts by Khushi, in separate functions with separate tests.

### When each piece runs

- **Load:** At application startup. Cache the result so sidebar interactions do not reread the CSV.
- **Setup:** At application startup. Read and validate the default Area and reporting dates.
- **Area Summary:** After Load and Setup, using the configured date window. Recalculate when the application reloads with updated configuration.
- **Filter:** At startup and whenever the selected LAPD Area changes.
- **Rank Districts:** After Filter, using the filtered DataFrame.
- **View:** At startup and after sidebar changes, displaying the current rankings and charts.

The reporting-date window is configured in `configs/default.toml`, not through the Streamlit interface. Updated configuration values take effect when the application reloads them.

### Real-world operation

The LAPD offenses file contains 471,285 rows and is approximately 143.4 MB in the September 2026 snapshot (`data_overview_lapd-nibrs.md`, section 4).

Load uses pandas with explicit column types and `usecols` to read only the fields required for the application and the specified normalization steps.

The normalized DataFrame is cached using `@st.cache_data`. Sidebar interactions reuse the cached data and do not reread the source CSV.

The initial application runs locally with Python, pandas, and Streamlit. Keep the raw CSV unchanged and exclude the downloaded `data/` directory from Git.

For later cloud deployment, provide the same data snapshot and configuration in the deployment environment while preserving the existing module interfaces.

### Build order and run

Build and verify the application in this order:

1. Implement Load and validate the normalized DataFrame against the sample CSV.
2. Implement Setup and verify the configuration defaults.
3. Implement Filter and test the Area, offense-code, evening-time, and reporting-date boundaries.
4. Implement Area Summary and Rank Districts, reusing Filter's shared definitions.
5. Implement View and connect the modules through `app.py`.
6. Run the application and check the outputs against the module-level "Done when" tests.

**Environment:** Python with pandas and Streamlit. Declare dependencies in `requirements.txt`.

**Entry point:** `app.py`

**Run locally:**

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Integration checks — Done when

1. The application opens with the configured default LAPD Area.
2. The Area comparison displays ranked counts for the configured reporting-date window.
3. The district table and bar chart show the same top-10 reporting districts and combined offense counts.
4. The first five districts are clearly identified as the priority shortlist.
5. Changing the selected Area updates the district table and chart without rereading the offenses CSV.
6. Exporting the ranked table produces a CSV matching the displayed results and includes the required context.
7. An Area with no qualifying offenses displays an empty result without crashing.
8. The application runs locally using the documented installation and startup commands.
9. The config fits the downloaded data (checked after Load and Area Summary; Setup never reads the CSV):
   - `default_area` is the first row of the Area Summary for `start`–`end`; if not, set `default_area` to that Area in `configs/default.toml`.
   - The month of `end` is complete: its `Date Rptd` count is at least 90% of the median of the six months before it, and the month after it is not. Sample: July 2026 has 991 reports against 870–1,004; August 2026 has 663.

## 02 — Load and normalize data

Build a loader that reads the local LAPD NIBRS offenses CSV snapshot and returns one normalized pandas DataFrame, `offenses`. One row represents one charged offense on a police report. Later pieces receive this table and must not reread or mutate the source CSV.

| Input | Output | Purpose |
|---|---|---|
| `data/lapd_nibrs_offenses_k7nn-b2ep.csv` | `offenses` | Incident-level offense analysis |
| `sample/offenses_sample.csv` | the same output | Development and loader checks before the full download is available |

Keep the raw CSVs unchanged and do not commit the downloaded `data/` folder. Use pandas for the typed local CSV read. The full offenses file is about 143 MB with 471,285 rows, so later callers should pass the columns they need; use `usecols` rather than loading unneeded columns.

### Required normalization

- Read `CaseNo`, `UniqueNIBRNo`, `Time OCC`, `AREA`, and `RPT Dist No` as strings. Do not coerce `CaseNo` to a number: leading zeros matter and one value is the literal `RFC CITATION`. Normalize valid `Time OCC` values to zero-padded four-character `HHMM` text; leave blank, malformed, or impossible times missing, and record their count for the limitations/methodology piece.
- Strip trailing whitespace from text fields, including `offenses["AREA NAME"]`.
- Replace `AREA` with its two-digit zero-padded normalized text and `RPT Dist No` with its four-digit zero-padded normalized text. Leave missing values missing.
- Parse `Date Rptd` and `Date OCC` using the documented month-first format with invalid values coerced to missing. Do not silently discard missing or invalid dates; record their counts for the limitations/methodology piece.
- Do not fill a blank value with a substantive value such as zero, `No`, or `Unknown` unless a later piece explicitly defines that transformation.
- **Deduplicate the DataFrame.** Drop duplicate rows based on `UniqueNIBRNo` to prevent fan-out errors. The final loaded DataFrame must have exactly 471,285 rows.
- Remove unnecessary columns for the scope of the project **after** passing the raw CSV file as a variable.
- After reading the CSV into the `offenses` DataFrame and before returning it,
  create `Type of Crime` from every original column whose name ends in
  `Crime`. For each offense, list the names of every such column whose value
  is `Yes`, separated by `; `; one offense may therefore have more than one
  listed type. Then remove the individual `*Crime` source columns from the
  returned DataFrame. Preserve `NIBR Code`; Filter and Rank continue to use it
  for the 23C/120 counts.

The loader only normalizes formats and reports quality checks. It does not choose the tool's harm measures, remove plausible-looking records, impute missing values, or create rankings. In particular, later metric pieces must decide how to handle impossible `Date OCC` values, incomplete recent weeks, and zero latitude/longitude values before using those fields in a chart or map.

### Done when

1. The loader runs against the sample offenses CSV and the full offenses CSV using the same interface.
2. It reports input and output row counts, missing parsed-date counts, and the number of distinct normalized `AREA` and `RPT Dist No` values.
3. `UniqueNIBRNo` is unique in `offenses`; a failed check stops the build with an actionable error.
4. The full snapshot check reports 471,285 offense rows and 21 normalized areas (the row total may differ after a publisher refresh, so display the observed total and download date).


## 03 — Filter

This piece keeps only the rows the manager cares about: evening shoplifting (NIBR code 23C) and robbery (code 120) in one LAPD Area, after the January 2025 reporting break.

### Receives

A cleaned pandas DataFrame from Load, with these columns:

- `RPT Dist No` (4-character text)
- `Time OCC` (zero-padded 4-character HHMM text)
- `NIBR Code` (text)
- `AREA NAME` (text)
- `Date Rptd` (parsed as a date)
- `Date OCC` (parsed as a date)

Plus the selected LAPD Area name from the sidebar and `start`/`end` dates from Setup.

### Returns

A filtered DataFrame with the same columns, containing only rows where:

1. `AREA NAME` equals the chosen area.
2. `NIBR Code` is `"23C"` or `"120"`.
3. `Time OCC` is between `"1800"` and `"2359"`.
4. `Date OCC` is inclusively between `start` and `end`.

Rows with missing or invalid `Time OCC` or `Date Rptd` values are excluded. The original DataFrame is not modified. If no rows match, return an empty DataFrame with the same columns.

### Definitions and why

The evening window and risk codes live in this file, in one place, as constants. Setup owns the date window.

```python
EVENING_START = "1800"
EVENING_END = "2359"
RISK_CODES = ["23C", "120"]
```

### Contract — `src/filter.py`

```python
def filter_offenses(
    offenses: pd.DataFrame,
    selected_area: str,
    start: date,
    end: date,
) -> pd.DataFrame:
    ...
```

Filter operates on the in-memory DataFrame and does not read files, aggregate counts, or rank districts.

### Done when

1. Only the selected LAPD Area and NIBR codes `23C` and `120` are retained.
2. Records at `1800` and `2359` are included; records at `1759` and `0000` are excluded.
3. Records on both `start` and `end` dates are included; records outside the range are excluded.
4. Missing or invalid dates and times are excluded.
5. The input DataFrame remains unchanged, and an empty result preserves the original columns.

## 04 — Rank

### Area summary

The Area Summary calculation supports the all-area comparison before a manager chooses an area. It receives the normalized `offenses` DataFrame plus `start` and `end` from Setup. It applies the same `RISK_CODES`, evening window, and inclusive date range (on `Date OCC`) as Filter, but does not filter on area. It returns one row per `AREA NAME`, with `AREA NAME`, `shoplifting_incidents`, `robbery_incidents`, and `combined_incidents`, sorted by `combined_incidents` descending and then `AREA NAME` ascending.

The area-comparison view uses this returned table; it must not recompute the
counts or read the CSV.

### District rank

The Rank piece turns the filtered offense rows into the district-level table
used by every results view. It receives the filtered DataFrame and `k` (an
integer, default `10`) and returns a DataFrame with these columns:

| Column | Definition |
|---|---|
| `rank` | One-based position after sorting |
| `RPT Dist No` | Normalized four-character reporting-district identifier |
| `shoplifting_incidents` | Count of filtered rows where `NIBR Code == "23C"` |
| `robbery_incidents` | Count of filtered rows where `NIBR Code == "120"` |
| `combined_incidents` | `shoplifting_incidents + robbery_incidents` |

Count offense rows, not distinct `CaseNo` values: each row is one charged
offense. Include a district when it has at least one qualifying row. Sort by
`combined_incidents` descending, then `shoplifting_incidents` descending,
then `robbery_incidents` descending, then `RPT Dist No` ascending for a
deterministic tie-breaker. Return the first `k` rows; if fewer than `k`
districts qualify, return every qualifying district.

If no district has a qualifying offense, return an empty DataFrame with **all five output columns in the documented order**, rather than returning `None` or raising an error. Validate `k` as a positive integer; an invalid value (for example, `0`, `-1`, or a string) raises a `ValueError` that mentions `k`. For a valid `k`, return no more than `k` rows and number `rank` consecutively from 1. Do not change the filtered input DataFrame.

### Done when

1. On a small invented table with two 23C rows and one 120 row in district
   `0101`, and one 23C row in district `0102`, the result ranks `0101` first
   with counts `2`, `1`, and `3`, followed by `0102` with counts `1`, `0`, and
   `1`.
2. A tie on all three count columns sorts the smaller normalized `RPT Dist No`
   first.
3. The View can render the returned DataFrame without recomputing counts.

## 05 — Views

All views use recorded incidents in the LAPD Area that are reported between 18:00 and 24:00, with NIBRS crime codes 23C (shoplifting) or 120 (robbery). Exclude January 2025.

- **Starting Screen Layout/Contract** (`layout_contract`): This displays what the user sees on the first screen before they start any usage. First, a sidebar opens with the 'default_area', which is where they select one of the LAPD areas. The Area comparison is also shown here for the user to compare data. Next the top 10 ranked district table will appear with the bar chart that corresponds to the selected Area. The export will apply to the ranking of the selected area. Area comparison will remain as a display-only. 
- **Ranked RPT Dist Nos** (`top10_districts`): a table of the top 10 RPT Dist Nos ranked by combined count of qualifying evening offences. Columns: rank, RPT Dist No, shoplifting incidents, robbery incidents, combined incidents. The first five rows are visually marked as the recommended priority-district shortlist; the manager assigns guards to individual stores within those districts. Option: `k`, default 10.
- **Evening-risk bar chart** (`evening_risk_chart`): horizontal bar chart of the ranked top 10 RPT Dist Nos, sorted descending by incident count. X-axis: combined reported offences. Y-axis: RPT Dist No. Tooltip shows the shoplifting and robbery breakdown.
- **Area comparison** (`area_comparison`): display-only bar chart ranking every LAPD Area by combined qualifying evening offences. This supports quarterly prioritisation before the manager selects an area from the sidebar dropdown.
- **Export** (`export_ranked_table`): downloads the current ranked table as CSV, including the applied area, time window, offence codes, exclusion note, and export date.

Every results view shows this caption: “Reported offenses, not actual crime. Evening = 18:00–24:00. Drop data from January 2025 reporting.”

## 06 — Setup

Setup reads the starting defaults (the LAPD Area shown when the page opens, and the time window) from one config file, checks them, and returns them as one object. Setup runs once at startup. It reads only its own config file: never the LAPD CSV (Load) and never the screen (View).

### Config file — `configs/default.toml`

```toml
default_area = "Mission"     # Area preselected in the sidebar: the most evening 23C + 120 offences
start        = "2025-02-01"    # after the January 2025 NIBRS reporting break
end          = "2026-07-31"    # last complete month; August 2026 is still being entered
```

The page should open on the Area the manager is most likely to act on. In the team's sample (2025-02-01 to 2026-07-31, 18:00–23:59), Mission has the most evening 23C + 120 offences (33: 28 shoplifting, 5 robbery), just ahead of Pacific and Wilshire (32 each). The full data decides (Integration check 9).

The tool uses this fixed, explicitly configured inclusive reporting range; it
does not calculate a rolling window. At a quarterly review, the manager edits
`start` and/or `end` in this file to select the intended comparison period;
no code changes are required.

### Contract — `src/setup.py`

```python
@dataclass(frozen=True)
class Defaults:
    default_area: str
    start: date
    end: date

def load_defaults(path: Path = Path("configs/default.toml")) -> Defaults: ...
```

| Field | Passed to | Use |
|---|---|---|
| `default_area` | View | initial choice in the sidebar dropdown |
| `start`, `end` | Filter | keeps rows with `start ≤ Date OCC ≤ end` |

### Checks

`load_defaults` raises a `ValueError` naming the field and the bad value when:

- `default_area` is not one of the 21 Area names: Central, Rampart, Southwest, Hollenbeck, Harbor, Hollywood, Wilshire, West LA, Van Nuys, West Valley, Northeast, 77th Street, Newton, Pacific, N Hollywood, Foothill, Devonshire, Southeast, Mission, Olympic, Topanga;
- `start` is before 2025-02-01, or `end` is not after `start`;
- a key is missing or unknown.

### Done when

1. `load_defaults()` returns dates and an Area that passes validation; on the prepared data, the default Area equals the first row of the Area Summary for its configured window.
2. A test file with `default_area = "Hollywod"` raises a `ValueError` whose message contains `Hollywod`; one with `start = 2024-06-01` raises one naming `start`.

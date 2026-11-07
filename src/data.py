"""The only module that reads offense CSVs; normalization never filters rows."""
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_COLUMNS = ['CaseNo', 'UniqueNIBRNo', 'Date Rptd', 'Date OCC', 'Time OCC',
                'AREA', 'AREA NAME', 'RPT Dist No', 'NIBR Code']
DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'

@st.cache_data(show_spinner=False)
def load_offenses(path: str | Path) -> pd.DataFrame:
    offenses = pd.read_csv(path, dtype='string', usecols=lambda c: c in BASE_COLUMNS or c.endswith('Crime') or c == 'Type of Crime')
    input_rows = len(offenses)
    for col in offenses:
        offenses[col] = offenses[col].str.rstrip().replace('', pd.NA)
    crime_cols = [c for c in offenses if c.endswith('Crime') and c != 'Type of Crime']
    if crime_cols:
        offenses['Type of Crime'] = offenses[crime_cols].apply(
            lambda row: '; '.join(c for c in crime_cols if pd.notna(row[c]) and row[c] == 'Yes'), axis=1).astype('string')
        offenses = offenses.drop(columns=crime_cols)
    for col, width in [('AREA', 2), ('RPT Dist No', 4)]:
        offenses[col] = offenses[col].str.zfill(width)
    times = offenses['Time OCC'].str.zfill(4)
    valid = times.str.fullmatch(r'\d{4}', na=False) & times.str[:2].lt('24').fillna(False) & times.str[2:].lt('60').fillna(False)
    offenses['Time OCC'] = times.where(valid)
    for col in ['Date Rptd', 'Date OCC']:
        offenses[col] = pd.to_datetime(offenses[col], format=DATE_FORMAT, errors='coerce')
    if offenses['UniqueNIBRNo'].isna().any() or offenses['UniqueNIBRNo'].duplicated().any():
        raise ValueError('UniqueNIBRNo must be nonmissing and unique. Check the source snapshot for duplicate offense IDs; do not silently deduplicate.')
    offenses.attrs['quality'] = {
        'input_rows': input_rows, 'output_rows': len(offenses),
        'missing_Date_Rptd': int(offenses['Date Rptd'].isna().sum()),
        'missing_Date_OCC': int(offenses['Date OCC'].isna().sum()),
        'missing_or_invalid_Time_OCC': int(offenses['Time OCC'].isna().sum()),
        'distinct_AREA': int(offenses['AREA'].nunique()),
        'distinct_RPT_Dist_No': int(offenses['RPT Dist No'].nunique()),
    }
    return offenses

@st.cache_data(show_spinner=False)
def load_prepared(path: str | Path, metadata_path: str | Path,
                  snapshot_version: tuple[int, int] | None = None) -> tuple[pd.DataFrame, dict]:
    """Read the committed privacy-minimized snapshot, once per file version.

    ``snapshot_version`` is the two file modification times supplied by the
    app. It prevents a running Streamlit server from reusing a cached older
    schema after the prepared snapshot is refreshed.
    """
    import json
    with Path(metadata_path).open() as handle:
        metadata = json.load(handle)
    return pd.read_parquet(path), metadata

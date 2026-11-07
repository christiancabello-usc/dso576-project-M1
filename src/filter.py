"""Shared evening-risk definitions and in-memory selection."""
from datetime import date
import pandas as pd

EVENING_START = '1800'
EVENING_END = '2359'
RISK_CODES = ['23C', '120']

def qualifying_mask(offenses: pd.DataFrame, start: date, end: date) -> pd.Series:
    times = offenses['Time OCC']
    valid_times = times.str.fullmatch(r'(?:[01]\d|2[0-3])[0-5]\d', na=False)
    # The comparison window and the evening window both describe when an
    # offense happened, not when its report was entered by LAPD.
    dates = pd.to_datetime(offenses['Date OCC'], errors='coerce')
    return (offenses['NIBR Code'].isin(RISK_CODES)
            & valid_times & times.between(EVENING_START, EVENING_END)
            & dates.ge(pd.Timestamp(start))
            & dates.lt(pd.Timestamp(end) + pd.Timedelta(days=1))).fillna(False)

def filter_offenses(offenses: pd.DataFrame, selected_areas: str | list[str],
                    start: date, end: date) -> pd.DataFrame:
    areas = [selected_areas] if isinstance(selected_areas, str) else selected_areas
    return offenses.loc[qualifying_mask(offenses, start, end)
                        & offenses['AREA NAME'].isin(areas)].copy()

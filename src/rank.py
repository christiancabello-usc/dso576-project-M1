"""Count charged offense rows; never count distinct police reports."""
from datetime import date
import pandas as pd
from src.filter import qualifying_mask
from src.setup import AREAS

COUNTS = ['shoplifting_incidents', 'robbery_incidents', 'combined_incidents']
DISTRICT_COLUMNS = ['rank', 'RPT Dist No', *COUNTS]
RANKING_MEASURES = {
    'Combined offenses': ['combined_incidents', 'shoplifting_incidents', 'robbery_incidents'],
    'Robbery first': ['robbery_incidents', 'combined_incidents', 'shoplifting_incidents'],
    'Weighted (robbery × 3)': ['priority_score', 'robbery_incidents', 'shoplifting_incidents'],
}

def _counts(rows: pd.DataFrame, key: str | list[str]) -> pd.DataFrame:
    keys = [key] if isinstance(key, str) else key
    counts = rows.groupby([*keys, 'NIBR Code']).size().unstack(fill_value=0)
    counts = counts.reindex(columns=['23C', '120'], fill_value=0)
    counts.columns = COUNTS[:2]
    counts['combined_incidents'] = counts.sum(axis=1)
    return counts.reset_index()

def summarize_areas(offenses: pd.DataFrame, start: date, end: date) -> pd.DataFrame:
    counts = _counts(offenses.loc[qualifying_mask(offenses, start, end)], 'AREA NAME')
    counts = counts.set_index('AREA NAME').reindex(AREAS, fill_value=0).reset_index()
    return counts.sort_values(['combined_incidents', 'AREA NAME'], ascending=[False, True]).reset_index(drop=True)

def rank_districts(filtered: pd.DataFrame, k: int = 10,
                   measure: str = 'Combined offenses', include_area: bool = False) -> pd.DataFrame:
    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ValueError(f'k must be a positive integer; got {k!r}')
    if measure not in RANKING_MEASURES:
        raise ValueError(f'Unknown ranking measure: {measure!r}')
    keys = ['AREA NAME', 'RPT Dist No'] if include_area else ['RPT Dist No']
    counts = _counts(filtered, keys)
    counts['priority_score'] = counts['shoplifting_incidents'] + 3 * counts['robbery_incidents']
    sort_columns = [*RANKING_MEASURES[measure], *keys]
    counts = counts.sort_values(sort_columns, ascending=[False] * len(RANKING_MEASURES[measure]) + [True] * len(keys))
    counts = counts.head(k).reset_index(drop=True)
    counts.insert(0, 'rank', range(1, len(counts) + 1))
    columns = ['rank', *( ['AREA NAME'] if include_area else []), 'RPT Dist No', *COUNTS]
    if measure == 'Weighted (robbery × 3)':
        columns.append('priority_score')
    return counts[columns]

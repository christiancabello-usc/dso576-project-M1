"""Split the app's own evening rows for Central into 18:00-21:59 and 22:00-23:59.
Uses the team's committed snapshot and the app's own filter (src/filter.py)."""
from datetime import date
import pandas as pd
from src.filter import filter_offenses
from src.rank import rank_districts

offenses = pd.read_parquet('data/processed/offenses.parquet')
start, end = date(2025, 8, 1), date(2026, 7, 31)          # "Previous 12 months" in the app
rows = filter_offenses(offenses, 'Central', start, end)    # same rows the app counts
print('Rows the app counts for Central:', len(rows))
print(rank_districts(rows, k=5, measure='Combined offenses').to_string(index=False))

rows['window'] = rows['Time OCC'].str[:2].astype(int).map(lambda h: '22:00-23:59' if h >= 22 else '18:00-21:59')
split = (rows.groupby(['RPT Dist No', 'window', 'NIBR Code']).size()
             .unstack(['window', 'NIBR Code'], fill_value=0))
split.columns = [f'{w} {"shoplift" if c == "23C" else "robbery"}' for w, c in split.columns]
split['app combined'] = split.sum(axis=1)
split['late (22-24) total'] = split.filter(like='22:00').sum(axis=1)
top = split.sort_values('app combined', ascending=False).head(5)
print('\nTop 5 app districts, split by part of the evening:')
print(top.to_string())
print('\nCentral total by window:'); print(rows['window'].value_counts().sort_index().to_string())

# Does it hold, or could it be luck? Same split in two halves of the year.
rows['half'] = rows['Date OCC'].lt(pd.Timestamp('2026-02-01')).map({True: 'Aug25-Jan26', False: 'Feb26-Jul26'})
d = rows[rows['RPT Dist No'] == '0161']
print('\nDistrict 0161 by half-year and window:')
print(d.groupby(['half', 'window']).size().unstack(fill_value=0).to_string())

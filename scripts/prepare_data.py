"""Download unchanged public source, validate, and emit the app's compact snapshot.
Run from repo root: python scripts/prepare_data.py [--refresh]
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data import load_offenses
from src.filter import RISK_CODES
from src.rank import summarize_areas
from src.setup import load_defaults
import pandas as pd

URL = 'https://data.lacity.org/api/views/k7nn-b2ep/rows.csv?accessType=DOWNLOAD'
RAW = ROOT / 'data/raw/lapd_nibrs_offenses_k7nn-b2ep.csv'
OUT = ROOT / 'data/processed'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    if args.refresh or not RAW.exists():
        request = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        temporary = RAW.with_suffix('.part')
        with urllib.request.urlopen(request, timeout=180) as response, temporary.open('wb') as handle:
            while block := response.read(1024 * 1024):
                handle.write(block)
        temporary.replace(RAW)
    offenses = load_offenses(RAW)
    defaults = load_defaults(ROOT / 'configs/default.toml')
    summary = summarize_areas(offenses, defaults.start, defaults.end)
    # Keep both dates and occurrence times for the two risk codes so period edits work.
    # Case identifiers, addresses and coordinates have no role in this product.
    compact = offenses.loc[offenses['NIBR Code'].isin(RISK_CODES),
        ['Date Rptd','Date OCC','Time OCC','AREA','AREA NAME','RPT Dist No','NIBR Code']].copy()
    compact.attrs = {}
    compact.to_parquet(OUT / 'offenses.parquet', index=False)
    monthly = offenses['Date Rptd'].dt.to_period('M').value_counts().sort_index()
    period = pd.Period(defaults.end, freq='M')
    previous = [int(monthly.get(period - i, 0)) for i in range(1, 7)]
    median = float(pd.Series(previous).median())
    next_previous = [int(monthly.get(period + 1 - i, 0)) for i in range(1,7)]
    next_median = float(pd.Series(next_previous).median())
    metadata = {
        'source_url': URL,
        'download_date': datetime.fromtimestamp(RAW.stat().st_mtime, timezone.utc).date().isoformat(),
        'prepared_at': datetime.now(timezone.utc).isoformat(),
        'source_bytes': RAW.stat().st_size,
        'source_sha256': hashlib.file_digest(RAW.open('rb'), 'sha256').hexdigest(),
        'quality': offenses.attrs['quality'], 'condensed_rows': len(compact),
        'monthly_report_counts': {str(k): int(v) for k,v in monthly.items()},
        'configuration_check': {
            'start': str(defaults.start), 'end': str(defaults.end),
            'highest_area': summary.iloc[0]['AREA NAME'],
            'highest_area_count': int(summary.iloc[0]['combined_incidents']),
            'end_month_count': int(monthly.get(period, 0)), 'previous_six_months': previous,
            'previous_six_month_median': median,
            'end_month_complete': bool(monthly.get(period, 0) >= .9 * median),
            'next_month_count': int(monthly.get(period+1, 0)),
            'next_month_previous_six_median': next_median,
            'next_month_complete': bool(monthly.get(period+1, 0) >= .9 * next_median),
        },
    }
    (OUT / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))
    print(summary.to_string(index=False))
    if defaults.default_area != summary.iloc[0]['AREA NAME']:
        print('ACTION: update configs/default.toml default_area to the highest_area above.')
    if not metadata['configuration_check']['end_month_complete'] or metadata['configuration_check']['next_month_complete']:
        print('ACTION: review end in configs/default.toml against monthly counts above.')

if __name__ == '__main__':
    main()

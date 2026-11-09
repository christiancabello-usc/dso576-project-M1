"""MVP validation tests (Section 4): gaps not covered by the original build tests.

Each test names the user-facing promise it protects. Run with: python -m pytest -q
"""
from datetime import date
from io import BytesIO
from types import SimpleNamespace

import pandas as pd
import pytest

from src.data import load_prepared
from src.filter import filter_offenses
from src.rank import rank_districts, summarize_areas
from src.setup import Defaults, load_defaults
from src.view import attach_candidate_stores, export_ranked_table, period_options, read_store_mapping

SNAPSHOT = ('data/processed/offenses.parquet', 'data/processed/metadata.json')


# --- 1. Numbers the cases rely on match the committed snapshot ------------------------------

@pytest.fixture(scope='module')
def offenses():
    return load_prepared(*SNAPSHOT)[0]


def test_central_twelve_months_matches_live_app(offenses):
    """Elena's case (Central, Aug 2025-Jul 2026, combined): totals and top district shown live."""
    start, end = date(2025, 8, 1), date(2026, 7, 31)
    area = summarize_areas(offenses, start, end).set_index('AREA NAME').loc['Central']
    assert (area['shoplifting_incidents'], area['robbery_incidents'], area['combined_incidents']) == (103, 221, 324)
    ranked = rank_districts(filter_offenses(offenses, 'Central', start, end), k=10)
    assert ranked.iloc[0][['RPT Dist No', 'shoplifting_incidents', 'robbery_incidents', 'combined_incidents']].tolist() == ['0161', 59, 10, 69]


def test_area_totals_equal_sum_of_all_district_counts(offenses):
    """The Area metric and the district ranking must count the same rows (no row lost between them)."""
    start, end = date(2025, 8, 1), date(2026, 7, 31)
    areas = summarize_areas(offenses, start, end).set_index('AREA NAME')
    for name in ['Central', 'Topanga', 'Hollywood']:
        rows = filter_offenses(offenses, name, start, end)
        every_district = rank_districts(rows, k=10_000)
        assert every_district['combined_incidents'].sum() == areas.loc[name, 'combined_incidents'] == len(rows)


# --- 2. Ranking measures not covered by the build tests ------------------------------------

def test_robbery_first_orders_by_robbery_then_combined():
    rows = pd.DataFrame({'RPT Dist No': ['0101'] * 5 + ['0102'] * 2 + ['0103'] * 3,
                         'NIBR Code': ['23C'] * 4 + ['120'] + ['120'] * 2 + ['120', '23C', '23C']})
    combined = rank_districts(rows, measure='Combined offenses')['RPT Dist No'].tolist()
    robbery = rank_districts(rows, measure='Robbery first')['RPT Dist No'].tolist()
    assert combined == ['0101', '0103', '0102']
    assert robbery == ['0102', '0101', '0103']   # 2 robberies first; 0101 beats 0103 on combined (5 vs 3)


def test_unknown_measure_is_rejected():
    with pytest.raises(ValueError, match='measure'):
        rank_districts(pd.DataFrame({'RPT Dist No': ['0101'], 'NIBR Code': ['23C']}), measure='Burglary')


# --- 3. Optional CVS store mapping (CR-03 / CR-04 were built without tests) ----------------

def upload(text):
    return SimpleNamespace(getvalue=lambda: text.encode('utf-8'))


def test_store_mapping_pads_district_and_trims_area():
    mapping = read_store_mapping(upload(
        'store_id,store_name,address,area_name,rpt_dist_no\n'
        'S1,CVS 7th St,1 Main St, Central ,161\n'
        'S2,CVS Fig,2 Fig St,Central,0161\n'))
    assert mapping['rpt_dist_no'].tolist() == ['0161', '0161']
    assert mapping['area_name'].tolist() == ['Central', 'Central']


def test_store_mapping_missing_column_is_rejected_with_its_name():
    with pytest.raises(ValueError, match='rpt_dist_no'):
        read_store_mapping(upload('store_id,store_name,address,area_name\nS1,CVS,1 Main St,Central\n'))


def test_candidate_stores_attach_without_changing_counts():
    ranked = pd.DataFrame({'rank': [1, 2], 'AREA NAME': ['Central', 'Central'], 'RPT Dist No': ['0161', '0163'],
                           'shoplifting_incidents': [59, 27], 'robbery_incidents': [10, 4], 'combined_incidents': [69, 31]})
    mapping = pd.DataFrame({'store_id': ['S1', 'S2'], 'store_name': ['CVS A', 'CVS B'], 'address': ['x', 'y'],
                            'area_name': ['Central', 'Central'], 'rpt_dist_no': ['0161', '0161']})
    result = attach_candidate_stores(ranked, mapping)
    assert result['combined_incidents'].tolist() == [69, 31]
    assert result['candidate_store_count'].tolist() == [2, 0]
    assert result.loc[1, 'candidate_stores'] == 'No verified CVS store mapped'
    assert attach_candidate_stores(ranked, None) is ranked


# --- 4. Export carries everything a reader needs to reproduce the ranking ------------------

def test_export_records_measure_window_and_opens_in_excel():
    ranked = pd.DataFrame({'rank': [1], 'RPT Dist No': ['0161'], 'shoplifting_incidents': [59],
                           'robbery_incidents': [10], 'combined_incidents': [69]})
    raw = export_ranked_table(ranked, ['Central'], date(2025, 8, 1), date(2026, 7, 31), 'Robbery first')
    assert raw.startswith('\ufeff'.encode('utf-8'))           # BOM so Excel shows the en dash correctly
    exported = pd.read_csv(BytesIO(raw), dtype={'RPT Dist No': str})
    row = exported.iloc[0]
    assert row['RPT Dist No'] == '0161'                       # leading zero kept
    assert row['ranking_measure'] == 'Robbery first'
    assert row['evening_window'] == '18:00–24:00 (Time OCC)'
    assert (row['occurrence_start'], row['occurrence_end']) == ('2025-08-01', '2026-07-31')


# --- 5. Reporting periods: the label must match the dates (CR-13) --------------------------

def test_period_options_end_on_snapshot_end():
    periods = period_options(load_defaults())
    assert all(end == date(2026, 7, 31) for _, end in periods.values())
    twelve = next(v for k, v in periods.items() if k.startswith('Previous 12 months'))
    assert twelve == (date(2025, 8, 1), date(2026, 7, 31))


@pytest.mark.xfail(strict=True, reason='CR-13: "Most recent complete quarter" currently covers July 2026 only')
def test_most_recent_quarter_covers_three_months():
    periods = period_options(Defaults('Topanga', date(2025, 2, 1), date(2026, 7, 31)))
    start, end = next(v for k, v in periods.items() if k.startswith('Most recent complete quarter'))
    months = (end.year - start.year) * 12 + end.month - start.month + 1
    assert months == 3


# --- 6. Invariants over every selection a user can make -----------------------------------

from src.rank import RANKING_MEASURES
from src.setup import AREAS

PERIODS = list(period_options(load_defaults()).values())


@pytest.mark.parametrize('area', AREAS)
def test_invariants_for_every_area_period_and_measure(offenses, area):
    """For all 21 Areas x 3 periods x 3 measures (189 screens):
    combined = shoplifting + robbery; counts are whole and non-negative; at most 10 rows, ranked 1..n;
    rows sorted by the selected measure; districts in the top 10 are unique; the top-10 counts never
    exceed the Area total shown above them."""
    for start, end in PERIODS:
        rows = filter_offenses(offenses, area, start, end)
        area_total = len(rows)
        for measure, keys in RANKING_MEASURES.items():
            ranked = rank_districts(rows, k=10, measure=measure)
            assert len(ranked) <= 10 and ranked['rank'].tolist() == list(range(1, len(ranked) + 1))
            assert (ranked['combined_incidents'] == ranked['shoplifting_incidents'] + ranked['robbery_incidents']).all()
            assert (ranked[['shoplifting_incidents', 'robbery_incidents']] >= 0).all().all()
            assert ranked['RPT Dist No'].is_unique
            assert ranked['combined_incidents'].sum() <= area_total
            sort_key = ranked['shoplifting_incidents'] + 3 * ranked['robbery_incidents'] if keys[0] == 'priority_score' else ranked[keys[0]]
            assert sort_key.is_monotonic_decreasing


# --- 7. Cross-check: the same Area totals found another way (SQL, not pandas) -------------

def test_area_totals_match_independent_sql(offenses):
    """Recount every Area's evening shoplifting/robbery with SQLite over the raw columns,
    using string comparisons on Time OCC and date arithmetic in SQL, and compare with the app."""
    import sqlite3
    con = sqlite3.connect(':memory:')
    table = offenses[['AREA NAME', 'NIBR Code', 'Time OCC']].assign(day=offenses['Date OCC'].dt.strftime('%Y-%m-%d'))
    table.to_sql('offenses', con, index=False)
    for start, end in PERIODS:
        sql = '''SELECT "AREA NAME",
                        SUM("NIBR Code" = '23C'), SUM("NIBR Code" = '120'), COUNT(*)
                 FROM offenses
                 WHERE "NIBR Code" IN ('23C', '120') AND "Time OCC" BETWEEN '1800' AND '2359'
                   AND day BETWEEN ? AND ?
                 GROUP BY "AREA NAME"'''
        expected = {name: (s, r, c) for name, s, r, c in con.execute(sql, (start.isoformat(), end.isoformat()))}
        app = summarize_areas(offenses, start, end)
        for _, row in app.iterrows():
            got = (row['shoplifting_incidents'], row['robbery_incidents'], row['combined_incidents'])
            assert got == expected.get(row['AREA NAME'], (0, 0, 0)), (row['AREA NAME'], start, end)

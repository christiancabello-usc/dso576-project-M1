from datetime import date
import pandas as pd
from pandas.testing import assert_frame_equal
from src.filter import filter_offenses

def test_boundaries_and_no_mutation():
    df = pd.DataFrame({'AREA NAME': ['Mission'] * 10 + ['Pacific'],
        'NIBR Code': ['23C'] * 9 + ['220', '120'],
        'Time OCC': ['1800','2359','1759','0000',None,'1860','1800','1800','1800','1800','1800'],
        'Date OCC': pd.to_datetime(['2025-02-01','2026-07-31 23:59:59','2025-03-01','2025-03-01','2025-03-01','2025-03-01',None,'2025-01-31','2026-08-01','2025-03-01','2025-03-01'], format='mixed')})
    before = df.copy(deep=True)
    result = filter_offenses(df, 'Mission', date(2025,2,1), date(2026,7,31))
    assert list(result.index) == [0, 1]
    empty = filter_offenses(df, 'Central', date(2025,2,1), date(2026,7,31))
    assert empty.empty and list(empty) == list(df)
    assert_frame_equal(df, before)

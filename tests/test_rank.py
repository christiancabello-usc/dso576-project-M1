from datetime import date
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from src.rank import rank_districts, summarize_areas, DISTRICT_COLUMNS

def test_rank_counts_ties_empty_and_input():
    df = pd.DataFrame({'RPT Dist No':['0101','0101','0101','0103','0102'], 'NIBR Code':['23C','23C','120','23C','23C']})
    before = df.copy(deep=True)
    result = rank_districts(df)
    assert result.values.tolist() == [[1,'0101',2,1,3],[2,'0102',1,0,1],[3,'0103',1,0,1]]
    assert rank_districts(df, 1).shape[0] == 1
    empty = rank_districts(df.iloc[:0])
    assert empty.empty and list(empty) == DISTRICT_COLUMNS
    assert_frame_equal(df, before)

def test_multi_area_and_weighted_ranking():
    df = pd.DataFrame({'AREA NAME':['Mission','Mission','Pacific','Pacific'],
                       'RPT Dist No':['0101','0101','1401','1401'],
                       'NIBR Code':['23C','23C','23C','120']})
    result = rank_districts(df, k=5, measure='Weighted (robbery × 3)', include_area=True)
    assert result.iloc[0]['AREA NAME'] == 'Pacific'
    assert result.iloc[0]['priority_score'] == 4

@pytest.mark.parametrize('k', [0,-1,'10',True,1.5,None])
def test_invalid_k(k):
    with pytest.raises(ValueError, match='k'):
        rank_districts(pd.DataFrame(), k)

def test_area_summary_includes_all_21_and_shared_filter():
    df = pd.DataFrame({'AREA NAME':['Mission','Mission','Pacific','Pacific'], 'NIBR Code':['23C','120','23C','120'], 'Time OCC':['1800','2359','1800','1759'], 'Date OCC':pd.to_datetime(['2025-02-01']*4)})
    result = summarize_areas(df, date(2025,2,1), date(2026,7,31))
    assert len(result) == 21
    assert result.iloc[0].tolist() == ['Mission',1,1,2]
    assert result.iloc[1].tolist() == ['Pacific',1,0,1]
    assert result.iloc[2]['AREA NAME'] == '77th Street'

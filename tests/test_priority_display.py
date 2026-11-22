"""R1.1: sparse counts stay visible without receiving priority emphasis."""
from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd
from pandas.testing import assert_frame_equal

from src.view import RED, GRAY, render_results


def test_priority_display_requires_five_combined_offenses_without_reranking():
    # Include the threshold boundary, sparse top-five rows, and a qualifying
    # count outside the top five (possible with robbery-first ranking).
    ranked = pd.DataFrame({
        'rank': [1, 2, 3, 4, 5, 6],
        'RPT Dist No': ['0101', '0102', '0103', '0104', '0105', '0106'],
        'shoplifting_incidents': [0, 0, 0, 0, 0, 5],
        'robbery_incidents': [6, 5, 4, 2, 1, 0],
        'combined_incidents': [6, 5, 4, 2, 1, 5],
    })
    before = ranked.copy(deep=True)
    summary = pd.DataFrame({'AREA NAME': ['Central'],
                            'shoplifting_incidents': [5],
                            'robbery_incidents': [18],
                            'combined_incidents': [23]})
    metadata = {'quality': {'input_rows': 23, 'distinct_AREA': 1,
                           'missing_Date_Rptd': 0, 'missing_Date_OCC': 0,
                           'missing_or_invalid_Time_OCC': 0},
                'download_date': '2026-09-08', 'source_url': 'https://example.org'}
    with patch('src.view.st') as screen:
        screen.columns.side_effect = [[MagicMock() for _ in range(3)],
                                      [MagicMock(), MagicMock()]]
        render_results(ranked, summary, ['Central'], date(2026, 7, 1),
                       date(2026, 7, 31), 'Robbery first', metadata, None)

    table = screen.dataframe.call_args.args[0]
    styles = table._compute().ctx
    highlighted = [any(key == 'background-color' for key, _ in styles.get((i, 0), []))
                   for i in range(len(ranked))]
    assert highlighted == [True, True, False, False, False, False]
    assert_frame_equal(table.data[before.columns], before)
    assert table.data['Evidence'].tolist() == ['', '', 'Limited evidence',
                                             'Limited evidence', 'Limited evidence', '']
    assert_frame_equal(ranked, before)

    chart = screen.altair_chart.call_args.args[0]
    spec = chart.to_dict()
    color = spec['encoding']['color']
    assert color['condition']['test'] == '((datum.rank <= 5) && (datum.combined_incidents >= 5))'
    assert color['condition']['value'] == RED
    assert color['value'] == GRAY
    assert_frame_equal(chart.data[before.columns], before)
    # Labels must be visible on the axis, not only discoverable in a tooltip.
    labels = chart.data[spec['encoding']['y']['field']].tolist()
    assert labels == ['0101', '0102', '0103 · Limited evidence',
                      '0104 · Limited evidence', '0105 · Limited evidence', '0106']
    assert spec['encoding']['y']['sort'] == labels
    explanation = ' '.join(call.args[0] for call in screen.markdown.call_args_list)
    assert 'five combined offenses' in explanation
    assert 'practical display rule' in explanation
    assert 'not a statistically validated risk threshold' in explanation

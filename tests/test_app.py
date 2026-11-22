from datetime import date
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest

from src.data import load_prepared
from src.setup import load_defaults
from src.view import export_ranked_table


def test_config_fits_full_snapshot():
    df, meta = load_prepared('data/processed/offenses.parquet', 'data/processed/metadata.json')
    assert 'Date OCC' in df and len(df) == meta['condensed_rows']
    assert meta['configuration_check']['end_month_complete']


def test_screen_supports_multi_area_ranking_and_export():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
    assert not app.exception
    assert app.multiselect[0].value == [load_defaults().default_area]
    app.multiselect[0].set_value(['Topanga', 'Mission']).run(timeout=30)
    assert not app.exception
    ranked = app.dataframe[-1].value
    assert len(ranked) == 10
    assert 'AREA NAME' in ranked
    exported = pd.read_csv(BytesIO(export_ranked_table(
        ranked, ['Topanga', 'Mission'], date(2026, 7, 1), date(2026, 9, 30), 'Combined offenses')))
    assert exported['applied_areas'].iloc[0] == 'Topanga; Mission'
    assert exported['occurrence_start'].iloc[0] == '2026-07-01'


def test_r3_2_shows_plain_labels_and_a_populated_area_tooltip():
    with patch('src.view.st.altair_chart') as charts:
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
    assert not app.exception
    area_tooltips = charts.call_args_list[0].args[0].to_dict()['encoding']['tooltip']
    assert [(item['field'], item['title']) for item in area_tooltips] == [
        ('AREA NAME', 'LAPD Area'), ('shoplifting_incidents', 'Shoplifting offenses'),
        ('robbery_incidents', 'Robbery offenses'), ('combined_incidents', 'Combined offenses')]
    ranked_chart = charts.call_args_list[1].args[0]
    ranked_tooltips = ranked_chart.to_dict()['encoding']['tooltip']
    assert [(item['field'], item['title']) for item in ranked_tooltips] == [
        ('rank', 'Rank'), ('LAPD Area', 'LAPD Area'),
        ('RPT Dist No', 'LAPD reporting district'),
        ('shoplifting_incidents', 'Shoplifting offenses'),
        ('robbery_incidents', 'Robbery offenses'),
        ('combined_incidents', 'Combined offenses'), ('Evidence', 'Evidence note')]
    assert set(ranked_chart.data['LAPD Area']) == {load_defaults().default_area}


def test_empty_result_renders():
    df, meta = load_prepared('data/processed/offenses.parquet', 'data/processed/metadata.json')
    with patch('src.data.load_prepared', return_value=(df.iloc[:0], meta)):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
    assert not app.exception
    assert any('No qualifying offenses' in item.value for item in app.info)

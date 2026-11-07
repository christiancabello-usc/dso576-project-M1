"""Run with: streamlit run app.py"""
from pathlib import Path
import streamlit as st
from src.data import load_prepared
from src.setup import load_defaults
from src.filter import filter_offenses
from src.rank import summarize_areas, rank_districts
from src.view import attach_candidate_stores, select_controls, render_results

ROOT = Path(__file__).resolve().parent

@st.cache_data(show_spinner=False)
def area_summary(offenses, start, end):
    return summarize_areas(offenses, start, end)

def main():
    defaults = load_defaults(ROOT / 'configs/default.toml')
    offenses, metadata = load_prepared(ROOT / 'data/processed/offenses.parquet', ROOT / 'data/processed/metadata.json')
    initial_areas = area_summary(offenses, defaults.start, defaults.end)
    selected, measure, start, end, mapping = select_controls(defaults, initial_areas)
    if not selected:
        st.stop()
    areas = area_summary(offenses, start, end)
    combined = len(selected) > 1
    districts = rank_districts(filter_offenses(offenses, selected, start, end),
                               k=5 if combined else 10, measure=measure,
                               include_area=combined or mapping is not None)
    render_results(attach_candidate_stores(districts, mapping), areas, selected, start, end,
                   measure, metadata, mapping)

if __name__ == '__main__':
    main()

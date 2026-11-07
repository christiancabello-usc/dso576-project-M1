"""All screen rendering and exports, without recomputing offense counts."""
from datetime import date, datetime
from io import BytesIO
from zoneinfo import ZoneInfo

import altair as alt
import pandas as pd
import streamlit as st

from src.rank import RANKING_MEASURES
from src.setup import Defaults

CAPTION = 'Reported offenses, not actual crime. Evening = 18:00–24:00. January 2025 occurrence period excluded.'
RED = '#b5122b'
GRAY = '#a6adb7'
MAPPING_COLUMNS = ['store_id', 'store_name', 'address', 'area_name', 'rpt_dist_no']


def period_options(defaults: Defaults) -> dict[str, tuple[date, date]]:
    """Offer fixed, reproducible periods bounded by the snapshot's complete end month."""
    end = defaults.end
    quarter_start_month = ((end.month - 1) // 3) * 3 + 1
    quarter_start = date(end.year, quarter_start_month, 1)
    twelve_month_start = date(end.year - 1, end.month % 12 + 1, 1)
    return {
        f'Most recent complete quarter ({quarter_start:%b}–{end:%b %Y})': (quarter_start, end),
        f'Previous 12 months ({twelve_month_start:%b %Y}–{end:%b %Y})': (twelve_month_start, end),
        f'Full available period ({defaults.start:%b %Y}–{end:%b %Y})': (defaults.start, end),
    }


def read_store_mapping(uploaded) -> pd.DataFrame | None:
    if uploaded is None:
        return None
    mapping = pd.read_csv(BytesIO(uploaded.getvalue()), dtype='string')
    missing = set(MAPPING_COLUMNS).difference(mapping.columns)
    if missing:
        raise ValueError(f'Store mapping is missing columns: {", ".join(sorted(missing))}')
    mapping = mapping[MAPPING_COLUMNS].copy()
    mapping['area_name'] = mapping['area_name'].str.strip()
    mapping['rpt_dist_no'] = mapping['rpt_dist_no'].str.strip().str.zfill(4)
    return mapping.dropna(subset=['area_name', 'rpt_dist_no'])


def select_controls(defaults: Defaults, area_summary: pd.DataFrame) -> tuple[list[str], str, date, date, pd.DataFrame | None]:
    st.set_page_config(page_title='CVS | Evening Loss Prevention', page_icon='🔴', layout='wide')
    st.markdown('''<style>
    .stApp {background-color:#fafafa;} h1 {letter-spacing:-.035em;}
    [data-testid="stSidebar"] {background-color:#f1f2f4;}
    [data-testid="stSidebar"] h2 {font-size:1.2rem;}
    .block-container {padding-top:3.5rem;padding-bottom:1rem;}
    </style>''', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown('**CVS HEALTH** · LOS ANGELES')
        st.header('Evening allocation')
        options = sorted(area_summary['AREA NAME'].tolist())
        selected = st.multiselect('LAPD Areas', options, default=[defaults.default_area],
                                  help='Choose one Area for its top 10, or several Areas for one combined top-five shortlist.')
        if not selected:
            st.warning('Select at least one LAPD Area.')
        periods = period_options(defaults)
        period_label = st.selectbox('Reporting period', list(periods))
        start, end = periods[period_label]
        measure = st.selectbox('Ranking measure', list(RANKING_MEASURES),
                               help='Weighted ranking counts each robbery as three offense points.')
        st.caption(f'Occurrence dates: {start:%b %d, %Y} – {end:%b %d, %Y}')
        st.subheader('CVS store mapping')
        uploaded = st.file_uploader('Optional verified store mapping (CSV)', type='csv',
                                    help='Columns: store_id, store_name, address, area_name, rpt_dist_no.')
        mapping = None
        if uploaded is None:
            st.caption('Without a verified mapping, the app cannot recommend individual CVS stores or calculate offenses per CVS store.')
        else:
            try:
                mapping = read_store_mapping(uploaded)
                st.success(f'{len(mapping):,} mapped CVS stores loaded.')
            except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
                st.error(f'Mapping not used: {error}')
        st.subheader('Area comparison')
        st.caption('All 21 Areas · raw combined reported offenses')
        chart = alt.Chart(area_summary).mark_bar(color=GRAY, cornerRadiusEnd=2).encode(
            x=alt.X('combined_incidents:Q', title='Combined offenses', axis=alt.Axis(tickCount=3)),
            y=alt.Y('AREA NAME:N', sort=area_summary['AREA NAME'].tolist(), title=None,
                    axis=alt.Axis(labelOverlap=False, labelFontSize=10)),
            color=alt.condition(alt.FieldOneOfPredicate(field='AREA NAME', oneOf=selected), alt.value(RED), alt.value(GRAY)),
            tooltip=['AREA NAME:N', 'shoplifting_incidents:Q', 'robbery_incidents:Q', 'combined_incidents:Q']
        ).properties(height=430).configure_view(strokeWidth=0)
        st.altair_chart(chart, width='stretch')
        st.caption(CAPTION)
    return selected, measure, start, end, mapping


def attach_candidate_stores(ranked: pd.DataFrame, mapping: pd.DataFrame | None) -> pd.DataFrame:
    if mapping is None or ranked.empty:
        return ranked
    candidates = mapping.groupby(['area_name', 'rpt_dist_no'], dropna=False).agg(
        candidate_store_count=('store_id', 'nunique'),
        candidate_stores=('store_name', lambda names: '; '.join(names.dropna().astype(str).unique()))
    ).reset_index().rename(columns={'area_name': 'AREA NAME', 'rpt_dist_no': 'RPT Dist No'})
    return ranked.merge(candidates, on=['AREA NAME', 'RPT Dist No'], how='left').assign(
        candidate_store_count=lambda rows: rows['candidate_store_count'].fillna(0).astype(int),
        candidate_stores=lambda rows: rows['candidate_stores'].fillna('No verified CVS store mapped')
    )


def export_ranked_table(ranked: pd.DataFrame, selected_areas: list[str], start: date, end: date, measure: str) -> bytes:
    exported = ranked.copy()
    for key, value in {
        'applied_areas': '; '.join(selected_areas), 'occurrence_start': start.isoformat(),
        'occurrence_end': end.isoformat(), 'evening_window': '18:00–24:00 (Time OCC)',
        'offense_codes': '23C; 120', 'ranking_measure': measure,
        'exclusion_note': 'January 2025 occurrence reporting break excluded',
        'export_date': datetime.now(ZoneInfo('America/Los_Angeles')).date().isoformat(),
    }.items():
        exported[key] = value
    return exported.to_csv(index=False).encode('utf-8-sig')


def render_results(ranked: pd.DataFrame, area_summary: pd.DataFrame, selected_areas: list[str],
                   start: date, end: date, measure: str, metadata: dict,
                   mapping: pd.DataFrame | None) -> None:
    st.title('Evening Loss-Prevention Navigator')
    selected_summary = area_summary.loc[area_summary['AREA NAME'].isin(selected_areas)]
    scope = selected_areas[0] if len(selected_areas) == 1 else f'Combined ranking · {", ".join(selected_areas)}'
    st.subheader(f'{scope} · district priorities')
    st.caption(f'{start:%b %d, %Y} – {end:%b %d, %Y} · Occurrence date · Shoplifting 23C + robbery 120')
    metric_columns = st.columns(3)
    metric_columns[0].metric('Shoplifting offenses', int(selected_summary['shoplifting_incidents'].sum()))
    metric_columns[1].metric('Robbery offenses', int(selected_summary['robbery_incidents'].sum()))
    metric_columns[2].metric('Combined offenses', int(selected_summary['combined_incidents'].sum()))
    if mapping is None:
        st.warning('No verified CVS store mapping is loaded. Raw Area totals are not store-level risk or offenses per CVS store, and no individual store recommendation can be made.')
    else:
        store_counts = mapping.groupby('area_name')['store_id'].nunique().rename('mapped_CVS_stores')
        exposure = selected_summary.join(store_counts, on='AREA NAME').fillna({'mapped_CVS_stores': 0})
        exposure['offenses_per_mapped_CVS_store'] = exposure['combined_incidents'].div(exposure['mapped_CVS_stores'].replace(0, pd.NA))
        st.dataframe(exposure[['AREA NAME', 'combined_incidents', 'mapped_CVS_stores', 'offenses_per_mapped_CVS_store']],
                     hide_index=True, width='stretch',
                     column_config={'combined_incidents': 'Raw combined offenses', 'mapped_CVS_stores': 'Mapped CVS stores',
                                    'offenses_per_mapped_CVS_store': st.column_config.NumberColumn('Offenses per mapped CVS store', format='%.2f')})
    top_count = 10 if len(selected_areas) == 1 else 5
    st.markdown(f'**Red marks the first five priority districts** · ordered by **{measure.lower()}**. Counts are charged offense rows, not distinct reports.')
    left, right = st.columns([1.15, 1], gap='large')
    with left:
        st.markdown(f'**Top {top_count} reporting districts**')
        styled = ranked.style.apply(lambda row: ['background-color:#fce7eb;color:#85152a;font-weight:600' if row['rank'] <= 5 else '' for _ in row], axis=1)
        config = {'rank': st.column_config.NumberColumn('Rank', format='%d'), 'RPT Dist No': st.column_config.TextColumn('RPT Dist No'),
                  'shoplifting_incidents': st.column_config.NumberColumn('Shoplifting offenses', format='%d'),
                  'robbery_incidents': st.column_config.NumberColumn('Robbery offenses', format='%d'),
                  'combined_incidents': st.column_config.NumberColumn('Combined offenses', format='%d'),
                  'priority_score': st.column_config.NumberColumn('Weighted priority score', format='%d')}
        st.dataframe(styled, hide_index=True, width='stretch', height=390, column_config=config)
        st.caption(CAPTION)
        st.download_button('Download ranked CSV', export_ranked_table(ranked, selected_areas, start, end, measure),
                           file_name=f'evening_priorities_{"_".join(area.lower().replace(" ", "_") for area in selected_areas)}_{end}.csv',
                           mime='text/csv', disabled=ranked.empty, type='primary')
    with right:
        st.markdown('**Evening reported offenses**')
        if ranked.empty:
            st.info('No qualifying offenses for the selected Areas and occurrence-date window.')
        else:
            y = alt.Y('RPT Dist No:N', sort=ranked['RPT Dist No'].tolist(), title='RPT Dist No')
            chart = alt.Chart(ranked).mark_bar(cornerRadiusEnd=3).encode(
                y=y, x=alt.X('combined_incidents:Q', title='Combined reported offenses'),
                color=alt.condition(alt.datum.rank <= 5, alt.value(RED), alt.value(GRAY)),
                tooltip=[alt.Tooltip('rank:Q', title='Rank'), 'AREA NAME:N', 'RPT Dist No:N',
                         'shoplifting_incidents:Q', 'robbery_incidents:Q', 'combined_incidents:Q']
            ).properties(height=350).configure_view(strokeWidth=0)
            st.altair_chart(chart, width='stretch')
        st.caption(CAPTION)
    quality = metadata['quality']
    st.caption(f"Source: LAPD NIBRS · downloaded {metadata['download_date']} · {quality['input_rows']:,} unique charged-offense rows · {quality['distinct_AREA']} Areas")
    with st.expander('Methodology & data quality'):
        st.markdown(f"""[City of Los Angeles · LAPD NIBRS offenses]({metadata['source_url']}). Counts represent **charged offense rows**, not distinct reports, actual crime, CVS incidents, or store-level risk. Occurrence date and time determine inclusion. Local Los Angeles clock time is assumed.

Districts sort by the selected measure, then use documented offense-count tie breakers. With several Areas selected, the five rows are one combined cross-Area shortlist. Missing districts cannot be ranked.

Full-source quality: **{quality['missing_Date_Rptd']:,}** missing/invalid report dates; **{quality['missing_Date_OCC']:,}** missing/invalid occurrence dates; **{quality['missing_or_invalid_Time_OCC']:,}** missing/invalid times. Missing occurrence dates and times are excluded. No missing values are imputed.

January 2025 is excluded by the configured full-period start. Recent months may be incomplete. There is no store count, foot traffic, loss amount, or causal evidence of a guard's impact. Use verified store data and local knowledge before assignments.""")

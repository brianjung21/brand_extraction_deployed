from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

INPUT_PATH = Path("data/pivoted_brand_counts.csv")
START_DATE = '2025-08-24'
END_DATE = '2025-08-31'

st.set_page_config(page_title="Brand Mentions (Weekly)", layout='wide')

df = pd.read_csv(INPUT_PATH, encoding='utf-8')
df['date'] = pd.to_datetime(df['date'])
week = df[(df['date'] >= START_DATE) & (df['date'] <= END_DATE)].copy()

drop_cols = [c for c in ['date', 'total_mentions', 'num_brands_mentioned'] if c in week.columns]
brand_cols = [c for c in week.columns if c not in drop_cols]
week[brand_cols] = week[brand_cols].fillna(0)

st.title("Brand Mentions per Day (Weekly)")
st.caption(f"Window: {START_DATE} -> {END_DATE}")

totals = week[brand_cols].sum().sort_values(ascending=False)
default_brands = list(totals.head(5).index)

selected = st.multiselect("Pick brands to plot",
                          options=brand_cols,
                          default=default_brands)

if not selected:
    st.info("Select at least one brand to display the plot.")
else:
    long_df = week[['date'] + selected].melt(id_vars="date", var_name='brand', value_name='mentions')
    fig = px.line(
        long_df,
        x='date',
        y='mentions',
        color='brand',
        markers=True,
        title='Daily Mentions for Selected Brands'
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='Mentions', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show data table"):
        st.dataframe(long_df.sort_values(["brand", "date"]).reset_index(drop=True))

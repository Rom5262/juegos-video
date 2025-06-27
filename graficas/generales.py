
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def duracion_plataformas(df):
    if st.button("📈 Ver duración de plataformas"):
        plataforma = df.copy()
        if 'platform' in plataforma.columns and 'year_of_release' in plataforma.columns:
            active = plataforma.groupby("platform")["year_of_release"].agg(["min", "max"])
            active["year_activity"] = active["max"] - active["min"]
            data = active.reset_index().sort_values(by="year_activity", ascending=False)

            fig = px.line(
                data.sort_values(by='min'),
                x="min",
                y="year_activity",
                color="platform",
                markers=True,
                labels={
                    "min": "Año de lanzamiento",
                    "year_activity": "Duración (años)",
                    "platform": "Plataforma"
                },
                title="Duración de cada plataforma",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(xaxis_range=[1980, 2016], yaxis_range=[0, 20])
            st.plotly_chart(fig, use_container_width=True)

def plataformas_activas_por_anio(df):
    if st.button("📊 Ver plataformas activas por año"):
        plataformas = df.groupby('year_of_release')['platform'].nunique().reset_index()
        plataformas.columns = ['year', 'unique_platforms']

        fig = px.line(
            plataformas,
            x='year',
            y='unique_platforms',
            markers=True,
            labels={'year': 'Año', 'unique_platforms': 'Plataformas activas'},
            title='Cantidad de plataformas activas por año',
            color_discrete_sequence=['blue']
        )
        fig.update_layout(xaxis_title='Año', yaxis_title='Cantidad', xaxis=dict(dtick=1))
        st.plotly_chart(fig, use_container_width=True)

def top_plataformas(df):
    df = df.copy()
    df['total_sales'] = df[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum(axis=1)
    top_df = df.groupby('platform')['total_sales'].sum().reset_index()
    top10 = top_df.sort_values(by='total_sales', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top10['platform'], top10['total_sales'], color='skyblue')
    ax.set_title('Top 10 Plataformas por Ventas Totales')
    ax.set_xlabel('Plataforma')
    ax.set_ylabel('Ventas Totales (millones)')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)
    
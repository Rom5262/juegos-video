import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Duración de plataformas", layout="wide")
st.title("📊 Duración de plataformas en la industria de videojuegos")

if st.button("Ver gráfico de plataformas", key="btn_duracion_platform"):
    df = pd.read_csv("games.csv")
    df.columns = [col.lower() for col in df.columns]  

    if 'platform' in df.columns and 'year_of_release' in df.columns:
        platform_active = df.groupby("platform")["year_of_release"].agg(["min", "max"])
        platform_active["year_activity"] = platform_active["max"] - platform_active["min"]
        platform_durability = platform_active.reset_index().sort_values(by="year_activity", ascending=False)

        fig = px.line(
            platform_durability.sort_values(by='min'),
            x="min",
            y="year_activity",
            color="platform",
            markers=True,
            labels={
                "min": "Año de lanzamiento",
                "year_activity": "Duración (años)",
                "platform": "Plataforma"
            },
            title="Duración de cada plataforma en la industria",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            xaxis_range=[1980, 2016],
            yaxis_range=[0, 20],
            legend_title_text="Plataformas"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("El archivo no contiene las columnas necesarias: 'platform' y 'year_of_release'.")


import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(layout="wide")
st.title("🎮 Análisis de la industria de los videojuegos")

# Cargar y preparar el DataFrame
df = pd.read_csv("games.csv")
df.columns = [col.lower() for col in df.columns]

# 🔹 Gráfico: Plataformas activas por año
with st.expander("🔹 Plataformas activas por año"):
    if st.button("Ver gráfico de plataformas activas"):
        platforms_by_year = df.groupby('year_of_release')['platform'].nunique().reset_index()
        platforms_by_year.columns = ['year', 'unique_platforms']

        fig = px.line(
            platforms_by_year,
            x='year',
            y='unique_platforms',
            markers=True,
            labels={
                'year': 'Año de lanzamiento',
                'unique_platforms': 'Número de plataformas activas'
            },
            title='Cantidad de plataformas activas por año',
            color_discrete_sequence=['blue']
        )

        fig.update_layout(
            xaxis_title='Año',
            yaxis_title='Cantidad de plataformas',
            xaxis=dict(dtick=1),
            yaxis_range=[0, platforms_by_year['unique_platforms'].max() + 1]
        )

        st.plotly_chart(fig, use_container_width=True)

        
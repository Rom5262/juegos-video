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


st.set_page_config(layout="wide")
st.title("🎮 Análisis de la industria de los videojuegos")


df = pd.read_csv("games.csv")
df.columns = [col.lower() for col in df.columns]


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


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ventas Wii", layout="wide")
st.title("🎮 Ventas Totales por Año para Wii")

if st.button("Ver gráfico de ventas Wii", key="grafico_wii_final_v3"):
    df = pd.read_csv("games.csv")
    df.columns = [col.lower() for col in df.columns]
    df['platform'] = df['platform'].str.lower()

    df['total_sales'] = (
        df['na_sales'] +
        df['eu_sales'] +
        df['jp_sales'] +
        df['other_sales']
    )

    wii = df[df['platform'] == 'wii'].copy()
    wii = wii.dropna(subset=['year_of_release'])
    wii['year_of_release'] = wii['year_of_release'].astype(int)

    wii_sales = wii.groupby('year_of_release')['total_sales'].sum().reset_index()

    # Verifica si hay datos antes de graficar
    if wii_sales.empty:
        st.warning("⚠️ El DataFrame está vacío. No hay datos para graficar.")
    else:
        st.write("🔎 Vista previa de datos agregados:", wii_sales)

        fig = px.line(
            wii_sales,
            x='year_of_release',
            y='total_sales',
            title='Ventas Totales por Año para Wii',
            labels={'year_of_release': 'Año', 'total_sales': 'Ventas Totales (millones)'},
            markers=True,
            color_discrete_sequence=['royalblue']
        )

        fig.update_layout(
            xaxis_title='Año',
            yaxis_title='Ventas Totales',
            xaxis_range=[2005, 2016],
            template='simple_white'
        )

        st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Visualización de Ventas", layout="wide")
st.title("🎮 Análisis de Ventas de Videojuegos")

# =======================
# 📦 
# =======================
df = pd.read_csv("games.csv")
df.columns = [col.lower() for col in df.columns]
df['platform'] = df['platform'].str.lower()

df['total_sales'] = (
    df['na_sales'] +
    df['eu_sales'] +
    df['jp_sales'] +
    df['other_sales']
)

df = df.dropna(subset=['year_of_release'])
df['year_of_release'] = df['year_of_release'].astype(int)

# ===============================
# 🧪 Comparador de plataformas
# ===============================
st.markdown("---")
st.markdown("## 🧠 Comparador de Ventas por Plataforma")

plataformas = sorted(df['platform'].unique())
seleccion = st.selectbox("Selecciona una plataforma:", plataformas, key="selector_plataforma")

df_filtrado = df[df['platform'] == seleccion]

if df_filtrado.empty:
    st.warning(f"No hay datos para la plataforma '{seleccion}'.")
else:
    ventas = df_filtrado.groupby('year_of_release')['total_sales'].sum().reset_index()

    fig = px.line(
        ventas,
        x='year_of_release',
        y='total_sales',
        title=f"Ventas Totales por Año - {seleccion.upper()}",
        labels={'year_of_release': 'Año', 'total_sales': 'Ventas Totales (millones)'},
        markers=True,
        color_discrete_sequence=['indigo']
    )
    fig.update_layout(template="simple_white")
    st.plotly_chart(fig, use_container_width=True)



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Top Plataformas", layout="wide")
st.title("🎮 Ventas Totales por Plataforma (Top 10)")


df = pd.read_csv("games.csv")
df.columns = [col.lower() for col in df.columns]
df['platform'] = df['platform'].str.lower()

df['total_sales'] = (
    df['na_sales'] +
    df['eu_sales'] +
    df['jp_sales'] +
    df['other_sales']
)


total_sales_platform = df.groupby('platform')['total_sales'].sum().reset_index()
top_platforms = total_sales_platform.sort_values(by='total_sales', ascending=False).head(10)['platform'].tolist()

df_top = df[df['platform'].isin(top_platforms)]
sales_by_platform = df_top.groupby('platform')['total_sales'].sum().sort_values(ascending=False)


fig, ax = plt.subplots(figsize=(10, 6))
sales_by_platform.plot(kind='bar', ax=ax, color='skyblue')

ax.set_title('Ventas Totales por Plataforma (Top 10)', fontsize=16)
ax.set_xlabel('Plataforma', fontsize=12)
ax.set_ylabel('Ventas Totales (millones)', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=45)

st.pyplot(fig)

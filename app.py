
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Dashboard de Videojuegos", layout="wide")
st.title("🎮 Dashboard de Videojuegos")


@st.cache_data
def cargar_datos():
    df = pd.read_csv("games.csv")
    df.columns = [col.lower() for col in df.columns]
    return df

df = cargar_datos()



def duracion_plataformas(df):
    st.subheader("Duración de plataformas activas")
    duracion = df.groupby('platform')['year_of_release'].agg(['min', 'max'])
    duracion['duración'] = duracion['max'] - duracion['min']
    duracion = duracion.sort_values('duración', ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=duracion, x=duracion.index, y="duración", palette="viridis", ax=ax)
    ax.set_title("Top plataformas por años activos")
    ax.set_ylabel("Años activos")
    ax.set_xlabel("Plataforma")
    st.pyplot(fig)

def plataformas_activas_por_anio(df):
    st.subheader("Plataformas activas por año")
    df_activo = df.dropna(subset=['year_of_release'])
    conteo = df_activo.groupby('year_of_release')['platform'].nunique()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=conteo, marker="o", ax=ax)
    ax.set_title("Cantidad de plataformas activas por año")
    ax.set_ylabel("Número de plataformas")
    ax.set_xlabel("Año")
    st.pyplot(fig)

def top_plataformas(df):
    st.subheader("Top plataformas por ventas totales")
    df["total_sales"] = df[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum(axis=1)
    ventas = df.groupby("platform")["total_sales"].sum().sort_values(ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=ventas.values, y=ventas.index, palette="coolwarm", ax=ax)
    ax.set_title("Plataformas con mayores ventas")
    ax.set_xlabel("Ventas (millones)")
    ax.set_ylabel("Plataforma")
    st.pyplot(fig)

def comparar_ventas_por_plataforma(df):
    st.subheader("Ventas por región según plataforma")
    plataformas = df['platform'].dropna().unique()
    seleccion = st.selectbox("Elige una plataforma", sorted(plataformas))

    filtro = df[df['platform'] == seleccion]
    columnas = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    ventas = filtro[columnas].sum()

    fig, ax = plt.subplots(figsize=(8, 5))
    ventas.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title(f"Ventas totales en regiones para {seleccion}")
    ax.set_ylabel("Millones")
    st.pyplot(fig)

def comparador_estadistico_ventas(df):
    st.subheader("Comparador de ventas entre plataformas")
    opciones = sorted(df['platform'].dropna().unique())
    p1 = st.selectbox("Plataforma A", opciones, index=0)
    p2 = st.selectbox("Plataforma B", opciones, index=1)

    columnas = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    datos = df[df['platform'].isin([p1, p2])]
    resumen = datos.groupby('platform')[columnas].sum().T

    fig, ax = plt.subplots(figsize=(10, 5))
    resumen.plot(kind='bar', ax=ax)
    ax.set_title("Comparador de ventas por región")
    ax.set_ylabel("Millones de unidades")
    st.pyplot(fig)


modulo = st.sidebar.radio("Selecciona módulo", ["Generales", "Ventas"])

if modulo == "Generales":
    opcion = st.sidebar.selectbox("Análisis general", [
        "Duración de plataformas",
        "Plataformas activas por año",
        "Top plataformas por ventas"
    ])
    if opcion == "Duración de plataformas":
        duracion_plataformas(df)
    elif opcion == "Plataformas activas por año":
        plataformas_activas_por_anio(df)
    else:
        top_plataformas(df)

else:
    opcion = st.sidebar.selectbox("Análisis de ventas", [
        "Ventas por plataforma",
        "Comparador estadístico"
    ])
    if opcion == "Ventas por plataforma":
        comparar_ventas_por_plataforma(df)
    else:
        comparador_estadistico_ventas(df)

        
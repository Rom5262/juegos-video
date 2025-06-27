import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def comparar_ventas_por_plataforma(df):
    plataformas = sorted(df['platform'].unique())
    seleccion = st.selectbox("🎮 Selecciona una plataforma:", plataformas)

    df_filtrado = df[df['platform'] == seleccion]
    if df_filtrado.empty:
        st.warning(f"No hay datos para {seleccion}")
        return

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

def comparador_estadistico_ventas(df):
    plataformas = sorted(df['platform'].unique())
    seleccionadas = st.multiselect("📦 Plataformas a comparar:", plataformas, default=plataformas[:5])
    if not seleccionadas:
        st.warning("Selecciona al menos una plataforma.")
        return

    df_filtro = df[df['platform'].isin(seleccionadas)]
    limite = st.slider("Limitar juegos con ventas hasta:", 0.0, float(df_filtro['total_sales'].max()), 5.0, step=0.1)
    df_filtro = df_filtro[df_filtro['total_sales'] <= limite]

    if df_filtro.empty:
        st.warning("No hay datos que cumplan los filtros seleccionados.")
        return

    tipo = st.radio("Tipo de gráfico:", ["Histograma", "Boxplot", "KDE", "Violinplot"])
    plt.figure(figsize=(10, 6))

    if tipo == "Histograma":
        sns.histplot(data=df_filtro, x="total_sales", hue="platform", multiple="stack", binwidth=0.5)
    elif tipo == "Boxplot":
        sns.boxplot(data=df_filtro, x="platform", y="total_sales")
    elif tipo == "KDE":
        sns.kdeplot(data=df_filtro, x="total_sales", hue="platform", fill=True)
    elif tipo == "Violinplot":
        sns.violinplot(data=df_filtro, x="platform", y="total_sales", inner="quartile")

    plt.title(f"Ventas Totales por Plataforma ({tipo})")
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    st.pyplot(plt.gcf())
    
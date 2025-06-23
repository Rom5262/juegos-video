import pandas as pd
import plotly.express as px
import streamlit as st
import os


st.header('🎮 Top 10 plataformas por ventas totales de videojuegos')


ruta_csv = os.path.join(os.path.dirname(__file__), 'games.csv')

try:
    df = pd.read_csv(ruta_csv, encoding='utf-8')
    st.write("Archivo CSV cargado correctamente.")
    st.write("Columnas disponibles:", df.columns.tolist())
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV: {e}")


grafico_button = st.button('Mostrar gráfico de ventas')

if grafico_button:
    st.write('Mostrando las 10 plataformas con más ventas totales')

    total_sales_platform = df.groupby('platform')['total_sales'].sum().reset_index()
    total_sales_platform = total_sales_platform.sort_values(by='total_sales', ascending=False)

  
    top_10 = total_sales_platform.head(10)


    fig = px.bar(
        top_10,
        x='platform',
        y='total_sales',
        title='Top 10 plataformas por ventas totales',
        labels={'platform': 'Plataforma', 'total_sales': 'Ventas totales (millones)'},
        color='total_sales',
        color_continuous_scale='blues'
    )

   
    st.plotly_chart(fig, use_container_width=True)



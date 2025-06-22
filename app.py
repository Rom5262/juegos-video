import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.header('🎮 Duración de actividad por plataforma de videojuegos')

ruta_csv = os.path.join(os.path.dirname(__file__), 'games.csv')
df = pd.read_csv(ruta_csv, encoding='utf-8')  


df = df.dropna(subset=['platform', 'year_of_release'])


if st.button('Mostrar gráfico de duración'):

    # Agrupar por plataforma y calcular años de actividad
    platform_active = df.groupby('platform')['year_of_release'].agg(['min', 'max'])
    platform_active['duración'] = platform_active['max'] - platform_active['min']
    platform_active = platform_active.reset_index().sort_values(by='duración', ascending=True)

    
    fig = px.bar(
        platform_active,
        x='duración',
        y='platform',
        orientation='h',
        title='Duración de actividad por plataforma',
        labels={'duración': 'Años activos', 'platform': 'Plataforma'},
        color='duración',
        color_continuous_scale='turbo'
    )

    st.plotly_chart(fig, use_container_width=True)

import pandas as pd
import plotly.express as px
import streamlit as st


st.title('Análisis de la duración de plataformas de videojuegos')


df = pd.read_csv('games.csv')  

platform_active = df.groupby('platform')['year_of_release'].agg(year_start='min', year_end='max')
platform_active['year_activity'] = platform_active['year_end'] - platform_active['year_start']
platform_durability = platform_active.sort_values(by='year_start').reset_index()


if st.checkbox('Mostrar tabla de duraciones'):
    st.dataframe(platform_durability)


if st.button('Visualizar duración de plataformas'):
    st.write('Duración de cada plataforma en la industria del videojuego')
    fig = px.line(
        platform_durability,
        x='year_start',
        y='year_activity',
        color='platform',
        markers=True,
        labels={
            'year_start': 'Año de lanzamiento',
            'year_activity': 'Años de actividad',
            'platform': 'Plataforma'
        },
        title='Duración de plataformas en la industria'
    )
    fig.update_layout(xaxis_range=[1980, 2016], yaxis_range=[0, 20])
    st.plotly_chart(fig, use_container_width=True)
    
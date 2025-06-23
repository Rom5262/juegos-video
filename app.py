import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv('games.csv')  

platform_active = df.groupby('platform')['year_of_release'].agg(['min', 'max'])
platform_active['year_activity'] = platform_active['max'] - platform_active['min']
platform_durability = platform_active.reset_index()


platform_durability = platform_durability.sort_values(by='year_activity', ascending=False)


st.title("Duración de plataformas en la industria de videojuegos")


if st.button('Mostrar gráfico interactivo'):
    st.write("Visualización de los años de actividad de cada plataforma")

   
    fig = px.line(
        platform_durability.sort_values(by='min'),
        x='min',
        y='year_activity',
        color='platform',
        markers=True,
        labels={
            'min': 'Año de lanzamiento',
            'year_activity': 'Duración (años)',
            'platform': 'Plataforma'
        },
        title='Duración de cada plataforma en la industria',
        color_discrete_sequence=px.colors.qualitative.Set2  # Paleta más amigable
    )

   
    fig.update_layout(
        xaxis_range=[1980, 2016],
        yaxis_range=[0, 20],
        legend_title_text='Plataformas'
    )

    st.plotly_chart(fig, use_container_width=True)
    

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Este archivo contiene todas las funciones para generar los diferentes gráficos.

# Gráfico de duración de plataformas activas
def duracion_plataformas(df_filtered):
    st.subheader("Duración de plataformas activas")
    # Agrupa por plataforma y calcula el año mínimo y máximo de lanzamiento
    duracion = df_filtered.groupby('platform')['year_of_release'].agg(['min', 'max'])
    # Calcula la duración restando el año mínimo del máximo
    duracion['duración'] = duracion['max'] - duracion['min']
    # Ordena y selecciona las 15 plataformas principales por duración
    duracion = duracion.sort_values('duración', ascending=False).head(15)

    # Crea el gráfico de barras usando Matplotlib y Seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    # FIX: Se añade hue=duracion.index y legend=False para evitar FutureWarning
    sns.barplot(data=duracion, x=duracion.index, y="duración", palette="viridis", ax=ax, hue=duracion.index, legend=False)
    ax.set_title("Top plataformas por años activos")
    ax.set_ylabel("Años activos")
    ax.set_xlabel("Plataforma")
    # Muestra el gráfico en Streamlit
    st.pyplot(fig)

# Gráfico de plataformas activas por año
def plataformas_activas_por_anio(df_filtered):
    st.subheader("Plataformas activas por año")
    # Cuenta el número único de plataformas por año de lanzamiento
    conteo = df_filtered.groupby('year_of_release')['platform'].nunique()

    # Crea el gráfico de línea
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=conteo, marker="o", ax=ax)
    ax.set_title("Cantidad de plataformas activas por año")
    ax.set_ylabel("Número de plataformas")
    ax.set_xlabel("Año")
    st.pyplot(fig)

# Gráfico de top plataformas por ventas totales
def top_plataformas(df_filtered):
    st.subheader("Top plataformas por ventas totales")
    # Agrupa por plataforma y suma las ventas totales, luego selecciona las 15 principales
    ventas = df_filtered.groupby("platform")["total_sales"].sum().sort_values(ascending=False).head(15)

    # Crea el gráfico de barras horizontales
    fig, ax = plt.subplots(figsize=(10, 6))
    # FIX: Se añade hue=ventas.index y legend=False para evitar FutureWarning
    sns.barplot(x=ventas.values, y=ventas.index, palette="coolwarm", ax=ax, hue=ventas.index, legend=False)
    ax.set_title("Plataformas con mayores ventas")
    ax.set_xlabel("Ventas (millones)")
    ax.set_ylabel("Plataforma")
    st.pyplot(fig)

# Gráfico para comparar ventas por región de una plataforma seleccionada
def comparar_ventas_por_plataforma(df_filtered):
    st.subheader("Ventas por región según plataforma")
    # Obtiene todas las plataformas únicas y las ordena
    plataformas = df_filtered['platform'].dropna().unique()
    seleccion = st.selectbox("Elige una plataforma", sorted(plataformas))

    # Filtra los datos por la plataforma seleccionada
    filtro = df_filtered[df_filtered['platform'] == seleccion]
    # Columnas de ventas por región
    columnas = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    # Suma las ventas por región para la plataforma filtrada
    ventas = filtro[columnas].sum()

    # Crea el gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 5))
    ventas.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title(f"Ventas totales en regiones para {seleccion}")
    ax.set_ylabel("Millones")
    st.pyplot(fig)

# Gráfico para comparar ventas entre dos plataformas seleccionadas
def comparador_estadistico_ventas(df_filtered):
    st.subheader("Comparador de ventas entre plataformas")
    # Obtiene opciones para las dos plataformas a comparar
    opciones = sorted(df_filtered['platform'].dropna().unique())
    # Manejo de índices para evitar errores si hay menos de 2 plataformas
    p1_index = 0 if len(opciones) > 0 else None
    p2_index = 1 if len(opciones) > 1 else (0 if len(opciones) == 1 else None)

    p1 = st.selectbox("Plataforma A", opciones, index=p1_index) if p1_index is not None else None
    p2 = st.selectbox("Plataforma B", opciones, index=p2_index) if p2_index is not None else None

    if p1 is None or p2 is None:
        st.warning("Selecciona al menos dos plataformas para comparar.")
        return

    columnas = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    # Filtra los datos para ambas plataformas
    datos = df_filtered[df_filtered['platform'].isin([p1, p2])]
    # Agrupa por plataforma y suma las ventas por región, luego transpone el resultado
    resumen = datos.groupby('platform')[columnas].sum().T

    # Crea el gráfico de barras comparativo
    fig, ax = plt.subplots(figsize=(10, 5))
    resumen.plot(kind='bar', ax=ax)
    ax.set_title("Comparador de ventas por región")
    ax.set_ylabel("Millones de unidades")
    st.pyplot(fig)

# Función para la distribución de ventas por plataforma (Histograma/Violin Plot/Box Plot) con selección múltiple
def distribucion_ventas_por_plataforma(df_filtered):
    st.subheader("Distribución de Ventas por Plataforma para Comparación")

    # Dropdown para seleccionar el tipo de gráfico
    tipo_grafico = st.selectbox(
        "Selecciona el tipo de gráfico",
        ("Violin Plot", "Box Plot", "Histograma"),
        key="platform_sales_chart_type"
    )

    # Obtiene las plataformas únicas y las ordena para el dropdown de selección múltiple
    plataformas_disponibles = sorted(df_filtered['platform'].dropna().unique())
    
    # Selecciona las plataformas por defecto para mostrar alguna comparación
    default_platforms = []
    if len(plataformas_disponibles) >= 2:
        default_platforms = [plataformas_disponibles[0], plataformas_disponibles[1]]
    elif len(plataformas_disponibles) == 1:
        default_platforms = [plataformas_disponibles[0]]

    plataformas_seleccionadas = st.multiselect(
        "Selecciona una o varias plataformas para comparar",
        plataformas_disponibles,
        default=default_platforms
    )

    # Verifica si se ha seleccionado al menos una plataforma
    if not plataformas_seleccionadas:
        st.warning("Por favor, selecciona al menos una plataforma para visualizar su distribución de ventas.")
        return

    # Filtra los datos para las plataformas seleccionadas
    df_plataforma_filtrada = df_filtered[df_filtered['platform'].isin(plataformas_seleccionadas)]

    # Verifica si hay datos para las plataformas seleccionadas en el rango de años
    if df_plataforma_filtrada.empty:
        st.warning(f"No hay datos de ventas para las plataformas seleccionadas en el rango de años actual. Por favor, elige otras plataformas o ajusta el rango de años.")
        return

    # Crea el gráfico
    fig, ax = plt.subplots(figsize=(12, 7))

    if tipo_grafico == "Violin Plot":
        # Crea un violin plot de las ventas totales para las plataformas seleccionadas
        # FIX: Se añade hue='platform' y legend=False para evitar FutureWarning
        sns.violinplot(x='platform', y='total_sales', data=df_plataforma_filtrada, palette='viridis', ax=ax, hue='platform', legend=False)
        ax.set_title("Distribución de Ventas Totales por Plataforma (Violin Plot)")
        ax.set_xlabel("Plataforma")
        ax.set_ylabel("Ventas Totales (millones)")
        ax.set_ylim(bottom=0)

    elif tipo_grafico == "Box Plot":
        # Crea un box plot de las ventas totales para las plataformas seleccionadas
        # FIX: Se añade hue='platform' y legend=False para evitar FutureWarning
        sns.boxplot(x='platform', y='total_sales', data=df_plataforma_filtrada, palette='plasma', ax=ax, hue='platform', legend=False)
        ax.set_title("Distribución de Ventas Totales por Plataforma (Box Plot)")
        ax.set_xlabel("Plataforma")
        ax.set_ylabel("Ventas Totales (millones)")
        ax.set_ylim(bottom=0)

    elif tipo_grafico == "Histograma":
        # Para histogramas, superponerlos con transparencia para comparar
        ax.set_title("Histograma de Ventas Totales por Plataforma")
        ax.set_xlabel("Ventas Totales (millones)")
        ax.set_ylabel("Frecuencia")
        
        # Iterar sobre las plataformas seleccionadas y trazar su histograma
        for platform in plataformas_seleccionadas:
            data_to_plot = df_plataforma_filtrada[df_plataforma_filtrada['platform'] == platform]['total_sales']
            sns.histplot(data_to_plot, kde=True, ax=ax, label=platform, alpha=0.5, bins=30)
        ax.legend(title="Plataformas")
        ax.set_ylim(bottom=0)

    st.pyplot(fig)


# Nueva función para comparar ventas de un mismo videojuego en diferentes plataformas
def comparar_ventas_por_juego_y_plataforma(df_filtered):
    st.subheader("Comparación de Ventas por Videojuego y Plataforma")

    # Obtener la lista de videojuegos únicos con al menos 2 plataformas disponibles en el df filtrado
    # Agrupar por nombre de juego y contar las plataformas únicas
    juegos_multiplataforma = df_filtered.groupby('name')['platform'].nunique()
    # Filtrar solo los juegos que aparecen en más de una plataforma
    juegos_con_comparacion = juegos_multiplataforma[juegos_multiplataforma > 1].index.tolist()
    juegos_con_comparacion.sort() # Ordenar alfabéticamente

    if not juegos_con_comparacion:
        st.warning("No hay videojuegos con ventas en múltiples plataformas en el rango de años seleccionado para comparar.")
        return

    # Selector para elegir un videojuego
    juego_seleccionado = st.selectbox(
        "Selecciona un videojuego para comparar sus ventas entre plataformas",
        juegos_con_comparacion
    )

    # Filtrar el DataFrame para el juego seleccionado
    df_juego_filtrado = df_filtered[df_filtered['name'] == juego_seleccionado]

    # Agrupar las ventas totales por plataforma para el juego seleccionado
    ventas_por_plataforma_juego = df_juego_filtrado.groupby('platform')['total_sales'].sum().reset_index()
    
    if ventas_por_plataforma_juego.empty:
        st.warning(f"No hay datos de ventas para '{juego_seleccionado}' en el rango de años actual.")
        return

    # Crear el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    # FIX: Se añade hue='platform' y legend=False para evitar FutureWarning
    sns.barplot(x='platform', y='total_sales', data=ventas_por_plataforma_juego, palette='viridis', ax=ax, hue='platform', legend=False)
    ax.set_title(f"Ventas Totales de '{juego_seleccionado}' por Plataforma")
    ax.set_xlabel("Plataforma")
    ax.set_ylabel("Ventas Totales (millones)")
    ax.set_ylim(bottom=0) # Asegura que el eje Y comience en 0
    st.pyplot(fig)


# Función para la distribución de ventas por género en las Top 10 plataformas
# Ahora con selección de tipo de gráfico (Boxplot, Violin Plot, Histograma)
def distribucion_ventas_por_genero_top_plataformas(df_filtered):
    st.subheader("Distribución de Ventas por Género en Top 10 Plataformas")

    # Selector para el tipo de gráfico
    tipo_grafico = st.selectbox(
        "Selecciona el tipo de gráfico",
        ("Boxplot", "Violin Plot", "Histograma"),
        key="genre_sales_chart_type" # Añadir una key única es buena práctica en Streamlit
    )

    # Calcular las 10 plataformas con mayores ventas totales dentro del df_filtered actual
    top_10_platforms_series = df_filtered.groupby('platform')['total_sales'].sum().nlargest(10).index
    
    # Filtrar el DataFrame para incluir solo las Top 10 plataformas
    df_top_10 = df_filtered[df_filtered['platform'].isin(top_10_platforms_series)]

    if df_top_10.empty:
        st.warning("No hay datos disponibles para las Top 10 plataformas en el rango de años seleccionado.")
        return

    # Crear el gráfico basado en la selección del usuario
    fig, ax = plt.subplots(figsize=(14, 7))

    if tipo_grafico == "Boxplot":
        # FIX: Se añade hue='genre' y legend=False para evitar FutureWarning
        sns.boxplot(y='total_sales', x='genre', data=df_top_10, palette='viridis', ax=ax, hue='genre', legend=False)
        ax.set_title('Distribución de Ventas Totales por Género (Boxplot)', fontsize=16)
        ax.set_xlabel('Género', fontsize=12)
        ax.set_ylabel('Ventas Totales (millones)', fontsize=12)
        ax.set_ylim(bottom=0) # Asegura que el eje Y comience en 0 para ventas
        
    elif tipo_grafico == "Violin Plot":
        # FIX: Se añade hue='genre' y legend=False para evitar FutureWarning
        sns.violinplot(y='total_sales', x='genre', data=df_top_10, palette='plasma', ax=ax, hue='genre', legend=False)
        ax.set_title('Distribución de Ventas Totales por Género (Violin Plot)', fontsize=16)
        ax.set_xlabel('Género', fontsize=12)
        ax.set_ylabel('Ventas Totales (millones)', fontsize=12)
        ax.set_ylim(bottom=0) # Asegura que el eje Y comience en 0 para ventas

    elif tipo_grafico == "Histograma":
        ax.set_title('Histograma de Ventas Totales por Género', fontsize=16)
        ax.set_xlabel('Ventas Totales (millones)', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        
        genres_in_data = df_top_10['genre'].unique()
        for genre in sorted(genres_in_data): # Ordenar para consistencia
            data_to_plot = df_top_10[df_top_10['genre'] == genre]['total_sales']
            # Evitar errores si un género tiene pocos datos después del filtro de top_10
            if not data_to_plot.empty:
                sns.histplot(data_to_plot, kde=True, ax=ax, label=genre, alpha=0.5, bins=30)
        ax.legend(title="Géneros", bbox_to_anchor=(1.05, 1), loc='upper left') # Mueve la leyenda fuera del gráfico
        plt.tight_layout() # Asegura que la leyenda no se corte
        ax.set_ylim(bottom=0)

    plt.xticks(rotation=45, ha='right') # Rota las etiquetas del eje X para evitar superposición
    plt.tight_layout() # Ajusta el layout para que las etiquetas y la leyenda no se corten
    
    st.pyplot(fig)


# Nueva función unificada para el análisis de ventas por región y género
def analisis_ventas_por_region_y_genero(df_filtered):
    st.subheader("Análisis de Ventas por Región y Género")

    # Selector de región de ventas
    region_options = {
        "Ventas Globales": "total_sales",
        "Ventas Norteamérica (NA)": "na_sales",
        "Ventas Europa (EU)": "eu_sales",
        "Ventas Japón (JP)": "jp_sales",
        "Otras Ventas": "other_sales"
    }
    selected_region_display = st.selectbox(
        "Selecciona la región de ventas",
        list(region_options.keys()),
        key="sales_region_selector"
    )
    selected_region_column = region_options[selected_region_display]

    # Selector del tipo de análisis/gráfico
    chart_type = st.radio(
        "Selecciona el tipo de análisis",
        ["Top Géneros por Ventas", "Ventas Acumuladas por Género"],
        key="genre_analysis_type"
    )

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # Gráfico 1: Top Géneros por Ventas en la Región Seleccionada
    if chart_type == "Top Géneros por Ventas":
        st.write(f"### Top Géneros por {selected_region_display}")
        
        # Agrupar por género y sumar las ventas de la región seleccionada
        genre_sales = df_filtered.groupby('genre')[selected_region_column].sum().sort_values(ascending=False)

        if genre_sales.empty:
            st.info(f"No hay datos de ventas para géneros en {selected_region_display} para el rango de años seleccionado.")
            return

        # Seleccionar el número de géneros a mostrar (por ejemplo, los 15 principales)
        top_n_genres = st.slider("Mostrar Top N Géneros", 5, len(genre_sales), 15, key="top_genres_slider")
        top_genres = genre_sales.head(top_n_genres)

        fig, ax = plt.subplots(figsize=(12, 7))
        # FIX: Se añade hue=top_genres.index y legend=False para evitar FutureWarning
        sns.barplot(x=top_genres.values, y=top_genres.index, palette='magma', ax=ax, hue=top_genres.index, legend=False)
        ax.set_title(f'Top {top_n_genres} Géneros por {selected_region_display}', fontsize=16)
        ax.set_xlabel(f'Ventas ({selected_region_display.replace("Ventas ", "")}) en Millones', fontsize=12)
        ax.set_ylabel('Género', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)

    # Gráfico 2: Ventas Acumuladas por Género a lo largo del tiempo (Línea)
    elif chart_type == "Ventas Acumuladas por Género":
        st.write(f"### Evolución de Ventas por Género en {selected_region_display}")
        
        # Seleccionar géneros para comparar (multiselect)
        all_genres = sorted(df_filtered['genre'].dropna().unique().tolist())
        selected_genres_for_line = st.multiselect(
            "Selecciona géneros para comparar su evolución (máximo 5)",
            all_genres,
            default=all_genres[:3] if len(all_genres) >= 3 else all_genres, # Selecciona 3 por defecto
            max_selections=5,
            key="selected_genres_line_chart"
        )

        if not selected_genres_for_line:
            st.info("Por favor, selecciona al menos un género para el análisis de ventas acumuladas.")
            return
        
        # Filtrar datos por los géneros seleccionados
        df_filtered_genres = df_filtered[df_filtered['genre'].isin(selected_genres_for_line)]
        
        if df_filtered_genres.empty:
            st.warning("No hay datos para los géneros seleccionados en el rango de años actual.")
            return

        # Agrupar por año de lanzamiento y género, sumando las ventas de la región
        sales_over_time = df_filtered_genres.groupby(['year_of_release', 'genre'])[selected_region_column].sum().reset_index()

        fig, ax = plt.subplots(figsize=(14, 7))
        sns.lineplot(
            data=sales_over_time, 
            x='year_of_release', 
            y=selected_region_column, 
            hue='genre', 
            marker='o', 
            ax=ax
        )
        ax.set_title(f'Evolución de Ventas por Género en {selected_region_display}', fontsize=16)
        ax.set_xlabel('Año de Lanzamiento', fontsize=12)
        ax.set_ylabel(f'Ventas ({selected_region_display.replace("Ventas ", "")}) en Millones', fontsize=12)
        ax.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left') # Mueve la leyenda
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)


# Función para la tendencia de ventas de las Top 5 Plataformas en Norteamérica
def tendencia_ventas_top_na_plataformas(df_filtered):
    st.subheader("Tendencia de Ventas de las Top 5 Plataformas en Norteamérica")

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # 1. Calcular las Top 5 plataformas por ventas totales en Norteamérica
    na_sales_platform = df_filtered.groupby('platform')['na_sales'].sum().reset_index()
    na_sales_platform = na_sales_platform.sort_values(by='na_sales', ascending=False).head(5)
    
    top_na_platforms_names = na_sales_platform['platform'].tolist()

    if not top_na_platforms_names:
        st.info("No se encontraron Top 5 plataformas con ventas en Norteamérica para el rango de años seleccionado.")
        return

    # 2. Filtrar el DataFrame para incluir solo los juegos de esas Top 5 plataformas
    top_na_platforms_data = df_filtered[df_filtered['platform'].isin(top_na_platforms_names)]
    sales_trend = top_na_platforms_data.groupby(['year_of_release', 'platform'])['na_sales'].sum().reset_index()

    if sales_trend.empty:
        st.info("No hay datos de tendencia para las Top 5 plataformas en Norteamérica en el rango de años seleccionado.")
        return

    # Crear el gráfico de línea
    fig, ax = plt.subplots(figsize=(12, 7))

    for platform in sales_trend['platform'].unique():
        platform_data = sales_trend[sales_trend['platform'] == platform]
        ax.plot(platform_data['year_of_release'], 
                platform_data['na_sales'], label=platform, marker='o', linewidth=2)

    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas en Norteamérica (millones de USD)', fontsize=12)
    ax.set_title('Tendencia de Ventas de las Top 5 Plataformas en Norteamérica', fontsize=16)
    
    # Rango fijo de años para este gráfico
    ax.set_xlim(2000, 2016) 
    
    ax.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)


# Función para la tendencia de ventas de las Top 5 Plataformas en la Unión Europea
def tendencia_ventas_top_eu_plataformas(df_filtered):
    st.subheader("Tendencia de Ventas de las Top 5 Plataformas en la Unión Europea")

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # 1. Calcular las Top 5 plataformas por ventas totales en la Unión Europea
    eu_sales_platform = df_filtered.groupby('platform')['eu_sales'].sum().reset_index()
    eu_sales_platform = eu_sales_platform.sort_values(by='eu_sales', ascending=False).head(5)
    
    top_eu_platforms_names = eu_sales_platform['platform'].tolist()

    if not top_eu_platforms_names:
        st.info("No se encontraron Top 5 plataformas con ventas en la Unión Europea para el rango de años seleccionado.")
        return

    # 2. Filtrar el DataFrame para incluir solo los juegos de esas Top 5 plataformas
    top_eu_platforms_data = df_filtered[df_filtered['platform'].isin(top_eu_platforms_names)]
    sales_trend = top_eu_platforms_data.groupby(['year_of_release', 'platform'])['eu_sales'].sum().reset_index()

    if sales_trend.empty:
        st.info("No hay datos de tendencia para las Top 5 plataformas en la Unión Europea en el rango de años seleccionado.")
        return

    # Crear el gráfico de línea
    fig, ax = plt.subplots(figsize=(12, 7))

    for platform in sales_trend['platform'].unique():
        platform_data = sales_trend[sales_trend['platform'] == platform]
        ax.plot(platform_data['year_of_release'], 
                platform_data['eu_sales'], label=platform, marker='o', linewidth=2)

    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas en Europa (millones de USD)', fontsize=12)
    ax.set_title('Tendencia de Ventas de las Top 5 Plataformas en la Unión Europea', fontsize=16)
    
    # Rango fijo de años para este gráfico
    ax.set_xlim(2000, 2016) 
    
    ax.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)


# Función para la tendencia de ventas de las Top 5 Plataformas en Japón
def tendencia_ventas_top_jp_plataformas(df_filtered):
    st.subheader("Tendencia de Ventas de las Top 5 Plataformas en Japón")

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # 1. Calcular las Top 5 plataformas por ventas totales en Japón
    jp_sales_platform = df_filtered.groupby('platform')['jp_sales'].sum().reset_index()
    jp_sales_platform = jp_sales_platform.sort_values(by='jp_sales', ascending=False).head(5)
    
    top_jp_platforms_names = jp_sales_platform['platform'].tolist()

    if not top_jp_platforms_names:
        st.info("No se encontraron Top 5 plataformas con ventas en Japón para el rango de años seleccionado.")
        return

    # 2. Filtrar el DataFrame para incluir solo los juegos de esas Top 5 plataformas
    top_jp_platforms_data = df_filtered[df_filtered['platform'].isin(top_jp_platforms_names)]
    sales_trend = top_jp_platforms_data.groupby(['year_of_release', 'platform'])['jp_sales'].sum().reset_index()

    if sales_trend.empty:
        st.info("No hay datos de tendencia para las Top 5 plataformas en Japón en el rango de años seleccionado.")
        return

    # Crear el gráfico de línea
    fig, ax = plt.subplots(figsize=(12, 7))

    for platform in sales_trend['platform'].unique():
        platform_data = sales_trend[sales_trend['platform'] == platform]
        ax.plot(platform_data['year_of_release'], 
                platform_data['jp_sales'], label=platform, marker='o', linewidth=2)

    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas en Japón (millones de USD)', fontsize=12)
    ax.set_title('Tendencia de Ventas de las Top 5 Plataformas en Japón', fontsize=16)
    
    # Rango fijo de años para este gráfico
    ax.set_xlim(1995, 2016) 
    
    ax.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)


# Función para la tendencia de ventas de los Top 5 Géneros en Norteamérica
def tendencia_ventas_top_na_generos(df_filtered):
    st.subheader("Tendencia de Ventas de los Top 5 Géneros en Norteamérica")

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # 1. Calcular los Top 5 géneros por ventas totales en Norteamérica
    na_main_genres = df_filtered.groupby('genre')['na_sales'].sum().reset_index()
    na_main_genres = na_main_genres.sort_values(by='na_sales', ascending=False).head(5)
    
    top_na_genres_names = na_main_genres['genre'].tolist()

    if not top_na_genres_names:
        st.info("No se encontraron Top 5 géneros con ventas en Norteamérica para el rango de años seleccionado.")
        return

    # 2. Filtrar el DataFrame para incluir solo los juegos de esos Top 5 géneros
    top_na_genres_data = df_filtered[df_filtered['genre'].isin(top_na_genres_names)]
    sales_trend = top_na_genres_data.groupby(['year_of_release', 'genre'])['na_sales'].sum().reset_index()

    if sales_trend.empty:
        st.info("No hay datos de tendencia para los Top 5 géneros en Norteamérica en el rango de años seleccionado.")
        return

    # Crear el gráfico de línea
    fig, ax = plt.subplots(figsize=(12, 7))

    for genre in sales_trend['genre'].unique():
        genre_data = sales_trend[sales_trend['genre'] == genre]
        ax.plot(genre_data['year_of_release'], 
                genre_data['na_sales'], label=genre, marker='o', linewidth=2)

    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas en Norteamérica (millones de USD)', fontsize=12)
    ax.set_title('Tendencia de Ventas de los Top 5 Géneros en Norteamérica', fontsize=16)
    
    # Rango fijo de años para este gráfico
    ax.set_xlim(1985, 2016) 
    
    ax.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)


# Función para la tendencia de ventas de los Top 5 Géneros en Europa
def tendencia_ventas_top_eu_generos(df_filtered):
    st.subheader("Tendencia de Ventas de los Top 5 Géneros en Europa")

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # 1. Calcular los Top 5 géneros por ventas totales en Europa
    eu_main_genres = df_filtered.groupby('genre')['eu_sales'].sum().reset_index()
    eu_main_genres = eu_main_genres.sort_values(by='eu_sales', ascending=False).head(5)
    
    top_eu_genres_names = eu_main_genres['genre'].tolist()

    if not top_eu_genres_names:
        st.info("No se encontraron Top 5 géneros con ventas en Europa para el rango de años seleccionado.")
        return

    # 2. Filtrar el DataFrame para incluir solo los juegos de esos Top 5 géneros
    top_eu_genres_data = df_filtered[df_filtered['genre'].isin(top_eu_genres_names)]
    sales_trend = top_eu_genres_data.groupby(['year_of_release', 'genre'])['eu_sales'].sum().reset_index()

    if sales_trend.empty:
        st.info("No hay datos de tendencia para los Top 5 géneros en Europa en el rango de años seleccionado.")
        return

    # Crear el gráfico de línea
    fig, ax = plt.subplots(figsize=(12, 7))

    for genre in sales_trend['genre'].unique():
        genre_data = sales_trend[sales_trend['genre'] == genre]
        ax.plot(genre_data['year_of_release'], 
                genre_data['eu_sales'], label=genre, marker='o', linewidth=2)

    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas en Europa (millones de USD)', fontsize=12)
    ax.set_title('Tendencia de Ventas de los Top 5 Géneros en Europa', fontsize=16)
    
    # Rango fijo de años para este gráfico
    ax.set_xlim(1995, 2016) 
    
    ax.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)


# Función para la tendencia de ventas de los Top 5 Géneros en Japón
def tendencia_ventas_top_jp_generos(df_filtered):
    st.subheader("Tendencia de Ventas de los Top 5 Géneros en Japón")

    if df_filtered.empty:
        st.warning("No hay datos disponibles para el rango de años seleccionado.")
        return

    # 1. Calcular los Top 5 géneros por ventas totales en Japón
    jp_main_genres = df_filtered.groupby('genre')['jp_sales'].sum().reset_index()
    jp_main_genres = jp_main_genres.sort_values(by='jp_sales', ascending=False).head(5)
    
    top_jp_genres_names = jp_main_genres['genre'].tolist()

    if not top_jp_genres_names:
        st.info("No se encontraron Top 5 géneros con ventas en Japón para el rango de años seleccionado.")
        return

    # 2. Filtrar el DataFrame para incluir solo los juegos de esos Top 5 géneros
    top_jp_genres_data = df_filtered[df_filtered['genre'].isin(top_jp_genres_names)]
    sales_trend = top_jp_genres_data.groupby(['year_of_release', 'genre'])['jp_sales'].sum().reset_index()

    if sales_trend.empty:
        st.info("No hay datos de tendencia para los Top 5 géneros en Japón en el rango de años seleccionado.")
        return

    # Crear el gráfico de línea
    fig, ax = plt.subplots(figsize=(12, 7))

    for genre in sales_trend['genre'].unique():
        genre_data = sales_trend[sales_trend['genre'] == genre]
        # CORRECCIÓN AQUÍ: Cambiado 'platform_data' a 'genre_data'
        ax.plot(genre_data['year_of_release'], 
                genre_data['jp_sales'], label=genre, marker='o', linewidth=2)

    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas en Japón (millones de USD)', fontsize=12)
    ax.set_title('Tendencia de Ventas de los Top 5 Géneros en Japón', fontsize=16)
    
    # Rango fijo de años para este gráfico
    ax.set_xlim(1982, 2016) 
    
    ax.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)

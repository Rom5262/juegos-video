
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Este archivo contendrá todas las funciones para generar los diferentes gráficos.

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
    sns.barplot(data=duracion, x=duracion.index, y="duración", palette="viridis", ax=ax)
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
    sns.barplot(x=ventas.values, y=ventas.index, palette="coolwarm", ax=ax)
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
        ("Violin Plot", "Box Plot", "Histograma")
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
        sns.violinplot(x='platform', y='total_sales', data=df_plataforma_filtrada, palette='viridis', ax=ax)
        ax.set_title("Distribución de Ventas Totales por Plataforma (Violin Plot)")
        ax.set_xlabel("Plataforma")
        ax.set_ylabel("Ventas Totales (millones)")
        ax.set_ylim(bottom=0)

    elif tipo_grafico == "Box Plot":
        # Crea un box plot de las ventas totales para las plataformas seleccionadas
        sns.boxplot(x='platform', y='total_sales', data=df_plataforma_filtrada, palette='plasma', ax=ax)
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
    
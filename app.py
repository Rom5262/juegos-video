
import streamlit as st
import pandas as pd
# Ya no necesitamos importar matplotlib.pyplot y seaborn aquí
# porque están importados dentro de charts.py
# import matplotlib.pyplot as plt
# import seaborn as sns

# Importa todas las funciones de gráficos desde el archivo charts.py
from charts import (
    duracion_plataformas,
    plataformas_activas_por_anio,
    top_plataformas,
    comparar_ventas_por_plataforma,
    comparador_estadistico_ventas,
    distribucion_ventas_por_plataforma,
    comparar_ventas_por_juego_y_plataforma,
    distribucion_ventas_por_genero_top_plataformas, # Nueva importación para gráficos de distribución por género
    analisis_ventas_por_region_y_genero, # Nueva función unificada de ventas por región y género
    tendencia_ventas_top_na_plataformas, # Tendencia NA por plataforma
    tendencia_ventas_top_eu_plataformas, # Tendencia EU por plataforma
    tendencia_ventas_top_jp_plataformas, # Tendencia JP por plataforma
    tendencia_ventas_top_na_generos, # Tendencia NA por género
    tendencia_ventas_top_eu_generos, # Tendencia EU por género
    tendencia_ventas_top_jp_generos # Tendencia JP por género
)

# Configuración de la página de Streamlit
st.set_page_config(page_title="Dashboard de Videojuegos", layout="wide")
st.title("🎮 Dashboard de Videojuegos")

# Función para cargar y preprocesar los datos
# @st.cache_data decora la función para cachear los datos, mejorando el rendimiento
@st.cache_data
def cargar_datos():
    # Carga el archivo CSV
    df = pd.read_csv("games.csv")
    # Convierte los nombres de las columnas a minúsculas para facilitar el acceso
    df.columns = [col.lower() for col in df.columns]
    # Convierte 'year_of_release' a entero y maneja NaN.
    # Es importante hacer esto antes de filtrar por años, ya que el deslizador espera enteros.
    df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce')
    df = df.dropna(subset=['year_of_release']) # Elimina filas con NaN en year_of_release después de la conversión
    df['year_of_release'] = df['year_of_release'].astype(int)

    # Calcula las ventas totales sumando las ventas por región
    df["total_sales"] = df[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum(axis=1)
    return df

# Carga los datos al iniciar la aplicación
df = cargar_datos()

# --- Lógica principal de la aplicación con la barra lateral ---

# Rango de años en la barra lateral
# Asegúrate de que min_year y max_year existan y sean enteros antes de usarlos
if not df.empty and 'year_of_release' in df.columns:
    min_year = int(df['year_of_release'].min())
    max_year = int(df['year_of_release'].max())
else:
    min_year = 1980 # Valor por defecto si no hay datos de año
    max_year = 2020 # Valor por defecto si no hay datos de año
    st.warning("No se pudieron cargar los datos de años de lanzamiento. Usando rango de años predeterminado.")


st.sidebar.subheader("Filtrar por año de lanzamiento")
year_range = st.sidebar.slider(
    "Selecciona un rango de años",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year) # Valor inicial del slider
)

# Filtra el DataFrame completo basado en el rango de años seleccionado
df_filtered = df[(df['year_of_release'] >= year_range[0]) & (df['year_of_release'] <= year_range[1])]

if df_filtered.empty:
    st.warning("No hay datos para el rango de años seleccionado. Por favor, ajusta los filtros.")
else:
    # Selector de módulo en la barra lateral
    modulo = st.sidebar.radio("Selecciona módulo", ["Generales", "Ventas"])

    # Condicional para mostrar las opciones del módulo seleccionado
    if modulo == "Generales":
        opcion = st.sidebar.selectbox("Análisis general", [
            "Duración de plataformas",
            "Plataformas activas por año",
            "Top plataformas por ventas",
            "Distribución de ventas por plataforma para comparación",
            "Distribución de ventas por género en Top 10 Plataformas" # Nueva opción
        ])
        if opcion == "Duración de plataformas":
            duracion_plataformas(df_filtered)
        elif opcion == "Plataformas activas por año":
            plataformas_activas_por_anio(df_filtered)
        elif opcion == "Top plataformas por ventas":
            top_plataformas(df_filtered)
        elif opcion == "Distribución de ventas por plataforma para comparación":
            distribucion_ventas_por_plataforma(df_filtered)
        elif opcion == "Distribución de ventas por género en Top 10 Plataformas": # Nueva llamada
            distribucion_ventas_por_genero_top_plataformas(df_filtered)
    else: # Módulo de Ventas
        opcion = st.sidebar.selectbox("Análisis de ventas", [
            "Ventas por plataforma",
            "Comparador estadístico",
            "Comparar ventas por videojuego y plataforma",
            "Análisis de Ventas Regionales y por Género", # Nueva opción unificada
            "Tendencia de Ventas Top 5 NA Plataformas", # Nueva opción
            "Tendencia de Ventas Top 5 EU Plataformas", # Nueva opción
            "Tendencia de Ventas Top 5 JP Plataformas", # Nueva opción
            "Tendencia de Ventas Top 5 NA Géneros", # Nueva opción
            "Tendencia de Ventas Top 5 EU Géneros", # Nueva opción
            "Tendencia de Ventas Top 5 JP Géneros" # Nueva opción
        ])
        if opcion == "Ventas por plataforma":
            comparar_ventas_por_plataforma(df_filtered)
        elif opcion == "Comparador estadístico":
            comparador_estadistico_ventas(df_filtered)
        elif opcion == "Comparar ventas por videojuego y plataforma":
            comparar_ventas_por_juego_y_plataforma(df_filtered)
        elif opcion == "Análisis de Ventas Regionales y por Género": # Llamada a la nueva función unificada
            analisis_ventas_por_region_y_genero(df_filtered)
        elif opcion == "Tendencia de Ventas Top 5 NA Plataformas": # Llamada
            tendencia_ventas_top_na_plataformas(df_filtered)
        elif opcion == "Tendencia de Ventas Top 5 EU Plataformas": # Llamada
            tendencia_ventas_top_eu_plataformas(df_filtered)
        elif opcion == "Tendencia de Ventas Top 5 JP Plataformas": # Llamada
            tendencia_ventas_top_jp_plataformas(df_filtered)
        elif opcion == "Tendencia de Ventas Top 5 NA Géneros": # Llamada
            tendencia_ventas_top_na_generos(df_filtered)
        elif opcion == "Tendencia de Ventas Top 5 EU Géneros": # Llamada
            tendencia_ventas_top_eu_generos(df_filtered)
        elif opcion == "Tendencia de Ventas Top 5 JP Géneros": # Llamada
            tendencia_ventas_top_jp_generos(df_filtered)

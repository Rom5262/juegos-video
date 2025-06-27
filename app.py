
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    # Calcula las ventas totales sumando las ventas por región
    df["total_sales"] = df[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum(axis=1)
    return df

# Carga los datos al iniciar la aplicación
df = cargar_datos()

# --- Funciones para generar gráficos existentes ---

# Gráfico de duración de plataformas activas
def duracion_plataformas(df):
    st.subheader("Duración de plataformas activas")
    # Agrupa por plataforma y calcula el año mínimo y máximo de lanzamiento
    duracion = df.groupby('platform')['year_of_release'].agg(['min', 'max'])
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
def plataformas_activas_por_anio(df):
    st.subheader("Plataformas activas por año")
    # Elimina filas con valores nulos en 'year_of_release'
    df_activo = df.dropna(subset=['year_of_release'])
    # Cuenta el número único de plataformas por año de lanzamiento
    conteo = df_activo.groupby('year_of_release')['platform'].nunique()

    # Crea el gráfico de línea
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=conteo, marker="o", ax=ax)
    ax.set_title("Cantidad de plataformas activas por año")
    ax.set_ylabel("Número de plataformas")
    ax.set_xlabel("Año")
    st.pyplot(fig)

# Gráfico de top plataformas por ventas totales
def top_plataformas(df):
    st.subheader("Top plataformas por ventas totales")
    # Agrupa por plataforma y suma las ventas totales, luego selecciona las 15 principales
    ventas = df.groupby("platform")["total_sales"].sum().sort_values(ascending=False).head(15)

    # Crea el gráfico de barras horizontales
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=ventas.values, y=ventas.index, palette="coolwarm", ax=ax)
    ax.set_title("Plataformas con mayores ventas")
    ax.set_xlabel("Ventas (millones)")
    ax.set_ylabel("Plataforma")
    st.pyplot(fig)

# Gráfico para comparar ventas por región de una plataforma seleccionada
def comparar_ventas_por_plataforma(df):
    st.subheader("Ventas por región según plataforma")
    # Obtiene todas las plataformas únicas y las ordena
    plataformas = df['platform'].dropna().unique()
    seleccion = st.selectbox("Elige una plataforma", sorted(plataformas))

    # Filtra los datos por la plataforma seleccionada
    filtro = df[df['platform'] == seleccion]
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
def comparador_estadistico_ventas(df):
    st.subheader("Comparador de ventas entre plataformas")
    # Obtiene opciones para las dos plataformas a comparar
    opciones = sorted(df['platform'].dropna().unique())
    p1 = st.selectbox("Plataforma A", opciones, index=0) # Plataforma A
    p2 = st.selectbox("Plataforma B", opciones, index=1) # Plataforma B

    columnas = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    # Filtra los datos para ambas plataformas
    datos = df[df['platform'].isin([p1, p2])]
    # Agrupa por plataforma y suma las ventas por región, luego transpone el resultado
    resumen = datos.groupby('platform')[columnas].sum().T

    # Crea el gráfico de barras comparativo
    fig, ax = plt.subplots(figsize=(10, 5))
    resumen.plot(kind='bar', ax=ax)
    ax.set_title("Comparador de ventas por región")
    ax.set_ylabel("Millones de unidades")
    st.pyplot(fig)

# --- Nueva función para la distribución de ventas por plataforma (Histograma/Violin Plot) ---
def distribucion_ventas_por_plataforma(df):
    st.subheader("Distribución de Ventas por Plataforma")

    # Dropdown para seleccionar el tipo de gráfico
    tipo_grafico = st.selectbox(
        "Selecciona el tipo de gráfico",
        ("Histograma", "Violin Plot")
    )

    # Obtiene las plataformas únicas y las ordena para el dropdown
    plataformas_disponibles = sorted(df['platform'].dropna().unique())
    plataforma_seleccionada = st.selectbox(
        "Selecciona una plataforma",
        plataformas_disponibles
    )

    # Filtra los datos para la plataforma seleccionada
    df_filtrado = df[df['platform'] == plataforma_seleccionada]

    # Verifica si hay datos para la plataforma seleccionada
    if df_filtrado.empty:
        st.warning(f"No hay datos de ventas para la plataforma '{plataforma_seleccionada}'. Por favor, elige otra.")
        return

    # Crea el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    if tipo_grafico == "Histograma":
        # Crea un histograma de las ventas totales
        sns.histplot(df_filtrado['total_sales'], kde=True, ax=ax, color='skyblue', bins=30)
        ax.set_title(f"Histograma de Ventas Totales para {plataforma_seleccionada}")
        ax.set_xlabel("Ventas Totales (millones)")
        ax.set_ylabel("Frecuencia")
    elif tipo_grafico == "Violin Plot":
        # Crea un violin plot de las ventas totales
        sns.violinplot(y=df_filtrado['total_sales'], ax=ax, color='lightgreen')
        ax.set_title(f"Violin Plot de Ventas Totales para {plataforma_seleccionada}")
        ax.set_ylabel("Ventas Totales (millones)")
        ax.set_xlabel("") # No se necesita etiqueta en el eje X para un solo violín
    
    st.pyplot(fig)

# --- Lógica principal de la aplicación con la barra lateral ---

# Selector de módulo en la barra lateral
modulo = st.sidebar.radio("Selecciona módulo", ["Generales", "Ventas"])

# Condicional para mostrar las opciones del módulo seleccionado
if modulo == "Generales":
    opcion = st.sidebar.selectbox("Análisis general", [
        "Duración de plataformas",
        "Plataformas activas por año",
        "Top plataformas por ventas",
        "Distribución de ventas por plataforma" # Nueva opción
    ])
    if opcion == "Duración de plataformas":
        duracion_plataformas(df)
    elif opcion == "Plataformas activas por año":
        plataformas_activas_por_anio(df)
    elif opcion == "Top plataformas por ventas":
        top_plataformas(df)
    elif opcion == "Distribución de ventas por plataforma": # Llama a la nueva función
        distribucion_ventas_por_plataforma(df)
else: # Módulo de Ventas
    opcion = st.sidebar.selectbox("Análisis de ventas", [
        "Ventas por plataforma",
        "Comparador estadístico"
    ])
    if opcion == "Ventas por plataforma":
        comparar_ventas_por_plataforma(df)
    else:
        comparador_estadistico_ventas(df)
        

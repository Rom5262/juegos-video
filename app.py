
import streamlit as st
import pandas as pd

# Importar funciones de los módulos
from ventas import comparar_ventas_por_plataforma, comparador_estadistico_ventas
from generales import duracion_plataformas, plataformas_activas_por_anio, top_plataformas

# Cargar dataset
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos.csv")  # Reemplaza por la ruta de tu archivo real

df = cargar_datos()

# Interfaz principal
def main():
    st.set_page_config(page_title="Dashboard de Videojuegos", layout="wide")
    st.title("🎮 Dashboard de Videojuegos")

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

if __name__ == "__main__":
    main()

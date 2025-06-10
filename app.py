import streamlit as st
from streamlit_option_menu import option_menu
from cargar_datos import cargar_datos
from pregunta1 import mostrar_visualizacion_generos
from pregunta2 import mostrar_relacion_tecnologias_valoracion 
from pregunta3 import mostrar_visualizacion_impacto
from pregunta4 import mostrar_visualizacion_resenas
from pregunta5 import mostrar_visualizacion_gap
from pregunta6 import mostrar_exito_por_desarrollador


# Configuración de la página
st.set_page_config(page_title="Visualización Steam", layout="wide")

# Cargar datos
datos = cargar_datos()

with st.sidebar:
    selected = option_menu(
        "Navegación",  # título del menú
        [
            "Evolución por género y año",
            "Tecnologías vs valoración",
            "Picos de jugadores y reseñas",
            "Ratio de reseñas positivas",
            "Comportamiento de jugadores",
            "Éxito por desarrollador"
        ],
        icons=["bar-chart", "cpu", "activity", "percent", "file-person", "star"],
        menu_icon="cast", 
        default_index=0,
        orientation="vertical"
    )

# Mostrar visualización según la opción elegida
if selected == "Evolución por género y año":
    mostrar_visualizacion_generos(datos)
elif selected == "Tecnologías vs valoración":
    mostrar_relacion_tecnologias_valoracion(datos)
elif selected == "Picos de jugadores y reseñas":
    mostrar_visualizacion_impacto(datos)
elif selected == "Ratio de reseñas positivas":
    mostrar_visualizacion_resenas(datos)
elif selected == "Comportamiento de jugadores":
    mostrar_visualizacion_gap(datos)
elif selected == "Éxito por desarrollador":
    mostrar_exito_por_desarrollador(datos)
    

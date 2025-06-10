import streamlit as st
import pandas as pd
import altair as alt

# Visualización: Relación entre tecnologías utilizadas y valoración
@st.cache_data
def mostrar_relacion_tecnologias_valoracion(datos):
    st.title("Steam: Relación entre tecnologías utilizadas y valoración de los juegos")
    st.markdown("""
    Este apartado analiza si ciertos motores están asociados a mejores valoraciones.
    Para ello, se extraen tecnologías detectadas y se compara su valoración media. Se consideran las 15 tecnologías más utilizadas 
    """)

    # Filtro: Juegos que tienen tecnologías detectadas y ratio positivo válido
    juegos_con_tecnologia = datos[datos["detected_technologies"].notna() & (datos["positive_ratio"].notna())]

    # Separación: Expandir las tecnologías detectadas por juego
    filas_expandida = juegos_con_tecnologia.assign(
        tecnologia=juegos_con_tecnologia["detected_technologies"].str.split(",")
    ).explode("tecnologia")

    # Limpieza: Normalizar nombres de tecnologías
    filas_expandida["tecnologia"] = filas_expandida["tecnologia"].str.strip()

    # Agrupación: Valoración media por tecnología
    resumen_tecnologias = (
        filas_expandida.groupby("tecnologia")["positive_ratio"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "valoracion_media", "count": "n_juegos"})
    )

    # Filtro: Solo tecnologías con al menos 30 juegos
    resumen_filtrado = resumen_tecnologias[resumen_tecnologias["n_juegos"] >= 30]
    resumen_filtrado = resumen_filtrado.sort_values(by="valoracion_media", ascending=False).head(15)

    # Visualización: Barras horizontales con valoración media por tecnología
    grafico_barras = alt.Chart(resumen_filtrado).mark_bar().encode(
        x=alt.X("valoracion_media:Q", title="Valoración media (proporción positiva)"),
        y=alt.Y("tecnologia:N", sort="-x", title="Tecnología"),
        color=alt.Color("n_juegos:Q", scale=alt.Scale(scheme="blues"), title="Cantidad de juegos"),
        tooltip=["tecnologia", "valoracion_media", "n_juegos"]
    ).properties(
        width=800,
        height=600,
        title="Tecnologías más comunes y su valoración media"
    )

    st.altair_chart(grafico_barras, use_container_width=True)
import streamlit as st
import pandas as pd
import altair as alt

# Visualización: desarrolladores o publishers con mayor impacto
def mostrar_visualizacion_impacto(datos):
    st.title("Steam: Desarrolladores/Publishers más exitosos")
    st.markdown("""
    Esta sección analiza qué desarrolladores o publishers han logrado mayor pico de jugadores,
    y cómo se relaciona eso con su valoración promedio por parte del público. Se utilizan los 15 desarrolladores con mayor pico de jugadores
    """)

    # Filtro interactivo
    opcion = st.radio("Agrupar por:", ["Desarrollador", "Publisher"])
    campo = "developer" if opcion == "Desarrollador" else "publisher"

    # Diccionario para pluralizar correctamente
    plural = {"Desarrollador": "Desarrolladores", "Publisher": "Publishers"}

    # Agrupación
    resumen = (
        datos.dropna(subset=["positive_ratio", "all_time_peak", campo])
        .groupby(campo)
        .agg(
            pico_promedio=("all_time_peak", "mean"),
            valoracion_media=("positive_ratio", "mean"),
            cantidad_juegos=("game", "count")
        )
        .reset_index()
        .sort_values("pico_promedio", ascending=False)
        .head(15)
    )

    # Eje X ordenado
    resumen[campo] = resumen[campo].astype(str)

    # Escala compartida
    barras = alt.Chart(resumen).mark_bar(color="#1f77b4").encode(
        x=alt.X(f"{campo}:N", sort="-y", title=opcion),
        y=alt.Y("pico_promedio:Q", title="Pico promedio de jugadores"),
        tooltip=[campo, "pico_promedio", "valoracion_media", "cantidad_juegos"]
    )

    linea = alt.Chart(resumen).mark_line(color="orange", point=True).encode(
        x=alt.X(f"{campo}:N", sort="-y"),
        y=alt.Y("valoracion_media:Q", title="Valoración media", axis=alt.Axis(format="%")),
        tooltip=["valoracion_media"]
    )

    st.altair_chart((barras + linea).resolve_scale(y='independent').properties(
        width=900,
        height=500,
        title=f"{plural[opcion]} con mayor pico de jugadores y su valoración media"
    ), use_container_width=True)
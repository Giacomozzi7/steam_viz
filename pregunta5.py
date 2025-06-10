import streamlit as st
import altair as alt
import pandas as pd

@st.cache_data
def mostrar_visualizacion_gap(datos):
    st.title("Steam: Evolución de la pérdida de jugadores tras el pico histórico")
    st.markdown("""
    Esta visualización muestra cómo ha evolucionado el **player_activity_gap** 
    (diferencia entre el pico histórico y el pico de las últimas 24 h) a lo largo 
    de los años de lanzamiento de los juegos. El área sombreada indica el rango 
    intercuartílico (25º–75º percentil), y la línea la mediana de la pérdida de jugadores.
    """)

    # Filtrar valores válidos
    df = (
        datos
        .dropna(subset=["release_year", "player_activity_gap"])
        .query("player_activity_gap >= 0")  # opcional: excluir gaps negativos o erróneos
    )

    # Convertir release_year a categoría para un eje ordenado
    df["release_year"] = df["release_year"].astype(int).astype(str)

    # Base chart con agrupación por año
    base = alt.Chart(df).encode(
        x=alt.X("release_year:N", title="Año de lanzamiento")
    )

    # Banda intercuartílica
    band = base.mark_area(opacity=0.3, color="#72b7b2").transform_aggregate(
        q1="q1(player_activity_gap)",
        q3="q3(player_activity_gap)",
        groupby=["release_year"]
    ).encode(
        y=alt.Y("q1:Q", title="Player Activity Gap (jugadores)"),
        y2="q3:Q"
    )

    # Línea de la mediana
    line = base.mark_line(color="#4c78a8", size=3).transform_aggregate(
        median="median(player_activity_gap)",
        groupby=["release_year"]
    ).encode(
        y=alt.Y("median:Q", title="Player Activity Gap (mediana)")
    )

    chart = (band + line).properties(
        width=900,
        height=500,
        title="Evolución del player_activity_gap por año de lanzamiento"
    ).configure_axis(
        labelAngle=-45
    )

    st.altair_chart(chart, use_container_width=True)
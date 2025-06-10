import streamlit as st
import pandas as pd
import altair as alt

# Visualización: relación entre recepción y volumen de reseñas
def mostrar_visualizacion_resenas(datos):
    st.title("Steam: Reseñas y recepción de los juegos")
    st.markdown("""
    Esta sección examina la relación entre el volumen de reseñas y la percepción positiva.
    """)

    # Filtro
    juegos_filtrados = datos[(datos["total_reviews"] >= 50) & (datos["positive_ratio"].notna())]

    # Visualización adicional: distribución de positive_ratio
    histograma = alt.Chart(juegos_filtrados).mark_bar().encode(
        x=alt.X("positive_ratio:Q", bin=alt.Bin(maxbins=40), title="Proporción positiva"),
        y=alt.Y("count():Q", title="Número de juegos"),
        tooltip=[alt.Tooltip("count()", title="Juegos en bin")],
        color=alt.value("#72b7b2")
    ).properties(
        width=850,
        height=600,
        title="Distribución de valoraciones positivas"
    )

    st.altair_chart(histograma, use_container_width=True)
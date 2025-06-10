import streamlit as st
import altair as alt
import pandas as pd

@st.cache_data
def mostrar_exito_por_desarrollador(datos):
    st.title("Steam: Desarrolladores con éxito consistente")
    st.markdown("""
    Esta sección identifica a los estudios desarrolladores que han mantenido 
    una recepción positiva consistente a lo largo del tiempo. Para ello, se usa 
    la métrica `developer_success_score`, que representa el promedio de 
    `positive_ratio` de todos sus juegos. Se utiliza el top 15 de desarrolladores con mayor éxito sostenido (mínimo 5 juegos)
    """)

    # Filtrar y agrupar desarrolladores con al menos 5 juegos
    resumen = (
        datos.dropna(subset=["developer", "developer_success_score"])
        .groupby("developer")
        .agg(
            exito_promedio=("developer_success_score", "mean"),
            n_juegos=("game", "count")
        )
        .reset_index()
    )

    # Filtrar solo desarrolladores con 5 o más juegos
    resumen = resumen[resumen["n_juegos"] >= 5]

    # Top 20 por éxito promedio
    top = resumen.sort_values("exito_promedio", ascending=False).head(15)

    # Gráfico de barras horizontales
    grafico = alt.Chart(top).mark_bar().encode(
        y=alt.Y("developer:N", sort="-x", title="Desarrollador"),
        x=alt.X("exito_promedio:Q", title="Éxito promedio (positive_ratio)"),
        color=alt.Color("n_juegos:Q", scale=alt.Scale(scheme="greens"), title="Cantidad de juegos"),
        tooltip=["developer", "exito_promedio", "n_juegos"]
    ).properties(
        width=800,
        height=600,
        title="Desarrolladores con valoración positiva consistente"
    )

    st.altair_chart(grafico, use_container_width=True)
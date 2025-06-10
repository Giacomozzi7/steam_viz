import streamlit as st
import pandas as pd
import altair as alt

# Evaluación de lanzamientos por género
@st.cache_data
def mostrar_visualizacion_generos(datos):
    # Creación del título y descripción
    st.title("Steam: Evolución de lanzamientos por género y año")
    st.markdown("""
    Esta sección explora cómo han evolucionado los lanzamientos de videojuegos en Steam a lo largo de los años,
    centrándose en los principales géneros. Se consideran los 10 géneros más frecuentes en el conjunto de datos.
    """)

    # Creación de la tabla total de géneros
    juegos_filtrados = datos[(datos["primary_genre"].notna()) &
                             (~datos["primary_genre"].str.lower().isin(["unknown genre", "nan"]))]

    conteo_generos = juegos_filtrados["primary_genre"].value_counts().reset_index()
    conteo_generos.columns = ["Género", "Cantidad de juegos"]
    st.subheader("Cantidad total de juegos por género")
    st.dataframe(conteo_generos)

    # Selección de los 10 géneros más comunes
    top_generos = juegos_filtrados["primary_genre"].value_counts().head(10).index
    datos_top_generos = juegos_filtrados[juegos_filtrados["primary_genre"].isin(top_generos)]

    # Agrupación de datos por año y género
    datos_agregados = (
        datos_top_generos
        .groupby(["release_year", "primary_genre"])
        .size()
        .reset_index(name="Cantidad")
        .dropna(subset=["release_year"])
    )

    # Implementación del gráfico de área apilada
    st.subheader("Distribución de lanzamientos por año y género")
    grafico_area = alt.Chart(datos_agregados).mark_area(opacity=0.8).encode(
        x=alt.X("release_year:O", title="Año de lanzamiento"),
        y=alt.Y("Cantidad:Q", stack="normalize", title="Proporción de lanzamientos"),
        color=alt.Color("primary_genre:N", title="Género"),
        tooltip=[
            alt.Tooltip("release_year", title="Año"),
            alt.Tooltip("primary_genre", title="Género"),
            alt.Tooltip("Cantidad", title="Juegos lanzados")
        ]
    ).properties(
        width=900,
        height=500,
        title="Distribución de lanzamientos por género"
    )

    st.altair_chart(grafico_area, use_container_width=True)

    # Implementación del gráfico de barras vertical apilado
    st.subheader("Conteo total de lanzamientos por año y género")
    grafico_barras = alt.Chart(datos_agregados).mark_bar().encode(
        y=alt.Y("release_year:O", title="Año de lanzamiento"),
        x=alt.X("Cantidad:Q", title="Cantidad de lanzamientos"),
        color=alt.Color("primary_genre:N", title="Género"),
        tooltip=[
            alt.Tooltip("release_year", title="Año"),
            alt.Tooltip("primary_genre", title="Género"),
            alt.Tooltip("Cantidad", title="Juegos lanzados")
        ]
    ).properties(
        width=900,
        height=800,
        title="Lanzamientos totales por año y género"
    )

    st.altair_chart(grafico_barras, use_container_width=True)

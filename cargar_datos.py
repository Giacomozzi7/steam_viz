import pandas as pd

def cargar_datos(ruta_csv="game_data_all.csv"):
    # Carga del archivo CSV
    df = pd.read_csv(ruta_csv)

    # Normalización y limpieza de la columna de géneros
    df["primary_genre"] = df["primary_genre"].astype(str)
    df["primary_genre"] = (
        df["primary_genre"]
        .str.strip().str.lower().str.title()
        .str.replace(r"\s*\(.*?\)", "", regex=True)
    )
    df = df[~df["primary_genre"].str.contains("unknown|nan", na=False)]

    # Limpieza de la columna de tecnologías detectadas
    if "detected_technologies" in df.columns:
        df["detected_technologies"] = df["detected_technologies"].astype(str)
        df["detected_technologies"] = df["detected_technologies"].str.extract(r"Engine\.([^\s;]+)", expand=False)

    # Conversión de columnas numéricas necesarias
    df["all_time_peak"] = pd.to_numeric(df["all_time_peak"], errors="coerce")
    df["24_hour_peak"] = pd.to_numeric(df["24_hour_peak"], errors="coerce")
    df["positive_reviews"] = pd.to_numeric(df["positive_reviews"], errors="coerce")
    df["total_reviews"] = pd.to_numeric(df["total_reviews"], errors="coerce")

    # Creación de métricas derivadas
    df["positive_ratio"] = df["positive_reviews"] / df["total_reviews"]
    df["release"] = pd.to_datetime(df["release"], errors="coerce")
    df["release_year"] = df["release"].dt.year
    df["player_activity_gap"] = df["all_time_peak"] - df["24_hour_peak"]

    # Cálculo del puntaje de éxito por desarrollador
    dev_score = df.groupby("developer")["positive_ratio"].mean().reset_index()
    dev_score.rename(columns={"positive_ratio": "developer_success_score"}, inplace=True)
    df = pd.merge(df, dev_score, on="developer", how="left")

    return df
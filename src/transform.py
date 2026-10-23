import pandas as pd


def limpiar_datos_base(datos):
    """
    Realiza la limpieza inicial del dataset Netflix.
    """

    df = datos.copy()

    # Eliminar columnas sin información
    df = df.dropna(axis=1, how="all")

    # Detectar duraciones ubicadas incorrectamente
    patron = r"^\s*\d+\s*(?:min|Seasons?)\s*$"

    mascara = (
        df["duration"].isna()
        & df["rating"].astype("string").str.fullmatch(
            patron, case=False
        ).fillna(False)
    )

    # Corregir los registros identificados
    cantidad_corregida = int(mascara.sum())

    df.loc[mascara, "duration"] = df.loc[
        mascara, "rating"
    ]

    df.loc[mascara, "rating"] = None

    print("LIMPIEZA INICIAL COMPLETADA")
    print("Filas:", len(df))
    print("Columnas:", len(df.columns))
    print("Duraciones corregidas:", cantidad_corregida)

    return df


def normalizar_duraciones(datos):
    """
    Separa la duración en valor numérico y unidad.
    """

    df = datos.copy()

    # Extraer la cantidad numérica
    df["duration_value"] = pd.to_numeric(
        df["duration"].astype("string").str.extract(
            r"^(\d+)", expand=False
        ),
        errors="coerce"
    )

    # Estandarizar la unidad de duración
    df["duration_unit"] = (
        df["duration"]
        .astype("string")
        .str.extract(
            r"^\d+\s*(min|Seasons?)$",
            expand=False
        )
        .replace({
            "Seasons": "Season"
        })
    )

    print("NORMALIZACIÓN DE DURACIONES")
    print(
        df.groupby(
            ["type", "duration_unit"]
        ).size()
    )

    print(
        "Duraciones sin valor:",
        df["duration_value"].isna().sum()
    )

    return df


def crear_tablas_relacionales(datos):
    """
    Construye las tres tablas del modelo relacional.
    """

    # Tabla principal
    contenido_nuevo = datos[
        [
            "show_id",
            "type",
            "title",
            "release_year",
            "rating",
            "duration_value",
            "duration_unit"
        ]
    ].copy()

    # Tabla de países
    contenido_pais_nuevo = datos[
        ["show_id", "country"]
    ].copy()

    contenido_pais_nuevo["country"] = (
        contenido_pais_nuevo["country"]
        .fillna("Sin información")
        .str.split(",")
    )

    contenido_pais_nuevo = (
        contenido_pais_nuevo
        .explode("country")
    )

    contenido_pais_nuevo["country"] = (
        contenido_pais_nuevo["country"]
        .str.strip()
    )

    contenido_pais_nuevo = (
        contenido_pais_nuevo[
            contenido_pais_nuevo["country"].notna()
            & contenido_pais_nuevo["country"].ne("")
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Tabla de géneros
    contenido_genero_nuevo = datos[
        ["show_id", "listed_in"]
    ].copy()

    contenido_genero_nuevo["listed_in"] = (
        contenido_genero_nuevo["listed_in"]
        .str.split(",")
    )

    contenido_genero_nuevo = (
        contenido_genero_nuevo
        .explode("listed_in")
    )

    contenido_genero_nuevo = (
        contenido_genero_nuevo
        .rename(columns={"listed_in": "genre"})
    )

    contenido_genero_nuevo["genre"] = (
        contenido_genero_nuevo["genre"]
        .str.strip()
    )

    contenido_genero_nuevo = (
        contenido_genero_nuevo[
            contenido_genero_nuevo["genre"].notna()
            & contenido_genero_nuevo["genre"].ne("")
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    print("TABLAS RELACIONALES CREADAS")
    print("Contenido:", len(contenido_nuevo))
    print("Países:", len(contenido_pais_nuevo))
    print("Géneros:", len(contenido_genero_nuevo))

    return (
        contenido_nuevo,
        contenido_pais_nuevo,
        contenido_genero_nuevo
    )

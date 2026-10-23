from pathlib import Path
import pandas as pd


def extraer_datos(ruta_archivo):
    """
    Extrae los datos originales de Netflix.
    """

    ruta = Path(ruta_archivo)

    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    datos = pd.read_csv(
        ruta,
        encoding="latin-1"
    )

    print("EXTRACCIÓN COMPLETADA")
    print("Filas:", len(datos))
    print("Columnas:", len(datos.columns))

    return datos

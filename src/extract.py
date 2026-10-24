from io import StringIO
from pathlib import Path

import pandas as pd


def decodificar_archivo(ruta):
    """
    Decodifica el CSV linea por linea.

    El archivo de Netflix esta en UTF-8, pero algunas filas traen bytes
    invalidos (por ejemplo la fila s8809). Leerlo entero como latin-1
    estropea los acentos de todo el archivo; por eso se intenta UTF-8
    primero y solo las lineas que fallan se leen como latin-1.

    Devuelve el texto completo y la cantidad de lineas con respaldo.
    """
    lineas = []
    con_respaldo = 0

    with Path(ruta).open("rb") as archivo:
        for linea in archivo:
            try:
                lineas.append(linea.decode("utf-8"))
            except UnicodeDecodeError:
                lineas.append(linea.decode("latin-1"))
                con_respaldo += 1

    return "".join(lineas), con_respaldo


def extraer_datos(ruta_archivo):
    """
    Extrae los datos originales de Netflix sin transformarlos.
    """

    ruta = Path(ruta_archivo)

    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    texto, con_respaldo = decodificar_archivo(ruta)
    datos = pd.read_csv(StringIO(texto))

    print("EXTRACCIÓN COMPLETADA")
    print("Filas:", len(datos))
    print("Columnas:", len(datos.columns))
    print("Líneas leídas con codificación de respaldo:", con_respaldo)

    return datos

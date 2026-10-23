from database import crear_conexion
from load import cargar_datos
from pathlib import Path

from extract import extraer_datos
from transform import (
    limpiar_datos_base,
    normalizar_duraciones,
    crear_tablas_relacionales
)
from validate import validar_datos


def main():
    proyecto = Path(__file__).resolve().parent.parent
    ruta_csv = proyecto / "data" / "netflix_titles.csv"

    print("INICIANDO PIPELINE NETFLIX ETL")
    print("-----------------------------")

    # EXTRACT
    datos = extraer_datos(ruta_csv)

    # TRANSFORM
    datos = limpiar_datos_base(datos)
    datos = normalizar_duraciones(datos)

    contenido, pais, genero = crear_tablas_relacionales(
        datos
    )

    # VALIDATE
    validar_datos(contenido, pais, genero)

    print("-----------------------------")
    print("PIPELINE DE TRANSFORMACIÓN COMPLETADO")
    print("Contenido:", len(contenido))
    print("Países:", len(pais))
    print("Géneros:", len(genero))


    # LOAD
    engine = crear_conexion()

    try:
        cargar_datos(
            engine,
            contenido,
            pais,
            genero
        )
    finally:
        engine.dispose()

    print("PIPELINE ETL FINALIZADO")


if __name__ == "__main__":
    main()

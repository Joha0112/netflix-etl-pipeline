from pathlib import Path

from database import crear_conexion
from load import cargar_datos
from logger import configurar_logger
from extract import extraer_datos
from transform import (
    limpiar_datos_base,
    normalizar_duraciones,
    crear_tablas_relacionales
)
from validate import validar_datos


def main():
    logger = configurar_logger()

    proyecto = Path(__file__).resolve().parent.parent
    ruta_csv = proyecto / "data" / "netflix_titles.csv"

    logger.info("INICIANDO PIPELINE NETFLIX ETL")

    try:
        # EXTRACT
        logger.info("Iniciando extracción")
        datos = extraer_datos(ruta_csv)
        logger.info("Extracción completada: %s filas", len(datos))

        # TRANSFORM
        logger.info("Iniciando transformación")
        datos = limpiar_datos_base(datos)
        datos = normalizar_duraciones(datos)

        contenido, pais, genero = crear_tablas_relacionales(datos)

        logger.info(
            "Transformación completada: %s contenidos, "
            "%s países, %s géneros",
            len(contenido),
            len(pais),
            len(genero)
        )

        # VALIDATE
        logger.info("Iniciando validación")
        validar_datos(contenido, pais, genero)
        logger.info("Validación completada correctamente")

        # LOAD
        logger.info("Iniciando etapa de carga en MySQL")
        engine = crear_conexion()

        try:
            cargar_datos(engine, contenido, pais, genero)
        finally:
            engine.dispose()

        logger.info("Etapa de carga finalizada")
        logger.info("PIPELINE ETL FINALIZADO CORRECTAMENTE")

    except Exception:
        logger.exception("ERROR DURANTE LA EJECUCIÓN DEL PIPELINE")
        raise


if __name__ == "__main__":
    main()

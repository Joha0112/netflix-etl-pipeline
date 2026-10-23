from validate import validar_datos
import pandas as pd
from sqlalchemy import text


def cargar_datos(engine, contenido, pais, genero):
    """
    Carga los datos en MySQL únicamente
    cuando las tres tablas están vacías.
    """

    tablas = {
        "contenido": contenido,
        "contenido_pais": pais,
        "contenido_genero": genero
    }

    # Validar los datos antes de cargar
    validar_datos(contenido, pais, genero)

    with engine.begin() as conexion:

        # Verificar la base de datos
        base_actual = conexion.execute(
            text("SELECT DATABASE()")
        ).scalar()

        if base_actual != "netflix_etl_dev":
            raise ValueError(
                f"Base de datos no autorizada: {base_actual}"
            )

        # Comprobar si ya existen registros
        cantidades = {}

        for tabla in tablas:
            cantidades[tabla] = conexion.execute(
                text(f"SELECT COUNT(*) FROM {tabla}")
            ).scalar()

        if any(cantidad > 0 for cantidad in cantidades.values()):
            print("CARGA OMITIDA")
            print("Las tablas ya contienen registros.")
            print("No se modificó la base de datos.")
            return

        # Insertar respetando las relaciones
        for nombre, datos in tablas.items():
            datos.to_sql(
                name=nombre,
                con=conexion,
                if_exists="append",
                index=False,
                chunksize=1000
            )

        print("CARGA ETL COMPLETADA")
        print("Registros insertados:")
        for nombre, datos in tablas.items():
            print(f"{nombre}: {len(datos)}")

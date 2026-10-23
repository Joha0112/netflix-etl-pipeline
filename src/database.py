import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def crear_conexion():
    proyecto = Path(__file__).resolve().parent.parent
    ruta_env = proyecto / ".env"

    if not ruta_env.is_file():
        raise FileNotFoundError(
            "No se encontró el archivo .env"
        )

    load_dotenv(ruta_env, override=True)

    variables = [
        "MYSQL_HOST",
        "MYSQL_PORT",
        "MYSQL_DATABASE",
        "MYSQL_USER",
        "MYSQL_PASSWORD"
    ]

    faltantes = [
        variable for variable in variables
        if not os.getenv(variable)
    ]

    if faltantes:
        raise ValueError(
            "Faltan variables de configuración: "
            + ", ".join(faltantes)
        )

    if os.getenv("MYSQL_DATABASE") != "netflix_etl_dev":
        raise ValueError(
            "Base de datos no autorizada"
        )

    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        database=os.getenv("MYSQL_DATABASE")
    )

    engine = create_engine(
        url,
        pool_pre_ping=True
    )

    with engine.connect() as conexion:
        base_actual = conexion.execute(
            text("SELECT DATABASE()")
        ).scalar_one()

        if base_actual != "netflix_etl_dev":
            raise ValueError(
                "La conexión apunta a una base no autorizada"
            )

    return engine

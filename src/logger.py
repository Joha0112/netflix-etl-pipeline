import logging
from pathlib import Path


def configurar_logger():
    """Configura el registro de ejecuciones del pipeline."""

    carpeta_logs = Path(__file__).resolve().parent.parent / "logs"
    carpeta_logs.mkdir(parents=True, exist_ok=True)

    archivo_log = carpeta_logs / "netflix_etl.log"

    logger = logging.getLogger("netflix_etl")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        archivo = logging.FileHandler(
            archivo_log,
            encoding="utf-8"
        )
        archivo.setFormatter(formato)

        consola = logging.StreamHandler()
        consola.setFormatter(formato)

        logger.addHandler(archivo)
        logger.addHandler(consola)

    return logger

import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from extract import extraer_datos  # noqa: E402

ENCABEZADO = "show_id,title\r\n"


def escribir_csv(carpeta, contenido_bytes):
    ruta = Path(carpeta) / "prueba.csv"
    ruta.write_bytes(contenido_bytes)
    return ruta


class TestExtract(unittest.TestCase):

    def test_conserva_acentos_utf8(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = escribir_csv(
                carpeta,
                (ENCABEZADO + "s1,Pokémon\r\ns2,El patrón\r\n").encode("utf-8"),
            )
            datos = extraer_datos(ruta)

        self.assertEqual(datos["title"].tolist(), ["Pokémon", "El patrón"])

    def test_linea_con_bytes_invalidos_no_rompe_ni_estropea_las_demas(self):
        contenido = (
            (ENCABEZADO + "s1,Pokémon\r\n").encode("utf-8")
            + b"s2,Nombre con \xf8 invalido\r\n"
            + "s3,El patrón\r\n".encode("utf-8")
        )

        with tempfile.TemporaryDirectory() as carpeta:
            datos = extraer_datos(escribir_csv(carpeta, contenido))

        self.assertEqual(len(datos), 3)
        self.assertEqual(datos.loc[0, "title"], "Pokémon")
        self.assertEqual(datos.loc[2, "title"], "El patrón")
        self.assertIn("ø", datos.loc[1, "title"])

    def test_archivo_inexistente_lanza_error(self):
        with self.assertRaises(FileNotFoundError):
            extraer_datos("no_existe.csv")


if __name__ == "__main__":
    unittest.main()

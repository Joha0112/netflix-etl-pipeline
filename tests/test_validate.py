import sys
import unittest
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from validate import validar_datos  # noqa: E402


def tablas_validas():
    contenido = pd.DataFrame({
        "show_id": ["s1", "s2"],
        "type": ["Movie", "Movie"],
        "title": ["A", "B"],
        "release_year": [2020, 2021],
    })
    pais = pd.DataFrame({"show_id": ["s1", "s2"], "country": ["Chile", "Peru"]})
    genero = pd.DataFrame({"show_id": ["s1", "s2"], "genre": ["Dramas", "Comedies"]})
    return contenido, pais, genero


class TestValidar(unittest.TestCase):

    def test_datos_validos_pasan(self):
        validar_datos(*tablas_validas())

    def test_detecta_show_id_repetido(self):
        c, p, g = tablas_validas()
        c.loc[1, "show_id"] = "s1"
        with self.assertRaises(AssertionError):
            validar_datos(c, p, g)

    def test_detecta_mismo_contenido_con_distinto_show_id(self):
        c, p, g = tablas_validas()
        c.loc[1, ["title", "release_year"]] = ["A", 2020]
        with self.assertRaises(AssertionError):
            validar_datos(c, p, g)

    def test_detecta_pais_sin_contenido(self):
        c, p, g = tablas_validas()
        p.loc[1, "show_id"] = "s999"
        with self.assertRaises(AssertionError):
            validar_datos(c, p, g)

    def test_detecta_genero_vacio(self):
        c, p, g = tablas_validas()
        g.loc[0, "genre"] = " "
        with self.assertRaises(AssertionError):
            validar_datos(c, p, g)


if __name__ == "__main__":
    unittest.main()

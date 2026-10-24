import sys
import unittest
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from transform import (  # noqa: E402
    crear_tablas_relacionales,
    eliminar_duplicados,
    limpiar_datos_base,
    limpiar_texto,
    normalizar_duraciones,
)

COLUMNAS = [
    "show_id", "type", "title", "director", "cast", "country",
    "date_added", "release_year", "rating", "duration",
    "listed_in", "description",
]


def fila(**valores):
    base = {
        "show_id": "s1", "type": "Movie", "title": "Titulo",
        "director": None, "cast": None, "country": "Chile",
        "date_added": "May 1, 2020", "release_year": 2020,
        "rating": "TV-MA", "duration": "90 min",
        "listed_in": "Dramas", "description": "Texto",
    }
    base.update(valores)
    return base


def tabla(*filas):
    return pd.DataFrame(list(filas), columns=COLUMNAS)


def relacionales(df):
    """Igual que en main.py: primero se normaliza la duracion."""
    return crear_tablas_relacionales(normalizar_duraciones(df))


class TestLimpiarTexto(unittest.TestCase):

    def test_recorta_y_colapsa_espacios(self):
        df = tabla(fila(title="  Hola   mundo  "))
        self.assertEqual(limpiar_texto(df).loc[0, "title"], "Hola mundo")

    def test_reemplaza_saltos_de_linea(self):
        df = tabla(fila(title="A Story of a\nFlying Fortress"))
        self.assertEqual(
            limpiar_texto(df).loc[0, "title"], "A Story of a Flying Fortress"
        )

    def test_texto_vacio_pasa_a_nulo(self):
        df = tabla(fila(director="   "))
        self.assertTrue(pd.isna(limpiar_texto(df).loc[0, "director"]))


class TestEliminarDuplicados(unittest.TestCase):

    def test_elimina_filas_identicas_salvo_show_id(self):
        df = tabla(fila(show_id="s1"), fila(show_id="s2"))
        resultado = eliminar_duplicados(df)
        self.assertEqual(resultado["show_id"].tolist(), ["s1"])

    def test_nulos_iguales_cuentan_como_duplicado(self):
        df = tabla(
            fila(show_id="s1", director=None, country=None),
            fila(show_id="s2", director=None, country=None),
        )
        self.assertEqual(len(eliminar_duplicados(df)), 1)

    def test_conserva_mismo_titulo_con_distinto_anio(self):
        df = tabla(
            fila(show_id="s1", release_year=2010),
            fila(show_id="s2", release_year=2020),
        )
        self.assertEqual(len(eliminar_duplicados(df)), 2)

    def test_duplicado_oculto_por_espacio_se_detecta_tras_limpiar(self):
        df = tabla(
            fila(show_id="s1", title="Consequences"),
            fila(show_id="s2", title="Consequences "),
        )
        resultado = limpiar_datos_base(df)
        self.assertEqual(resultado["show_id"].tolist(), ["s1"])


class TestLimpiarDatosBase(unittest.TestCase):

    def test_corrige_duracion_ubicada_en_rating(self):
        df = tabla(
            fila(show_id="s1", title="Normal", duration="90 min"),
            fila(show_id="s2", title="Desplazada", rating="74 min", duration=None),
        )
        resultado = limpiar_datos_base(df).set_index("show_id")
        self.assertEqual(resultado.loc["s2", "duration"], "74 min")
        self.assertTrue(pd.isna(resultado.loc["s2", "rating"]))

    def test_no_toca_filas_correctas(self):
        df = tabla(fila(rating="TV-MA", duration="90 min"))
        resultado = limpiar_datos_base(df)
        self.assertEqual(resultado.loc[0, "rating"], "TV-MA")
        self.assertEqual(resultado.loc[0, "duration"], "90 min")

    def test_elimina_columnas_completamente_vacias(self):
        df = tabla(fila())
        df["Unnamed: 12"] = float("nan")
        self.assertNotIn("Unnamed: 12", limpiar_datos_base(df).columns)


class TestNormalizarDuraciones(unittest.TestCase):

    def test_separa_valor_y_unidad(self):
        df = tabla(
            fila(show_id="s1", duration="90 min"),
            fila(show_id="s2", type="TV Show", duration="2 Seasons"),
            fila(show_id="s3", type="TV Show", duration="1 Season"),
        )
        r = normalizar_duraciones(df)
        self.assertEqual(r["duration_value"].tolist(), [90, 2, 1])
        self.assertEqual(r["duration_unit"].tolist(), ["min", "Season", "Season"])


class TestTablasRelacionales(unittest.TestCase):

    def test_separa_varios_paises_y_generos(self):
        df = tabla(fila(country="Chile, Peru", listed_in="Dramas, Comedies"))
        _, pais, genero = relacionales(df)
        self.assertEqual(sorted(pais["country"]), ["Chile", "Peru"])
        self.assertEqual(sorted(genero["genre"]), ["Comedies", "Dramas"])

    def test_pais_vacio_se_marca_sin_informacion(self):
        df = tabla(fila(country=None))
        _, pais, _ = relacionales(df)
        self.assertEqual(pais["country"].tolist(), ["Sin información"])

    def test_coma_final_no_genera_pais_vacio(self):
        df = tabla(fila(country="United Kingdom,"))
        _, pais, _ = relacionales(df)
        self.assertEqual(pais["country"].tolist(), ["United Kingdom"])


if __name__ == "__main__":
    unittest.main()

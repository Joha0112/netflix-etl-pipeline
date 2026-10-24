"""
Prueba de integracion con el CSV real (se omite si el archivo no esta).
No necesita MySQL: solo extraccion, transformacion y validacion.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from extract import extraer_datos  # noqa: E402
from transform import (  # noqa: E402
    crear_tablas_relacionales,
    limpiar_datos_base,
    normalizar_duraciones,
)
from validate import validar_datos  # noqa: E402

RUTA_CSV = RAIZ / "data" / "netflix_titles.csv"


@unittest.skipUnless(RUTA_CSV.is_file(), "No se encontró data/netflix_titles.csv")
class TestPipelineCompleto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        datos = extraer_datos(RUTA_CSV)
        datos = limpiar_datos_base(datos)
        datos = normalizar_duraciones(datos)
        cls.contenido, cls.pais, cls.genero = crear_tablas_relacionales(datos)

    def test_validacion_automatica_pasa(self):
        validar_datos(self.contenido, self.pais, self.genero)

    def test_cantidad_de_registros(self):
        self.assertEqual(len(self.contenido), 8805)
        self.assertEqual(len(self.pais), 10839)
        self.assertEqual(len(self.genero), 19319)

    def test_no_hay_titulos_con_codificacion_corrupta(self):
        self.assertFalse(self.contenido["title"].str.contains("Ã|Â").any())

    def test_acentos_correctos(self):
        titulos = set(self.contenido["title"])
        self.assertIn("Pokémon Master Journeys: The Series", titulos)

    def test_duplicados_conocidos_eliminados(self):
        ids = set(self.contenido["show_id"])
        for show_id in ["s5965", "s5966", "s5967", "s6530"]:
            self.assertNotIn(show_id, ids)

    def test_fila_con_bytes_invalidos_sigue_presente(self):
        self.assertIn("s8809", set(self.contenido["show_id"]))

    def test_duraciones_desplazadas_corregidas(self):
        filas = self.contenido[
            self.contenido["show_id"].isin(["s5542", "s5795", "s5814"])
        ]
        self.assertEqual(sorted(filas["duration_value"].tolist()), [66, 74, 84])
        self.assertTrue(filas["rating"].isna().all())


if __name__ == "__main__":
    unittest.main()

# Netflix ETL Pipeline

Proyecto de ingeniería de datos desarrollado con Python y MySQL.

## Objetivo

Construir un pipeline ETL que extraiga información de un
dataset de Netflix, limpie y normalice los datos, valide
su integridad y los almacene en una base de datos relacional.

## Tecnologías

- Python
- Pandas
- MySQL
- SQLAlchemy
- PyMySQL
- python-dotenv
- Jupyter Notebook

## Arquitectura del pipeline

```text
CSV de Netflix
      |
      v
EXTRACT - Lectura del archivo CSV
      |
      v
TRANSFORM - Limpieza y normalización
      |
      v
VALIDATE - Controles de calidad
      |
      v
LOAD - Almacenamiento en MySQL
```

## Estructura del proyecto

```text
netflix-etl-pipeline/
├── data/
│   └── netflix_titles.csv
├── notebooks/
│   └── 01_netflix_pipeline_etl.ipynb
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   ├── test_validate.py
│   └── test_pipeline_completo.py
├── sql/
│   └── create_tables.sql
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Modelo de datos

El pipeline genera tres tablas relacionales:

| Tabla | Registros |
|---|---:|
| contenido | 8.805 |
| contenido_pais | 10.839 |
| contenido_genero | 19.319 |

Total: 38.963 registros.

## Instalación

1. Clonar el repositorio.
2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env` utilizando `.env.example`
   como referencia.
4. Configurar una base de datos MySQL llamada
   `netflix_etl_dev` con las tres tablas necesarias.
5. Ejecutar el pipeline:

```bash
python src/main.py
```

## Validaciones

El proyecto incluye controles de:

- Identificadores duplicados.
- Valores obligatorios vacíos.
- Integridad referencial.
- Consistencia de las tablas.
- Prevención de cargas duplicadas cuando las tablas
  ya contienen registros.

## Estado del proyecto

Pipeline ETL local implementado y probado correctamente.

La carga actual es de tipo inicial: cuando las tablas
ya contienen registros, el programa omite la inserción.
No implementa todavía cargas incrementales.

## Pruebas automatizadas

El proyecto incluye **29 pruebas automatizadas**, ejecutadas
exitosamente con pytest.

Las pruebas verifican:

- Extracción y lectura de datos.
- Tratamiento de caracteres y codificaciones.
- Eliminación de registros duplicados.
- Limpieza y transformación de datos.
- Normalización de duraciones.
- Creación y consistencia de tablas relacionales.
- Validaciones de calidad de datos.

Para ejecutar las pruebas:

```bash
python -m pytest tests/ -v
```

## Próximas mejoras

- Automatización de ejecuciones.
- Registro de logs.
- Implementación en Microsoft Azure.


## Fuente de los datos

- Dataset: Netflix Movies and TV Shows
- Autor: Shivam Bansal
- Plataforma: Kaggle
- Fuente: https://www.kaggle.com/datasets/shivamb/netflix-shows
- Licencia publicada: CC0 (Public Domain)

El archivo `data/netflix_titles.csv` se utiliza
con fines de aprendizaje y demostración de un
pipeline de ingeniería de datos.

Este proyecto es independiente y no está
afiliado oficialmente con Netflix.

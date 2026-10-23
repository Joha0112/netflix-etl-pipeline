import pandas as pd


def validar_datos(contenido, contenido_pais, contenido_genero):

    # Validar identificadores únicos
    assert contenido["show_id"].is_unique, (
        "Existen contenidos duplicados"
    )

    # Validar identificadores no nulos
    assert contenido["show_id"].notna().all(), (
        "Existen identificadores vacíos"
    )

    # Validar relaciones de países
    assert not contenido_pais.duplicated(
        subset=["show_id", "country"]
    ).any(), "Existen relaciones de países duplicadas"

    # Validar relaciones de géneros
    assert not contenido_genero.duplicated(
        subset=["show_id", "genre"]
    ).any(), "Existen relaciones de géneros duplicadas"

    # Validar integridad referencial
    assert contenido_pais["show_id"].isin(
        contenido["show_id"]
    ).all(), "Existen países sin contenido"

    assert contenido_genero["show_id"].isin(
        contenido["show_id"]
    ).all(), "Existen géneros sin contenido"

    # Validar valores obligatorios
    assert contenido_pais["country"].notna().all()
    assert contenido_genero["genre"].notna().all()

    assert contenido_pais["country"].astype(
        "string"
    ).str.strip().ne("").all()

    assert contenido_genero["genre"].astype(
        "string"
    ).str.strip().ne("").all()

    print("VALIDACIÓN AUTOMÁTICA EXITOSA")
    print("Contenidos:", len(contenido))
    print("Relaciones de países:", len(contenido_pais))
    print("Relaciones de géneros:", len(contenido_genero))

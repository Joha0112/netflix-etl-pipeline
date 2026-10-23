-- Netflix ETL Pipeline
-- Esquema de tablas para MySQL 8
-- Ejecutar en la base de datos netflix_etl_dev

CREATE TABLE IF NOT EXISTS contenido (
    show_id VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    release_year SMALLINT DEFAULT NULL,
    rating VARCHAR(30) DEFAULT NULL,
    duration_value SMALLINT DEFAULT NULL,
    duration_unit VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (show_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contenido_pais (
    show_id VARCHAR(10) NOT NULL,
    country VARCHAR(150) NOT NULL,
    PRIMARY KEY (show_id, country),
    CONSTRAINT contenido_pais_ibfk_1
        FOREIGN KEY (show_id)
        REFERENCES contenido(show_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contenido_genero (
    show_id VARCHAR(10) NOT NULL,
    genre VARCHAR(150) NOT NULL,
    PRIMARY KEY (show_id, genre),
    CONSTRAINT contenido_genero_ibfk_1
        FOREIGN KEY (show_id)
        REFERENCES contenido(show_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

# ChallengeFastapi


# Pasos a seguir para levantar el proyecto

- Clonar repositorio.

- Crear entorno virtual:

``` python3 -m venv ./venv ```

- Activar

``` . venv/bin/activate ```

- Instalar requirements

``` pip install -r requirements.txt ```


Dentro del proyecto, en la carpeta models, en el archivo db.py, completar user y password.

Correr el proyecto:

``` uvicorn app:app --reload ```


Corriendo el proyecto se deberia crear las tablas del proyecto.
Se puede crear de forma manual

Para crear la base:

CREATE DATABASE challengeBanza;


Para crear las tablas

CREATE TABLE client (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE accounts (
    id CHAR(36) PRIMARY KEY,
    id_client CHAR(36),
    balance FLOAT,
    FOREIGN KEY (id_client) REFERENCES client(id)
);


CREATE TABLE categorys (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE categorys_clients (
    id_category CHAR(36),
    id_client CHAR(36),
    FOREIGN KEY (id_category) REFERENCES categorys(id),
    FOREIGN KEY (id_client) REFERENCES client(id)
);


CREATE TABLE motions (
    id CHAR(36) PRIMARY KEY,
    id_account CHAR(36),
    type VARCHAR(255),
    amount FLOAT,
    date DATE,
    FOREIGN KEY (id_account) REFERENCES accounts(id)
);

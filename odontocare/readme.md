# OdontoCare – Proyecto Final Python C1

## Descripción General

OdontoCare es una API REST desarrollada con Flask para la gestión de clínicas dentales.
Permitiendo administrar usuarios, pacientes, doctores, centros medicos y citas médicas,
su autenticación es mediante JWT, control de roles, en SQLite a través de SQLAlchemy
y una arquitectura modular basada en Blueprints.

El proyecto cuenta con un cliente externo en Python y una arquitectura preparada para su ejecución mediante Docker.

---

## Arquitectura del Proyecto

El proyecto sigue una arquitectura modular organizada por dominios, utilizando Blueprints de Flask.
Cada módulo se encarga de una responsabilidad concreta del sistema, para su buen mantenimiento y
escalabilidad.

La aplicación principal inicializa Flask, configura las extensiones y registra los distintos módulos.
Las responsabilidades se dividen de la siguiente forma:

- El módulo de autenticación gestiona el inicio de sesión y la generación de tokens JWT.
- El módulo de administración permite la gestión de usuarios, pacientes, doctores y centros médicos.
- El módulo de citas implementa la lógica de negocio relacionada con la creación, consulta y cancelación de citas.
- Los modelos de datos se definen mediante SQLAlchemy y representan las entidades principales del sistema.
- Los mecanismos de seguridad y control de roles se implementan mediante decoradores personalizados.

El cliente externo se encuentra desacoplado del backend y consume la API a través de peticiones HTTP,
simulando el uso real del sistema desde una aplicación independiente.

---

## Tecnologías Utilizadas

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite
- Requests
- Docker

---

## Autenticación y Seguridad

La API utiliza autenticación basada en JWT.

Endpoint de autenticación:

POST /auth/login

El token obtenido debe enviarse en cada petición protegida mediante el header:

Authorization: Bearer <token>

La validación de permisos y roles se realiza exclusivamente en el servidor,
evitando confiar en información proporcionada por el cliente.

---

## Roles del Sistema

- admin: gestión completa del sistema
- secretaria: gestión y cancelación de citas
- medico: creación y visualización de sus propias citas
- paciente: visualización de sus propias citas

---

## Endpoints Principales

Autenticación:
- POST /auth/login

Administración (requiere rol admin):
- POST /admin/usuarios
- POST /admin/pacientes
- POST /admin/doctores
- POST /admin/centros

Gestión de Citas:
- POST /citas
- GET /citas
- PUT /citas/<id>

---

## Reglas de consulta

- Un paciente solo puede consultar sus propias citas.
- La creación de citas está restringida a los roles admin y medico.
- No se permite agendar citas duplicadas para un mismo doctor en la misma fecha y hora.
- Un doctor solo puede consultar sus propias citas.
- Solo los roles admin y secretaria pueden cancelar citas.
- Un paciente inactivo no puede tener citas médicas.

---

## Cliente Externo

El proyecto incluye un cliente externo desarrollado en Python que consume la API REST.
El cliente gestiona la autenticación, el envío del token y las consultas con distintos endpoints.

La carga de datos inicial se puede hacer desde un archivo CSV locales (dentro de la carpeta data),
enviando los registros de forma individual a la API.

---

## Base de Datos

El sistema utiliza SQLite como motor de base de datos y SQLAlchemy.
Las tablas se crean automáticamente al iniciar la aplicación.
La base de datos no se incluye en el repositorio y se genera localmente.

---

## Docker

El proyecto incluye un Dockerfile para la construcción de la imagen del servicio.

---

## Ejecución Local

1. Instalar dependencias:
   pip install -r requirements.txt

2. Ejecutar la aplicación:
   python run.py

3. Ejecutar el cliente:
   python client/client.py

---

## Vídeo de Demostración

El proyecto incluye un vídeo explicativo donde se muestra el funcionamiento completo del sistema,
incluyendo autenticación, uso del cliente externo, gestión de entidades y control de roles.

---




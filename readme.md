## Proyecto Final Python C1

## Descripción General

OdontoCare es una API REST desarrollada con Flask para la gestión de clínicas dentales.
Permitiendo administrar usuarios, pacientes, doctores, centros medicos y citas médicas,
su autenticación es mediante JWT, control de roles, en SQLite a través de SQLAlchemy
y una arquitectura modular basada en Blueprints.

El proyecto cuenta con un cliente externo en Python y esta preparada para su ejecución mediante Docker.

---

## Arquitectura del Proyecto

El proyecto sigue una arquitectura modular, utilizando Blueprints de Flask.
Cada módulo se encarga de una responsabilidad concreta del sistema, para su buen mantenimiento y
escalabilidad.

La aplicación principal inicializa Flask, configura las extensiones y registra los distintos módulos.
Las responsabilidades se dividen de la siguiente forma:

- El módulo de autenticación gestiona el inicio de sesión y la generación de tokens JWT.
- El módulo de administración permite la gestión de usuarios, pacientes, doctores y centros médicos.
- El módulo de citas implementa la lógica de negocio relacionada con la creación, consulta y cancelación de citas.
- Los modelos de datos se definen mediante SQLAlchemy y representan las entidades principales del sistema.

El cliente externo es independiente del backend y consume la API a través de peticiones HTTP,
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


## Autenticación y Seguridad

La API utiliza autenticación basada en JWT.

Endpoint de autenticación:

POST /auth/login

El token obtenido debe enviarse en cada petición protegida mediante el header:

Authorization: Bearer <token>

La validación de permisos y roles se realiza exclusivamente en el servidor,
no se confia en información proporcionada por el cliente.

---

## Roles del Sistema


| Acción            | Admin | Secretaria | Médico | Paciente |
|-------------------|:-----:|:----------:|:------:|:--------:|
| Crear pacientes   | Sí    | No         | No     | No       |
| Crear doctores    | Sí    | No         | No     | No       |
| Crear centros     | Sí    | No         | No     | No       |
| Crear citas       | Sí    | No         | No     | Sí (solo propias) |
| Cancelar citas    | Sí    | Sí         | No     | No       |
| Ver citas         | Todas | Filtradas por fecha | Propias | Propias |

---

## Endpoints Principales

---

## Creación primer usuario Admin:

- POST /auth/register (Esta colsulta solo se ejecuta para crear el 1 usuario admin cuan no hay registos en la bdd )

(CON BDD VACIA SIN TOKEN SOLO LA 1 VEZ)

ejemplo:(POST) http://127.0.0.1:5000/auth/register

json:

{
  "username": "admin",
  "password": "admin123"
}

(No lleva token, porque aún no existe ningún usuario.)

## Autenticación:

- POST /auth/login (Permite autenticar un usuario y obtener un token JWT)

ejemplo:(POST) http://127.0.0.1:5000/auth/login

json:

{
  "username": "admin",
  "password": "admin123"
}


## Creación admin o secretaria:

- POST /admin/usuario

ejemplo: (POST) http://127.0.0.1:5000/admin/usuario

json:

{
  "username": "secretaria1",
  "password": "1234",
  "rol": "secretaria"
}

(NECESARIO TOKEN ADMIN)

## Gestión de doctores:

- POST /admin/doctores

(Permite crear Doctores)

ejemplo: (POST) http://127.0.0.1:5000/admin/doctores

json:

{
  "nombre": "Dr. Pepito",
  "especialidad": "Diagnóstico",
  "centro_id": 1,
  "username": "dr.pepito",
  "password": "1234"
}

(NECESARIO TOKEN ADMIN)



## Esquema Endpoint por Rol (Resumen):

| Endpoint                                | Rol que crea            | Quién puede llamarlo |
| --------------------------------------- | ----------------------- | -------------------- |
| `POST /auth/register`                   | admin (solo el primero) | Sistema (BDD vacía)  |
| `POST /admin/pacientes`                 | paciente                | Admin                |
| `POST /admin/doctores`                  | medico                  | Admin                |
| `POST /admin/usuarios`                  | admin / secretaria      | Admin                |


## Gestion Centros Médicos:

- POST /admin/centros

- GET  /admin/centros/<id>

(Permite crear centros médicos y consultar su información.)

ejemplo: (POST) http://127.0.0.1:5000/admin/centros

json:

{
  "nombre": "Hospital Central",
  "direccion": "Calle Mayor 123"
}

(NECESARIO TOKEN ADMIN)

## Gestión de pacientes:

- POST /admin/pacientes
- GET  /admin/pacientes
- GET  /admin/pacientes/<id>
- PUT  /admin/pacientes/<id>
- DELETE /admin/pacientes/<id>

(Permite crear, consultar, actualizar y eliminar pacientes.)

(NECESARIO TOKEN ADMIN)

## Gestión de citas

POST /citas (Crear cita)
*Evita doble reserva del doctor
GET /citas (Listar citas)

ejemplo : (POST) http://127.0.0.1:5000/citas

json:

{
  "paciente_id": 1,
  "doctor_id": 1,
  "centro_id": 1,
  "fecha": "2026-01-20T10:00:00",
  "motivo": "Revisión general"
}

(NECESARIO TOKEN ADMIN O MISMO PACIENTE)

## Reglas de consulta de citas

- Un paciente solo puede consultar sus propias citas.
- La creación de citas está restringida a los roles admin y medico.
- No se permite agendar citas duplicadas para un mismo doctor en la misma fecha y hora.
- Un doctor solo puede consultar sus propias citas.
- Solo los roles admin y secretaria pueden cancelar citas.
- Un paciente inactivo no puede tener citas médicas.


## Cliente Externo (dentro de carpeta client)

El proyecto incluye un cliente externo desarrollado en Python que consume la API REST.
El cliente gestiona la autenticación, el envío del token y las consultas con distintos endpoints.

La carga de datos inicial se puede hacer desde un archivo CSV locales (dentro de la carpeta data),
enviando los registros de forma individual a la API.

Ejecución (dentro de su carpeta client) : python client.py

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

Esta disponible en :

https://drive.google.com/file/d/1ikd3znU5BWZp_AQER4Kaxw9uekWOK6nE/view?usp=drive_link

(Vídeo se entrega mediante enlace externo debido a la limitación de tamaño de GitHub)

---




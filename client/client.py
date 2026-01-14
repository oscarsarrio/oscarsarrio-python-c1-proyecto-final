import requests
import csv

BASE_URL = "http://127.0.0.1:5000"

# -----------------------
# Helpers HTTP
# -----------------------
def post(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(url, json=data, headers=headers)

def get(url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(url, headers=headers)

# -----------------------
# Auth
# -----------------------
def login():
    print("\nLOGIN")
    username = input("Usuario: ")
    password = input("Password: ")

    r = post(f"{BASE_URL}/auth/login", {
        "username": username,
        "password": password
    })
    r.raise_for_status()
    print("Login correcto\n")
    return r.json()["access_token"]

# -----------------------
# Formularios
# -----------------------
def crear_paciente(token):
    print("\nCREAR PACIENTE")
    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    estado = input("Estado (ACTIVO/INACTIVO) [ACTIVO]: ") or "ACTIVO"
    username = input("Username del paciente: ")
    password = input("Password del paciente: ")

    r = post(f"{BASE_URL}/admin/pacientes", {
        "nombre": nombre,
        "telefono": telefono,
        "estado": estado,
        "username": username,
        "password": password
    }, token)
    
    if r.status_code == 403:
        print("No tienes permisos para crear pacientes (solo admin).\n")
        return

    if r.status_code == 400:
        print("Datos inválidos:", r.json().get("error"), "\n")
        return

    r.raise_for_status()
    print("Paciente creado:", r.json()["paciente"], "\n")
    
def crear_centro(token):
  def crear_centro(token):
    print("\nCREAR CENTRO")
    nombre = input("Nombre: ")
    direccion = input("Dirección: ")

    r = post(f"{BASE_URL}/admin/centros", {
        "nombre": nombre,
        "direccion": direccion
    }, token)

    if r.status_code == 403:
        print("No tienes permisos para crear centros (solo admin).\n")
        return

    if r.status_code == 400:
        print("Datos inválidos:", r.json().get("error"), "\n")
        return

    r.raise_for_status()
    print("Centro creado:", r.json()["centro"], "\n")

def crear_doctor(token):
    print("\nCREAR DOCTOR")
    nombre = input("Nombre: ")
    especialidad = input("Especialidad: ")
    centro_id = input("ID del centro: ")
    username = input("Username del doctor: ")
    password = input("Password del doctor: ")

    r = post(f"{BASE_URL}/admin/doctores", {
        "nombre": nombre,
        "especialidad": especialidad,
        "centro_id": int(centro_id),
        "username": username,
        "password": password
    }, token)
    
    if r.status_code == 403:
        print("No tienes permisos para crear doctores (solo admin).\n")
        return

    if r.status_code == 400:
        print("Datos inválidos:", r.json().get("error"), "\n")
        return



    r.raise_for_status()
    print("Doctor creado:", r.json()["doctor"], "\n")


def crear_cita(token):
   def crear_cita(token):
    print("\nCREAR CITA")

    try:
        paciente_id = int(input("ID del paciente: "))
        doctor_id = int(input("ID del doctor: "))
        centro_id = int(input("ID del centro: "))
        fecha = input("Fecha (YYYY-MM-DDTHH:MM:SS): ")
        motivo = input("Motivo: ")

        r = post(f"{BASE_URL}/citas", {
            "paciente_id": paciente_id,
            "doctor_id": doctor_id,
            "centro_id": centro_id,
            "fecha": fecha,
            "motivo": motivo
        }, token)

        if r.status_code == 400:
            print("Error de validación:", r.json().get("error"))
            return

        if r.status_code == 403:
            print("No tienes permisos para crear citas.")
            return

        if r.status_code == 404:
            print("Paciente, doctor o centro no existe.")
            return

        if r.status_code == 409:
            print("El doctor ya tiene una cita en esa fecha.")
            return

        r.raise_for_status()

        print("Cita creada correctamente:")
        print(r.json()["cita"], "\n")

    except ValueError:
        print("Error: los IDs deben ser numéricos.\n")

    
def listar_citas(token):
    print("\nLISTAR CITAS")
    print("Filtros opcionales (deja vacío si no aplica)")
    doctor_id = input("Doctor ID: ")
    paciente_id = input("Paciente ID: ")
    centro_id = input("Centro ID: ")
    estado = input("Estado (ACTIVA/CANCELADA): ")
    fecha = input("Fecha (YYYY-MM-DDTHH:MM:SS): ")

    params = {}
    if doctor_id:
        params["doctor_id"] = doctor_id
    if paciente_id:
        params["paciente_id"] = paciente_id
    if centro_id:
        params["centro_id"] = centro_id
    if estado:
        params["estado"] = estado
    if fecha:
        params["fecha"] = fecha

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/citas", params=params, headers=headers)

    r.raise_for_status()
    for c in r.json():
        print(c)


# -----------------------
# Menú
# -----------------------
def menu():
    print("""
========= ODONTOCARE =========
1. Crear paciente
2. Crear centro
3. Crear doctor
4. Crear cita
5. Listar citas
6. Cargar datos desde CSV
0. Salir
==============================
""")

def main():
    token = login()

    while True:
        menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_paciente(token)
        elif opcion == "2":
            crear_centro(token)
        elif opcion == "3":
            crear_doctor(token)
        elif opcion == "4":
            crear_cita(token)
        elif opcion == "5":
            listar_citas(token)
        elif opcion == "6":
            cargar_datos_csv(token)
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida\n")
            
def cargar_datos_csv(token, ruta_csv="../data/datos.csv"):
    print("\nCargando datos desde CSV...\n")

    with open(ruta_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for fila in reader:
            tipo = fila["tipo"]

            try:
                if tipo == "centro":
                    r = post(f"{BASE_URL}/admin/centros", {
                        "nombre": fila["nombre"],
                        "direccion": fila["direccion"]
                    }, token)

                elif tipo == "paciente":
                    r = post(f"{BASE_URL}/admin/pacientes", {
                        "nombre": fila["nombre"],
                        "telefono": fila["telefono"],
                        "estado": fila["estado"],
                        "username": fila["username"],
                        "password": fila["password"]
                    }, token)

                elif tipo == "doctor":
                    r = post(f"{BASE_URL}/admin/doctores", {
                        "nombre": fila["nombre"],
                        "especialidad": fila["especialidad"],
                        "centro_id": int(fila["centro_id"]),
                        "username": fila["username"],
                        "password": fila["password"]
                    }, token)

                else:
                    print(f"Tipo desconocido: {tipo}")
                    continue

                if r.status_code in (200, 201):
                    print(f"OK → {tipo}: {fila['nombre']}")
                elif r.status_code == 409:
                    print(f"YA EXISTE → {tipo}: {fila['nombre']}")
                else:
                    print(f"ERROR ({r.status_code}) → {tipo}: {fila['nombre']}")

            except Exception as e:
                print(f"Excepción procesando fila {fila}: {e}")

def crear_cita(token):
    print("\nCREAR CITA")

    try:
        paciente_id = int(input("ID del paciente (si eres paciente se aplicará tu id): "))
        doctor_id = int(input("ID del doctor: "))
        centro_id = int(input("ID del centro: "))
        fecha = input("Fecha (YYYY-MM-DDTHH:MM:SS): ")
        motivo = input("Motivo: ")

        r = post(f"{BASE_URL}/citas", {
            "paciente_id": paciente_id,
            "doctor_id": doctor_id,
            "centro_id": centro_id,
            "fecha": fecha,
            "motivo": motivo
        }, token)

        # ---- Gestión de errores ----
        if r.status_code == 400:
            print("Error de validación:", r.json().get("error"), "\n")
            return

        if r.status_code == 403:
            print("No tienes permisos para crear citas.\n")
            return

        if r.status_code == 404:
            print("Paciente, doctor o centro no existe.\n")
            return

        if r.status_code == 409:
            print("El doctor ya tiene una cita en esa fecha y hora.\n")
            return

        r.raise_for_status()

        print("Cita creada correctamente:")
        print(r.json()["cita"], "\n")

    except ValueError:
        print("Error: los IDs deben ser numéricos.\n")


if __name__ == "__main__":
    main()

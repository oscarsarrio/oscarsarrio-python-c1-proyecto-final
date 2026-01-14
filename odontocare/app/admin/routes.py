from werkzeug.security import generate_password_hash
from app.utils.security import admin_required
from app.models import User

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Paciente, Centro, Doctor

admin_bp = Blueprint("admin", __name__)

# ----------------------
# Ping protegido
# ----------------------

@admin_bp.route("/ping", methods=["GET"])
@jwt_required()
def ping():
    return jsonify({"message": "Admin protegido funcionando"})


# ======================
# CRUD PACIENTES
# ======================

@admin_bp.route("/pacientes", methods=["POST"])
@admin_required
def crear_paciente():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    nombre = data.get("nombre")
    telefono = data.get("telefono")
    estado = data.get("estado", "ACTIVO")

    username = data.get("username")
    password = data.get("password")

    if not nombre or not username or not password:
        return jsonify({
            "error": "nombre, username y password son obligatorios"
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    # Crear usuario paciente
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        rol="paciente"
    )

    db.session.add(user)
    db.session.flush()  # obtenemos user.id

    paciente = Paciente(
        nombre=nombre,
        telefono=telefono,
        estado=estado,
        id_usuario=user.id
    )

    db.session.add(paciente)
    db.session.commit()

    return jsonify({
        "message": "Paciente creado correctamente",
        "paciente": {
            "id": paciente.id,
            "nombre": paciente.nombre,
            "telefono": paciente.telefono,
            "estado": paciente.estado,
            "usuario": {
                "id": user.id,
                "username": user.username,
                "rol": user.rol
            }
        }
    }), 201

@admin_bp.route("/pacientes", methods=["GET"])
@jwt_required()
def listar_pacientes():
    pacientes = Paciente.query.all()

    return jsonify([
        {
            "id": p.id,
            "nombre": p.nombre,
            "telefono": p.telefono,
            "estado": p.estado,
            "id_usuario": p.id_usuario
        }
        for p in pacientes
    ]), 200


@admin_bp.route("/pacientes/<int:paciente_id>", methods=["GET"])
@admin_required
def obtener_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)

    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404

    return jsonify({
        "id": paciente.id,
        "nombre": paciente.nombre,
        "telefono": paciente.telefono,
        "estado": paciente.estado,
        "id_usuario": paciente.id_usuario
    }), 200


@admin_bp.route("/pacientes/<int:paciente_id>", methods=["PUT"])
@admin_required
def actualizar_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)

    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404

    data = request.get_json()

    paciente.nombre = data.get("nombre", paciente.nombre)
    paciente.telefono = data.get("telefono", paciente.telefono)
    paciente.estado = data.get("estado", paciente.estado)
    paciente.id_usuario = data.get("id_usuario", paciente.id_usuario)

    db.session.commit()

    return jsonify({"message": "Paciente actualizado correctamente"}), 200


@admin_bp.route("/pacientes/<int:paciente_id>", methods=["DELETE"])
@admin_required
def eliminar_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)

    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404

    db.session.delete(paciente)
    db.session.commit()

    return jsonify({"message": "Paciente eliminado correctamente"}), 200


# ======================
# CRUD CENTROS
# ======================

@admin_bp.route("/centros", methods=["POST"])
@admin_required
def crear_centro():
    data = request.get_json()

    nombre = data.get("nombre")
    direccion = data.get("direccion")

    if not nombre or not direccion:
        return jsonify({"error": "Nombre y dirección obligatorios"}), 400

    centro_existente = Centro.query.filter_by(nombre=nombre).first()
    if centro_existente:
        return jsonify({
            "error": "El centro ya existe",
            "centro_id": centro_existente.id
        }), 409

    centro = Centro(nombre=nombre, direccion=direccion)
    db.session.add(centro)
    db.session.commit()

    return jsonify({
        "message": "Centro creado correctamente",
        "centro": {
            "id": centro.id,
            "nombre": centro.nombre
        }
    }), 201

@admin_bp.route("/centros/<int:centro_id>", methods=["GET"])
@jwt_required()
def obtener_centro(centro_id):
    centro = Centro.query.get(centro_id)

    if not centro:
        return jsonify({"error": "Centro no encontrado"}), 404

    return jsonify({
        "id": centro.id,
        "nombre": centro.nombre,
        "direccion": centro.direccion
    }), 200


# ======================
# CRUD DOCTORES
# ======================

@admin_bp.route("/doctores", methods=["POST"])
@admin_required
def crear_doctor():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    nombre = data.get("nombre")
    especialidad = data.get("especialidad")
    centro_id = data.get("centro_id")

    username = data.get("username")
    password = data.get("password")

    if not nombre or not especialidad or not centro_id or not username or not password:
        return jsonify({
            "error": "nombre, especialidad, centro_id, username y password son obligatorios"
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    centro = Centro.query.get(centro_id)
    if not centro:
        return jsonify({"error": "El centro no existe"}), 404

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        rol="medico"
    )

    db.session.add(user)
    db.session.flush()

    doctor = Doctor(
        nombre=nombre,
        especialidad=especialidad,
        centro_id=centro_id,
        id_usuario=user.id
    )

    db.session.add(doctor)
    db.session.commit()

    return jsonify({
        "message": "Doctor creado correctamente",
        "doctor": {
            "id": doctor.id,
            "nombre": doctor.nombre,
            "especialidad": doctor.especialidad,
            "centro": {
                "id": centro.id,
                "nombre": centro.nombre
            },
            "usuario": {
                "id": user.id,
                "username": user.username,
                "rol": user.rol
            }
        }
    }), 201


# ======================
# CRUD ROLES
# ======================

@admin_bp.route("/usuario", methods=["POST"])
@admin_required
def crear_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    username = data.get("username")
    password = data.get("password")
    rol = data.get("rol")

    if not username or not password or not rol:
        return jsonify({
            "error": "username, password y rol son obligatorios"
        }), 400

    if rol not in ["admin", "secretaria"]:
        return jsonify({
            "error": "Rol inválido. Solo se permite admin o secretaria"
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        rol=rol
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Usuario creado correctamente",
        "usuario": {
            "id": user.id,
            "username": user.username,
            "rol": user.rol
        }
    }), 201

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.extensions import db
from app.models import Cita, Paciente, Doctor, Centro,User

citas_bp = Blueprint("citas", __name__)

# ======================
# Crear cita
# ======================

@citas_bp.route("/", methods=["POST"])
@jwt_required()
def crear_cita():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    doctor_id = data.get("doctor_id")
    centro_id = data.get("centro_id")
    fecha = data.get("fecha")
    motivo = data.get("motivo")
    estado = data.get("estado", "PENDIENTE")

    if not doctor_id or not centro_id or not fecha:
        return jsonify({
            "error": "doctor_id, centro_id y fecha son obligatorios"
        }), 400

    # Usuario autenticado
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    # Determinar paciente según rol
    if user.rol == "paciente":
        paciente = Paciente.query.filter_by(id_usuario=user.id).first()
        if not paciente:
            return jsonify({"error": "Paciente no válido"}), 400
        paciente_id = paciente.id
    else:
        paciente_id = data.get("paciente_id")
        if not paciente_id:
            return jsonify({"error": "paciente_id es obligatorio"}), 400
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({"error": "Paciente no existe"}), 404

    # Validar fecha
    try:
        fecha_dt = datetime.fromisoformat(fecha)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido (ISO 8601)"}), 400

    # Validaciones de existencia
    doctor = Doctor.query.get(doctor_id)
    centro = Centro.query.get(centro_id)

    if not doctor:
        return jsonify({"error": "Doctor no existe"}), 404
    if not centro:
        return jsonify({"error": "Centro no existe"}), 404

    if paciente.estado != "ACTIVO":
        return jsonify({"error": "Paciente inactivo"}), 400

    # Doctor pertenece al centro
    if doctor.centro_id != centro.id:
        return jsonify({"error": "El doctor no pertenece a este centro"}), 400

    # Evitar doble reserva
    cita_existente = Cita.query.filter_by(
        doctor_id=doctor_id,
        fecha=fecha_dt
    ).first()

    if cita_existente:
        return jsonify({
            "error": "El doctor ya tiene una cita en esa fecha y hora"
        }), 409

    # Crear cita
    cita = Cita(
        fecha=fecha_dt,
        motivo=motivo,
        estado=estado,
        paciente_id=paciente.id,
        doctor_id=doctor.id,
        centro_id=centro.id,
        id_usuario_registra=user.id
    )

    db.session.add(cita)
    db.session.commit()

    return jsonify({
        "message": "Cita creada correctamente",
        "cita": {
            "id": cita.id,
            "fecha": cita.fecha.isoformat(),
            "estado": cita.estado,
            "paciente": paciente.nombre,
            "doctor": doctor.nombre,
            "centro": centro.nombre,
            "motivo": cita.motivo,
            "usuario_registra": user.username
        }
    }), 201


# ======================
# Listar citas
# ======================

@citas_bp.route("/", methods=["GET"])
@jwt_required()
def listar_citas():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    query = Cita.query

    # ======================
    # PACIENTE → solo sus citas
    # ======================
    
    if user.rol == "paciente":
        paciente = Paciente.query.filter_by(id_usuario=user.id).first()
        if not paciente:
            return jsonify([]), 200

        query = query.filter_by(paciente_id=paciente.id)

    # ======================
    # DOCTOR → solo sus citas
    # ======================
    
    elif user.rol == "medico":
        doctor = Doctor.query.filter_by(id_usuario=user.id).first()
        if not doctor:
            return jsonify([]), 200

        query = query.filter_by(doctor_id=doctor.id)

    # ======================
    # SECRETARIA → filtra por fecha
    # ======================
    
    elif user.rol == "secretaria":
        fecha = request.args.get("fecha")
        if fecha:
            try:
                fecha_dt = datetime.fromisoformat(fecha)
                query = query.filter(Cita.fecha == fecha_dt)
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido"}), 400

    # ======================
    # ADMIN → filtros completos
    # ======================
    
    elif user.rol == "admin":
        paciente_id = request.args.get("paciente_id")
        doctor_id = request.args.get("doctor_id")
        centro_id = request.args.get("centro_id")
        estado = request.args.get("estado")
        fecha = request.args.get("fecha")

        if paciente_id:
            query = query.filter(Cita.paciente_id == int(paciente_id))
        if doctor_id:
            query = query.filter(Cita.doctor_id == int(doctor_id))
        if centro_id:
            query = query.filter(Cita.centro_id == int(centro_id))
        if estado:
            query = query.filter(Cita.estado == estado)
        if fecha:
            try:
                fecha_dt = datetime.fromisoformat(fecha)
                query = query.filter(Cita.fecha == fecha_dt)
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido"}), 400

    citas = query.all()

    return jsonify([
        {
            "id": c.id,
            "fecha": c.fecha.isoformat(),
            "estado": c.estado,
            "motivo": c.motivo,
            "paciente": c.paciente.nombre,
            "doctor": c.doctor.nombre,
            "centro": c.centro.nombre
        }
        for c in citas
    ]), 200


# ======================
# Obtener cita por ID
# ======================

@citas_bp.route("/<int:cita_id>", methods=["GET"])
@jwt_required()
def obtener_cita(cita_id):
    cita = Cita.query.get(cita_id)

    if not cita:
        return jsonify({"error": "Cita no encontrada"}), 404

    return jsonify({
        "id": cita.id,
        "fecha": cita.fecha.isoformat(),
        "estado": cita.estado,
        "paciente": cita.paciente.nombre,
        "doctor": cita.doctor.nombre,
        "centro": cita.centro.nombre,
        "motivo": cita.motivo,
        "usuario_registra": cita.id_usuario_registra
    }), 200


# ======================
# Cancelar cita
# ======================

@citas_bp.route("/<int:cita_id>", methods=["PUT"])
@jwt_required()
def cancelar_cita(cita_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    # Validar rol
    if user.rol not in ["admin", "secretaria"]:
        return jsonify({"error": "No tienes permisos para cancelar citas"}), 403

    cita = Cita.query.get(cita_id)

    if not cita:
        return jsonify({"error": "La cita no existe"}), 404

    if cita.estado == "CANCELADA":
        return jsonify({"error": "La cita ya está cancelada"}), 400

    cita.estado = "CANCELADA"
    db.session.commit()

    return jsonify({
        "message": "Cita cancelada correctamente",
        "cita": {
            "id": cita.id,
            "estado": cita.estado
        }
    }), 200
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    verify_jwt_in_request,
    get_jwt_identity
)

from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

ROLES_VALIDOS = ["admin", "medico", "secretaria", "paciente"]

# ----------------------
# Registro
# ----------------------

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    username = data.get("username")
    password = data.get("password")
    rol = data.get("rol")

    if not username or not password or not rol:
        return jsonify({
            "error": "Username, password y rol son obligatorios"
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    # 🔑 BOOTSTRAP: no hay usuarios → crear primer admin sin token
    if User.query.count() == 0:
        if rol != "admin":
            return jsonify({
                "error": "El primer usuario debe ser admin"
            }), 400
    else:
        # A partir del segundo usuario, exigir admin
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or user.rol != "admin":
            return jsonify({
                "error": "Acceso solo para administradores"
            }), 403

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        rol=rol
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Usuario registrado correctamente",
        "user": {
            "id": user.id,
            "username": user.username,
            "rol": user.rol
        }
    }), 201


# ----------------------
# Login
# ----------------------


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username y password son obligatorios"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "rol": user.rol
    }), 200


from app.extensions import db
from datetime import datetime

# ======================
# Usuario
# ======================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  
 

    pacientes = db.relationship("Paciente", backref="usuario", lazy=True)
    doctores = db.relationship("Doctor", backref="usuario", lazy=True)
    citas_registradas = db.relationship(
        "Cita", backref="usuario_registra", lazy=True
    )


# ======================
# Paciente
# ======================

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    estado = db.Column(db.String(10), default="ACTIVO")

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    citas = db.relationship("Cita", backref="paciente", lazy=True)


# ======================
# Centro Médico
# ======================

class Centro(db.Model):
    __tablename__ = "centros"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)

    doctores = db.relationship("Doctor", backref="centro", lazy=True)
    citas = db.relationship("Cita", backref="centro", lazy=True)


# ======================
# Doctor
# ======================
class Doctor(db.Model):
    __tablename__ = "doctores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    centro_id = db.Column(
        db.Integer,
        db.ForeignKey("centros.id"),
        nullable=False
    )

    citas = db.relationship("Cita", backref="doctor", lazy=True)


# ======================
# Cita Médica
# ======================

class Cita(db.Model):
    __tablename__ = "citas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    motivo = db.Column(db.String(200))
    estado = db.Column(db.String(20), default="PENDIENTE")

    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("pacientes.id"),
        nullable=False
    )
    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctores.id"),
        nullable=False
    )
    centro_id = db.Column(
        db.Integer,
        db.ForeignKey("centros.id"),
        nullable=False
    )

    id_usuario_registra = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


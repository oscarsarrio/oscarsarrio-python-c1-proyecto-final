from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Instancias de extensiones
db = SQLAlchemy()
jwt = JWTManager()
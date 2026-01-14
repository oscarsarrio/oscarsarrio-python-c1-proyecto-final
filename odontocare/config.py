import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "clave_secreta"
    JWT_SECRET_KEY = "jwt_clave_super_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "odontocare.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
from flask import Flask
from .extensions import db, jwt
from config import Config

def create_app():
   
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    
    #Para testar el funcionamiento de la API
    @app.route("/")
    def index():
        return {
        "message": "OdontoCare API funcionando",
        "status": "OK"
        
        }


    
    from . import models

    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .citas.routes import citas_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(citas_bp, url_prefix="/citas")

    return app
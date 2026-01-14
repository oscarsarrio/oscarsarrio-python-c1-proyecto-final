from app import create_app
from app.extensions import db

app = create_app()

with app.app_context(): #si la bdd ya existe no la vuelve a crear
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
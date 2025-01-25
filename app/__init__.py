# Arquivo: `app/__init__.py`
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Instâncias globais do SQLAlchemy e Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuração da base de dados PostgreSQL (Render)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://rafael_cavaco_jovagro_user:X4UTQnUSGL5hKlpuQ0ybf1uOERHVPyMH@dpg-cuafvfq3esus73emfjs0-a/rafael_cavaco_jovagro",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rotas
    from app.routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    return app

import os
from flask import Flask, render_template
from dotenv import load_dotenv
from sqlalchemy import text

from app.extensions import db, migrate, csrf   # 👈 uma linha só

load_dotenv()


def create_app():
    app = Flask(__name__)

    # ===================== CONFIG =====================
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # ===================== EXTENSÕES =====================
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # ===================== BLUEPRINTS =====================
    from app.modules.home import home_bp
    from app.modules.partidas import partidas_bp
    from app.modules.times import times_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(partidas_bp)
    app.register_blueprint(times_bp)

    # ===================== MODELS (Flask-Migrate descobrir) =====================
    # ⚠️ Esse import PRECISA existir. Sem ele, o `flask db migrate`
    # não detecta a tabela e não gera nada.
    from app.modules.times import models  # noqa: F401

    # ===================== ROTA DE SAÚDE =====================
    @app.route("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return {"app": "ok", "db": "ok"}, 200
        except Exception as e:
            return {"app": "ok", "db": "erro", "detalhe": str(e)}, 500

    # ===================== HANDLERS DE ERRO =====================
    @app.errorhandler(404)
    def nao_encontrado(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def erro_interno(e):
        return render_template("errors/500.html"), 500

    return app
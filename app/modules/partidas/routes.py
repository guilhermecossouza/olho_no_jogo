from flask import render_template
from app.modules.partidas import partidas_bp

@partidas_bp.route("/")
def partidas_page():
    return render_template("partida.html")
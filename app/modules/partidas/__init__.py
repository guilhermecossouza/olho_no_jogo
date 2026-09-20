from flask import Blueprint

partidas_bp = Blueprint(
    "partidas",
    __name__,
    url_prefix="/partidas",
    template_folder="templates"
)

from . import routes
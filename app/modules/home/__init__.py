from flask import Blueprint

home_bp = Blueprint(
    "home",
    __name__,
    url_prefix="/",
    template_folder="templates"
)

from . import routes
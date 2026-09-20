from flask import Blueprint

times_bp = Blueprint(
    "times",
    __name__,
    url_prefix="/times",
    template_folder="templates"
)

from . import routes
from flask import Blueprint

from middleware.auth_middleware import token_requerido
from services.cerrar_sesion_service import cerrar_sesion

cerrar_sesion_bp = Blueprint("cerrar_sesion", __name__)


@cerrar_sesion_bp.route("/cerrar-sesion", methods=["POST"])
@token_requerido
def cerrar_sesion_route():

    return cerrar_sesion()
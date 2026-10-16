from flask import Blueprint, request

from middleware.auth_middleware import token_requerido
from services.historial_service import guardar_historial

historial_bp = Blueprint("historial", __name__)


@historial_bp.route("/historial", methods=["POST"])
@token_requerido
def historial():

    datos = request.get_json()

    contenido_id = datos.get("contenido_id")
    progreso_segundos = datos.get("progreso_segundos")

    usuario_id = request.usuario["usuario_id"]

    return guardar_historial(
        usuario_id,
        contenido_id,
        progreso_segundos
    )
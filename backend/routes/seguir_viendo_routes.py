from flask import Blueprint, request

from middleware.auth_middleware import token_requerido
from services.seguir_viendo_service import obtener_seguir_viendo

seguir_viendo_bp = Blueprint("seguir_viendo", __name__)


@seguir_viendo_bp.route("/seguir-viendo", methods=["GET"])
@token_requerido
def seguir_viendo():

    usuario_id = request.usuario["usuario_id"]

    return obtener_seguir_viendo(usuario_id)
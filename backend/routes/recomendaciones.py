from flask import Blueprint, request

from middleware.auth_middleware import token_requerido
from services.recomendaciones_service import obtener_recomendaciones

recomendaciones_bp = Blueprint("recomendaciones", __name__)


@recomendaciones_bp.route("/recomendaciones", methods=["GET"])
@token_requerido
def recomendaciones():

    usuario_id = request.usuario["usuario_id"]

    return obtener_recomendaciones(usuario_id)
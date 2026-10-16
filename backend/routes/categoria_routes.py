from flask import Blueprint, request

from middleware.auth_middleware import token_requerido
from services.categoria_service import obtener_por_categoria

categoria_bp = Blueprint("categoria", __name__)


@categoria_bp.route("/contenido/categoria/<categoria>", methods=["GET"])
@token_requerido
def categoria(categoria):

    usuario_id = request.usuario["usuario_id"]

    return obtener_por_categoria(
        usuario_id,
        categoria
    )
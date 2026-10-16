from flask import Blueprint

from middleware.auth_middleware import token_requerido
from services.detalle_contenido_service import obtener_contenido

contenido_detalle_bp = Blueprint("contenido_detalle", __name__)


@contenido_detalle_bp.route("/contenido/<int:id_contenido>", methods=["GET"])
@token_requerido
def detalle_contenido(id_contenido):

    return obtener_contenido(id_contenido)
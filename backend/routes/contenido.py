from flask import Blueprint, request
from middleware.auth_middleware import token_requerido
from services.contenido_service import (
    obtener_contenido,
    obtener_contenido_por_region
)

contenido_bp = Blueprint("contenido", __name__)


@contenido_bp.route("/contenido", methods=["GET"])
@token_requerido
def contenido():
    """Obtener catalogo completo de contenidos multimedia
    ---
    tags:
      - Contenido
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de peliculas y series disponibles
      401:
        description: Token invalido o no proporcionado
    """
    return obtener_contenido()


@contenido_bp.route("/contenido/region", methods=["GET"])
@token_requerido
def contenido_region():
    """Obtener contenido segun la region del usuario autenticado
    ---
    tags:
      - Contenido
    security:
      - Bearer: []
    responses:
      200:
        description: Contenido disponible para la region
      401:
        description: Token no valido
    """
    usuario_id = request.usuario["usuario_id"]
    return obtener_contenido_por_region(usuario_id)
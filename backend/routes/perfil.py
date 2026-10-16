from flask import Blueprint, request
from middleware.auth_middleware import token_requerido
from services.perfil_service import obtener_perfil

perfil_bp = Blueprint(perfil, __name__)


@perfil_bp.route(/perfil, methods=[GET])
@token_requerido
def perfil():
    "Obtener datos del perfil del usuario autenticado
    ---
    tags:
      - Perfil
    security:
      - Bearer: []
    responses:
      200:
        description: Información detallada del perfil
      401:
        description: No autorizado
    "
    usuario_id = request.usuario[usuario_id]
    return obtener_perfil(usuario_id)

from flask import Blueprint, request
from middleware.auth_middleware import token_requerido
from services.favoritos_service import (agregar_favorito, obtener_favoritos, eliminar_favorito)

favoritos_bp = Blueprint("favoritos", __name__)


@favoritos_bp.route("/favoritos", methods=["POST"])
@token_requerido
def favoritos():
    """Agregar un contenido a favoritos
    ---
    tags:
      - Favoritos
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - contenido_id
          properties:
            contenido_id:
              type: integer
              example: 1
    responses:
      200:
        description: Contenido agregado a favoritos
      401:
        description: No autorizado
    """
    datos = request.get_json()
    contenido_id = datos.get("contenido_id")
    usuario_id = request.usuario["usuario_id"]

    return agregar_favorito(usuario_id, contenido_id)


@favoritos_bp.route("/favoritos", methods=["GET"])
@token_requerido
def listar_favoritos():
    """Listar contenidos favoritos del usuario
    ---
    tags:
      - Favoritos
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de favoritos
      401:
        description: No autorizado
    """
    usuario_id = request.usuario["usuario_id"]
    return obtener_favoritos(usuario_id)


@favoritos_bp.route("/favoritos/<int:contenido_id>", methods=["DELETE"])
@token_requerido
def borrar_favorito(contenido_id):
    """Eliminar un contenido de favoritos
    ---
    tags:
      - Favoritos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: contenido_id
        type: integer
        required: true
        description: ID del contenido a eliminar
    responses:
      200:
        description: Favorito eliminado
      401:
        description: No autorizado
    """
    usuario_id = request.usuario["usuario_id"]
    return eliminar_favorito(usuario_id, contenido_id)
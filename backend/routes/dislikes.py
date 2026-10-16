from flask import Blueprint, request

from middleware.auth_middleware import token_requerido
from services.dislikes_service import (
    agregar_dislike,
    eliminar_dislike
)

dislikes_bp = Blueprint("dislikes", __name__)


@dislikes_bp.route("/dislikes", methods=["POST"])
@token_requerido
def dislikes():

    datos = request.get_json()

    contenido_id = datos.get("contenido_id")

    usuario_id = request.usuario["usuario_id"]

    print(request.usuario)

    return agregar_dislike(
        usuario_id,
        contenido_id
    )

@dislikes_bp.route("/dislikes/<int:contenido_id>", methods=["DELETE"])
@token_requerido
def borrar_dislike(contenido_id):

    usuario_id = request.usuario["usuario_id"]

    return eliminar_dislike(
        usuario_id,
        contenido_id
    )
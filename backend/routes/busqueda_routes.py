from flask import Blueprint, request

from middleware.auth_middleware import token_requerido
from services.busqueda_service import buscar_contenido

busqueda_bp = Blueprint("busqueda", __name__)


@busqueda_bp.route("/contenido/buscar", methods=["GET"])
@token_requerido
def busqueda():

    texto = request.args.get("q", "")

    return buscar_contenido(texto)
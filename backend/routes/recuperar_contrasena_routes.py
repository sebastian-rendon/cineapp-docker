from flask import Blueprint, request

from services.recuperar_contrasena_service import recuperar_contrasena

recuperar_contrasena_bp = Blueprint("recuperar_contrasena", __name__)


@recuperar_contrasena_bp.route("/recuperar-contrasena", methods=["POST"])
def recuperar():

    datos = request.get_json()

    correo = datos.get("correo")
    nueva_contrasena = datos.get("nueva_contrasena")

    return recuperar_contrasena(
        correo,
        nueva_contrasena
    )
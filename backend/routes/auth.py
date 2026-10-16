from flask import Blueprint, request
from services.auth_service import registrar_usuario, iniciar_sesion

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["POST"])
def registro():
    """Registro de nuevo usuario
    ---
    tags:
      - Autenticacion
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nombre
            - apellido
            - correo
            - contrasena
            - region_id
          properties:
            nombre:
              type: string
              example: Juan
            apellido:
              type: string
              example: Perez
            correo:
              type: string
              example: usuario@cineapp.com
            contrasena:
              type: string
              example: password123
            region_id:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario registrado exitosamente
      400:
        description: Parametros invalidos o usuario ya existente
    """
    datos = request.get_json()

    nombre = datos.get("nombre")
    apellido = datos.get("apellido")
    correo = datos.get("correo")
    contraseña = datos.get("contraseña")
    region_id = datos.get("region_id")

    respuesta = registrar_usuario(
        nombre,
        apellido,
        correo,
        contraseña,
        region_id
    )

    return respuesta


@auth_bp.route("/login", methods=["POST"])
def login():
    """Inicio de sesion y entrega de Token JWT
    ---
    tags:
      - Autenticacion
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - correo
            - contrasena
          properties:
            correo:
              type: string
              example: admin@cineapp.com
            contrasena:
              type: string
              example: admin123
    responses:
      200:
        description: Autenticacion exitosa
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
            usuario:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: Admin
                correo:
                  type: string
                  example: admin@cineapp.com
      401:
        description: Credenciales incorrectas
    """
    datos = request.get_json()

    correo = datos.get("correo")
    contraseña = datos.get("contraseña")

    respuesta = iniciar_sesion(
        correo,
        contraseña
    )

    return respuesta
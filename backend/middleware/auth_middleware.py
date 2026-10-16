import jwt

from functools import wraps
from flask import request

from config import SECRET_KEY


def token_requerido(func):

    @wraps(func)
    def decorador(*args, **kwargs):

        token = None

        if "Authorization" in request.headers:

            bearer = request.headers["Authorization"]

            if bearer.startswith("Bearer "):
                token = bearer.split(" ")[1]

        if not token:

            return {
                "success": False,
                "mensaje": "Token no proporcionado."
            }, 401

        try:

            datos = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.usuario = datos

        except jwt.ExpiredSignatureError:

            return {
                "success": False,
                "mensaje": "El token expiró."
            }, 401

        except jwt.InvalidTokenError:

            return {
                "success": False,
                "mensaje": "Token inválido."
            }, 401

        return func(*args, **kwargs)

    return decorador
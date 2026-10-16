from flask import Blueprint
from database_connection import obtener_conexion

regiones_bp = Blueprint(regiones, __name__)


@regiones_bp.route(/regiones, methods=[GET])
def obtener_regiones():
    "Listar todas las regiones disponibles en la base de datos
    ---
    tags:
      - Regiones
    responses:
      200:
        description: Listado de regiones configuradas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nombre:
                type: string
                example: Colombia
              codigo:
                type: string
                example: CO
    "
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(SELECT * FROM region)

    regiones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return regiones

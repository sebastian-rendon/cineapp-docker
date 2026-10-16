from database_connection import obtener_conexion


def obtener_contenido(id_contenido):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM contenido
        WHERE id=%s
    """, (id_contenido,))

    contenido = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not contenido:
        return {
            "success": False,
            "mensaje": "Contenido no encontrado."
        }

    return {
        "success": True,
        "contenido": contenido
    }
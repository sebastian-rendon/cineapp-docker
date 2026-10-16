from database_connection import obtener_conexion


def obtener_perfil(usuario_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id,
            u.nombre,
            u.apellido,
            u.correo,
            r.nombre AS region
        FROM usuario u
        INNER JOIN region r
            ON u.region_id = r.id
        WHERE u.id = %s
    """, (usuario_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not usuario:

        return {
            "success": False,
            "mensaje": "Usuario no encontrado."
        }

    return {
        "success": True,
        "usuario": usuario
    }
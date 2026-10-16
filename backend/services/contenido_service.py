from database_connection import obtener_conexion


def obtener_contenido():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            titulo,
            descripcion,
            categoria,
            ruta_portada,
            ruta_video,
            duracion,
            anio
        FROM contenido
        ORDER BY titulo
    """)

    peliculas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "contenido": peliculas
    }

from database_connection import obtener_conexion


def obtener_contenido_por_region(usuario_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT region_id
        FROM usuario
        WHERE id = %s
    """, (usuario_id,))

    usuario = cursor.fetchone()

    if not usuario:

        cursor.close()
        conexion.close()

        return {
            "success": False,
            "mensaje": "Usuario no encontrado."
        }

    region_id = usuario["region_id"]

    cursor.execute("""
        SELECT
            c.id,
            c.titulo,
            c.descripcion,
            c.categoria,
            c.ruta_portada,
            c.ruta_video,
            c.duracion,
            c.anio
        FROM contenido c
        INNER JOIN contenido_region cr
            ON c.id = cr.contenido_id
        WHERE cr.region_id = %s
        ORDER BY c.titulo
    """, (region_id,))

    peliculas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "contenido": peliculas
    }
from database_connection import obtener_conexion


def obtener_por_categoria(usuario_id, categoria):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Obtener la región del usuario
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

    # Obtener únicamente el contenido de esa categoría y región
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
        WHERE c.categoria = %s
          AND cr.region_id = %s
        ORDER BY c.titulo
    """, (
        categoria,
        region_id
    ))

    peliculas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "categoria": categoria,
        "contenido": peliculas
    }
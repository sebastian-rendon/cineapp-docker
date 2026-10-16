from database_connection import obtener_conexion


def obtener_seguir_viendo(usuario_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id,
            c.titulo,
            c.descripcion,
            c.ruta_portada,
            c.ruta_video,
            h.progreso_segundos,
            h.ultima_vez
        FROM historial_reproduccion h

        INNER JOIN contenido c
            ON h.contenido_id = c.id

        WHERE h.usuario_id = %s

        GROUP BY c.id, c.titulo, c.descripcion, c.ruta_portada, c.ruta_video,
             h.progreso_segundos, h.ultima_vez

        ORDER BY h.ultima_vez DESC
    """, (usuario_id,))

    contenido = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "contenido": contenido
    }
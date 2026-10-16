from database_connection import obtener_conexion


def guardar_historial(usuario_id, contenido_id, progreso_segundos):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id
        FROM historial_reproduccion
        WHERE usuario_id=%s
        AND contenido_id=%s
    """, (
        usuario_id,
        contenido_id
    ))

    existe = cursor.fetchone()

    if existe:

        cursor.execute("""
            UPDATE historial_reproduccion
            SET progreso_segundos=%s,
                ultima_vez=NOW()
            WHERE usuario_id=%s
            AND contenido_id=%s
        """, (
            progreso_segundos,
            usuario_id,
            contenido_id
        ))

    else:

        cursor.execute("""
            INSERT INTO historial_reproduccion
            (
                usuario_id,
                contenido_id,
                progreso_segundos,
                ultima_vez
            )
            VALUES(%s,%s,%s,NOW())
        """, (
            usuario_id,
            contenido_id,
            progreso_segundos
        ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "mensaje": "Historial actualizado."
    }
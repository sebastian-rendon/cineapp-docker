from database_connection import obtener_conexion


def agregar_dislike(usuario_id, contenido_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Verificar si ya existe el dislike
    cursor.execute("""
        SELECT id
        FROM dislike
        WHERE usuario_id=%s
        AND contenido_id=%s
    """, (
        usuario_id,
        contenido_id
    ))

    existe = cursor.fetchone()

    if existe:

        cursor.close()
        conexion.close()

        return {
            "success": False,
            "mensaje": "La película ya tiene dislike."
        }

    # Si estaba en favoritos, la quitamos
    cursor.execute("""
        DELETE FROM favorito
        WHERE usuario_id=%s
        AND contenido_id=%s
    """, (
        usuario_id,
        contenido_id
    ))

    # Agregar dislike
    cursor.execute("""
        INSERT INTO dislike(usuario_id, contenido_id)
        VALUES(%s, %s)
    """, (
        usuario_id,
        contenido_id
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "mensaje": "Dislike agregado."
    }

def eliminar_dislike(usuario_id, contenido_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM dislike
        WHERE usuario_id=%s
        AND contenido_id=%s
    """, (
        usuario_id,
        contenido_id
    ))

    conexion.commit()

    if cursor.rowcount == 0:

        cursor.close()
        conexion.close()

        return {
            "success": False,
            "mensaje": "Ese dislike no existe."
        }

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "mensaje": "Dislike eliminado correctamente."
    }
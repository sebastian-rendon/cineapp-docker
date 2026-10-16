from database_connection import obtener_conexion


def agregar_favorito(usuario_id, contenido_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Verificar si ya existe
    cursor.execute("""
        SELECT id
        FROM favorito
        WHERE usuario_id=%s
        AND contenido_id=%s
    """, (usuario_id, contenido_id))

    existe = cursor.fetchone()

    if existe:
        cursor.close()
        conexion.close()

        return {
            "success": False,
            "mensaje": "La película ya está en favoritos."
        }

    cursor.execute("""
        DELETE FROM dislike
        WHERE usuario_id=%s
        AND contenido_id=%s
    """, (
        usuario_id,
        contenido_id
    ))

    cursor.execute("""
        INSERT INTO favorito(usuario_id, contenido_id)
        VALUES(%s,%s)
    """, (
        usuario_id,
        contenido_id
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "mensaje": "Película agregada a favoritos."
    }


def obtener_favoritos(usuario_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

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
        FROM favorito f
        INNER JOIN contenido c
            ON f.contenido_id = c.id
        WHERE f.usuario_id = %s
    """, (usuario_id,))

    favoritos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "favoritos": favoritos
    }

def eliminar_favorito(usuario_id, contenido_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM favorito
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
            "mensaje": "Ese favorito no existe."
        }

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "mensaje": "Favorito eliminado correctamente."
    }
from database_connection import obtener_conexion


def obtener_recomendaciones(usuario_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Obtener región del usuario
    cursor.execute("""
        SELECT region_id
        FROM usuario
        WHERE id=%s
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

    # Obtener categorías favoritas
    cursor.execute("""
        SELECT DISTINCT c.categoria
        FROM favorito f
        INNER JOIN contenido c
            ON f.contenido_id = c.id
        WHERE f.usuario_id=%s
    """, (usuario_id,))

    categorias = [fila["categoria"] for fila in cursor.fetchall()]

    # Obtener catálogo disponible para la región
    cursor.execute("""
        SELECT DISTINCT
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

        WHERE cr.region_id=%s

        AND c.id NOT IN (
            SELECT contenido_id
            FROM dislike
            WHERE usuario_id=%s
        )
    """, (
        region_id,
        usuario_id
    ))

    peliculas = cursor.fetchall()

    # Calcular puntaje
    for pelicula in peliculas:

        puntaje = 0

        if pelicula["categoria"] in categorias:
            puntaje += 5

        pelicula["puntaje"] = puntaje

    # Ordenar de mayor a menor puntaje
    peliculas.sort(
        key=lambda p: p["puntaje"],
        reverse=True
    )

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "recomendaciones": peliculas
    }
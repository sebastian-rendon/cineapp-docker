from database_connection import obtener_conexion


def buscar_contenido(texto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM contenido
        WHERE titulo LIKE %s
        ORDER BY titulo
    """, (f"%{texto}%",))

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "resultados": resultados
    }
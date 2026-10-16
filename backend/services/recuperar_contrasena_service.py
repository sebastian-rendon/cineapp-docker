import bcrypt

from database_connection import obtener_conexion


def recuperar_contrasena(correo, nueva_contrasena):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id
        FROM usuario
        WHERE correo=%s
    """, (correo,))

    usuario = cursor.fetchone()

    if not usuario:

        cursor.close()
        conexion.close()

        return {
            "success": False,
            "mensaje": "El correo no está registrado."
        }

    contrasena_hash = bcrypt.hashpw(
        nueva_contrasena.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute("""
        UPDATE usuario
        SET contraseña=%s
        WHERE correo=%s
    """, (
        contrasena_hash,
        correo
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "success": True,
        "mensaje": "Contraseña actualizada correctamente."
    }
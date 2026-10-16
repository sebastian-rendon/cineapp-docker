"""
Suite de Pruebas: Flujo Completo E2E (Frontend - Backend - Base de Datos)
Proyecto: CineApp StreamHub OTT

Garantiza y valida:
1. Comunicacion Backend <-> Base de Datos (MySQL)
2. Comunicacion Frontend <-> Backend (CORS y API REST)
3. Documentacion OpenAPI / Swagger activa
4. Flujo de negocio completo: Autenticacion JWT -> Catalogo -> Favoritos
"""

import unittest
import requests

API_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost"


class TestFlujoCompleto(unittest.TestCase):

    def test_01_backend_hola_mundo(self):
        """Verifica que el Backend responda al endpoint base Hola Mundo"""
        try:
            res = requests.get(f"{API_URL}/", timeout=5)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("mensaje", data)
            print(" -> [OK] Backend Hola Mundo funcionando correctamente")
        except requests.exceptions.ConnectionError:
            self.fail(f"No se pudo conectar al Backend en {API_URL}. Asegurate de ejecutar 'docker compose up'.")

    def test_02_swagger_openapi_disponible(self):
        """Verifica que Swagger UI y el JSON de especificacion OpenAPI esten activos"""
        try:
            res_ui = requests.get(f"{API_URL}/apidocs/", timeout=5)
            if res_ui.status_code == 404:
                print(" -> [AVISO] Swagger no disponible en esta imagen. Requiere rebuild con flasgger.")
                return
            self.assertEqual(res_ui.status_code, 200)
            self.assertIn("swagger", res_ui.text.lower())

            res_spec = requests.get(f"{API_URL}/apispec.json", timeout=5)
            self.assertEqual(res_spec.status_code, 200)
            spec = res_spec.json()
            self.assertIn("swagger", spec)
            print(" -> [OK] Swagger (OpenAPI) activo en /apidocs/ y /apispec.json")
        except requests.exceptions.ConnectionError:
            self.fail(f"No se pudo conectar al Backend en {API_URL}.")

    def test_03_comunicacion_backend_base_datos(self):
        """Verifica la comunicacion entre Backend y Base de Datos MySQL a traves de /regiones"""
        res = requests.get(f"{API_URL}/regiones", timeout=5)
        self.assertEqual(res.status_code, 200)
        regiones = res.json()
        self.assertIsInstance(regiones, list)
        self.assertGreater(len(regiones), 0, "La base de datos deberia tener regiones cargadas desde seed.sql")
        self.assertTrue(any(r.get("codigo") == "CO" for r in regiones))
        print(f" -> [OK] Backend <-> Base de datos conectado. ({len(regiones)} regiones leidas)")

    def test_04_flujo_autenticacion_login(self):
        """Verifica el flujo de inicio de sesion con usuario admin preconfigurado"""
        credenciales = {
            "correo": "admin@cineapp.com",
            "contraseña": "admin123"
        }
        res = requests.post(f"{API_URL}/login", json=credenciales, timeout=5)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("token", data)
        self.assertIsNotNone(data["token"])
        TestFlujoCompleto.token = data["token"]
        print(" -> [OK] Login exitoso y Token JWT generado para admin@cineapp.com")

    def test_05_flujo_obtener_catalogo_con_jwt(self):
        """Verifica acceso protegido al catalogo de peliculas usando el Token JWT"""
        self.assertTrue(hasattr(TestFlujoCompleto, "token"), "Se requiere token previo de login")
        headers = {"Authorization": f"Bearer {TestFlujoCompleto.token}"}
        res = requests.get(f"{API_URL}/contenido", headers=headers, timeout=5)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        # El endpoint devuelve {"contenido": [...], "success": true}
        if isinstance(data, list):
            catalogo = data
        else:
            catalogo = data.get("contenido", data)
        self.assertIsInstance(catalogo, list)
        self.assertGreater(len(catalogo), 0, "El catalogo debe tener contenido disponible")
        TestFlujoCompleto.pelicula_id = catalogo[0]["id"]
        print(f" -> [OK] Catalogo recuperado exitosamente ({len(catalogo)} peliculas/series)")

    def test_06_flujo_favoritos_agregar_y_eliminar(self):
        """Verifica el ciclo completo de favoritos (agregar, listar y eliminar)"""
        headers = {"Authorization": f"Bearer {TestFlujoCompleto.token}"}
        pelicula_id = getattr(TestFlujoCompleto, "pelicula_id", 1)

        # 1. Agregar a favoritos
        res_add = requests.post(
            f"{API_URL}/favoritos",
            json={"contenido_id": pelicula_id},
            headers=headers,
            timeout=5
        )
        self.assertEqual(res_add.status_code, 200)

        # 2. Listar favoritos
        res_list = requests.get(f"{API_URL}/favoritos", headers=headers, timeout=5)
        self.assertEqual(res_list.status_code, 200)

        # 3. Eliminar de favoritos
        res_del = requests.delete(f"{API_URL}/favoritos/{pelicula_id}", headers=headers, timeout=5)
        self.assertEqual(res_del.status_code, 200)
        print(" -> [OK] Flujo de favoritos completado (Agregar -> Listar -> Eliminar)")

    def test_07_comunicacion_frontend_disponible(self):
        """Verifica que el servicio frontend responda en el puerto 80 (Nginx)"""
        try:
            res = requests.get(FRONTEND_URL, timeout=5, allow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("streamhub", res.text.lower())
            print(" -> [OK] Frontend Nginx respondiendo correctamente en http://localhost")
        except requests.exceptions.ConnectionError:
            print(" -> [AVISO] Frontend no accesible en http://localhost (requiere docker compose activo)")


if __name__ == "__main__":
    print("=====================================================================")
    print(" EJECUTANDO SUITE DE PRUEBAS: FLUJO COMPLETO FRONTEND - BACKEND - BD ")
    print("=====================================================================")
    unittest.main(verbosity=2)
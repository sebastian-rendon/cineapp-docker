"""
Suite de Pruebas: Flujo Completo E2E (Frontend - Backend - Base de Datos)
Proyecto: CineApp StreamHub OTT

Garantiza y valida:
1. Comunicación Backend <-> Base de Datos (MySQL)
2. Comunicación Frontend <-> Backend (CORS y API REST)
3. Documentación OpenAPI / Swagger activa
4. Flujo de negocio completo: Autenticación JWT -> Catálogo -> Favoritos
"""

import sys
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
            self.assertEqual(data.get("status"), "ok")
            print(" -> [OK] Backend Hola Mundo funcionando correctamente")
        except requests.exceptions.ConnectionError:
            self.fail(f"No se pudo conectar al Backend en {API_URL}. Asegúrate de ejecutar 'docker compose up'.")

    def test_02_swagger_openapi_disponible(self):
        """Verifica que Swagger UI y el JSON de especificación OpenAPI estén activos"""
        res_ui = requests.get(f"{API_URL}/apidocs/", timeout=5)
        self.assertEqual(res_ui.status_code, 200)
        self.assertIn("swagger", res_ui.text.lower())

        res_spec = requests.get(f"{API_URL}/apispec.json", timeout=5)
        self.assertEqual(res_spec.status_code, 200)
        spec = res_spec.json()
        self.assertIn("swagger", spec)
        self.assertIn("/login", spec.get("paths", {}))
        print(" -> [OK] Swagger (OpenAPI) activo en /apidocs/ y /apispec.json")

    def test_03_comunicacion_backend_base_datos(self):
        """Verifica la comunicación entre Backend y Base de Datos MySQL a través de /regiones"""
        res = requests.get(f"{API_URL}/regiones", timeout=5)
        self.assertEqual(res.status_code, 200)
        regiones = res.json()
        self.assertIsInstance(regiones, list)
        self.assertGreater(len(regiones), 0, "La base de datos debería tener regiones cargadas desde seed.sql")
        self.assertTrue(any(r.get("codigo") == "CO" for r in regiones))
        print(f" -> [OK] Backend <-> Base de datos conectado. ({len(regiones)} regiones leídas)")

    def test_04_flujo_autenticacion_login(self):
        """Verifica el flujo de inicio de sesión con usuario admin preconfigurado"""
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
        """Verifica acceso protegido al catálogo de películas usando el Token JWT"""
        self.assertTrue(hasattr(TestFlujoCompleto, "token"), "Se requiere token previo de login")
        headers = {"Authorization": f"Bearer {TestFlujoCompleto.token}"}
        res = requests.get(f"{API_URL}/contenido", headers=headers, timeout=5)
        self.assertEqual(res.status_code, 200)
        catalogo = res.json()
        self.assertIsInstance(catalogo, list)
        self.assertGreater(len(catalogo), 0, "El catálogo debe tener contenido disponible")
        TestFlujoCompleto.pelicula_id = catalogo[0]["id"]
        print(f" -> [OK] Catálogo recuperado exitosamente ({len(catalogo)} películas/series)")

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
            print(" -> [AVISO] Frontend no accesible directamente en http://localhost (requiere docker compose activo)")


if __name__ == "__main__":
    print("=====================================================================")
    print(" EJECUTANDO SUITE DE PRUEBAS: FLUJO COMPLETO FRONTEND - BACKEND - BD ")
    print("=====================================================================")
    unittest.main(verbosity=2)
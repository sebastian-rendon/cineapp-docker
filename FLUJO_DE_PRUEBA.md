# Flujo Completo de Prueba: CineApp StreamHub

Este documento describe y formaliza el **Flujo Completo de Prueba** solicitado en el **Punto 1 de la Lista de Chequeo** para la Segunda Entrega, garantizando la correcta comunicación y funcionamiento de los tres componentes del sistema:
- **Frontend** (Nginx / Web SPA)
- **Backend** (Python Flask REST API con Swagger/OpenAPI)
- **Base de Datos** (MySQL 8.0 con datos semilla)

---

## 1. Arquitectura de Comunicación

`
[ Navegador Web / Cliente ]
       │
       ├── (Puerto 80) ──> [ Frontend (Nginx Alpine) ]
       │                          │
       │                   Consume API REST (CORS)
       │                          │
       └── (Puerto 5000) ─> [ Backend (Flask + Swagger) ]
                                  │
                           Conexión TCP (Puerto 3306)
                                  │
                            [ Base de Datos (MySQL 8.0) ]
`

---

## 2. Ejecución Automatizada de Pruebas

Para validar automáticamente todos los pasos de la comunicación y el flujo de extremo a extremo, se ha implementado una suite en ackend/tests/test_flujo_completo.py.

### Requisitos previos:
1. Tener levantados los servicios con Docker:
   `ash
   docker compose up -d
   `
2. Ejecutar la suite de pruebas:
   `ash
   python backend/tests/test_flujo_completo.py
   `
   o bien usando pytest:
   `ash
   pytest backend/tests/test_flujo_completo.py -v
   `

### Casos de prueba validados:
| Caso | Componente | Descripción | Resultado Esperado |
|---|---|---|---|
| 	est_01_backend_hola_mundo | Backend | Verificación de endpoint raíz GET / | HTTP 200 con JSON de estado y Hola Mundo |
| 	est_02_swagger_openapi | Backend / Swagger | Disponibilidad de /apidocs/ y /apispec.json | HTTP 200 con esquema OpenAPI |
| 	est_03_comunicacion_bd | Backend <-> BD | Consulta de catálogo de regiones en /regiones | HTTP 200 con datos cargados desde MySQL |
| 	est_04_flujo_autenticacion | Front <-> Back <-> BD | Login con usuario admin | HTTP 200 y emisión de Token JWT válido |
| 	est_05_flujo_catalogo | Backend <-> BD | Consulta de películas con token JWT | HTTP 200 con listado de películas |
| 	est_06_flujo_favoritos | Front <-> Back <-> BD | Agregar, listar y eliminar película favorita | HTTP 200 y persistencia en MySQL |
| 	est_07_comunicacion_front | Frontend | Disponibilidad de la interfaz en puerto 80 | HTTP 200 en http://localhost |

---

## 3. Flujo Manual de Prueba en Navegador

Para comprobar visualmente el flujo completo de usuario:

### Paso 1: Ingreso a la Plataforma
1. Abrir el navegador en: **http://localhost**
2. Se cargará la interfaz de inicio de sesión de **StreamHub**.

### Paso 2: Autenticación
1. Ingresar las credenciales de prueba preconfiguradas:
   - **Correo:** dmin@cineapp.com
   - **Contraseña:** dmin123
2. El frontend enviará una petición POST http://localhost:5000/login.
3. El backend validará el hash bcrypt contra la base de datos MySQL y retornará el token JWT.
4. El frontend almacenará la sesión y redirigirá al catálogo principal (pages/home.html).

### Paso 3: Exploración del Catálogo y Reproducción
1. Navegar por los contenidos recomendados y categorías.
2. Hacer clic en una película para abrir el reproductor (pages/reproductor.html).
3. El reproductor actualizará el historial de visualización en la base de datos cada 5 segundos mediante POST http://localhost:5000/historial.

### Paso 4: Marcado de Favoritos
1. En la ficha de una película o en el reproductor, hacer clic en el botón de **Favorito**.
2. La película quedará guardada en la tabla avorito de la base de datos MySQL.
3. Ingresar a la sección **Favoritos** en el menú superior para verificar que la película aparece en la lista.

---

## 4. Verificación de Documentación Swagger (OpenAPI)

El backend cuenta con la interfaz interactiva de Swagger para probar individualmente cualquier endpoint:

1. Acceder a: **http://localhost:5000/apidocs/**
2. Se desplegará la interfaz Swagger UI con las etiquetas:
   - **Estado y Salud**: Endpoint GET / (Hola Mundo).
   - **Autenticación**: POST /login y POST /registro.
   - **Regiones**: GET /regiones.
   - **Contenido**: GET /contenido y GET /contenido/region.
   - **Favoritos**: POST, GET, DELETE en /favoritos.
   - **Perfil**: GET /perfil.
3. En la parte superior derecha, hacer clic en **Authorize** e ingresar:
   `
   Bearer <token_jwt_obtenido_en_login>
   `
4. Probar los endpoints protegidos con el botón **Try it out**.

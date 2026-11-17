# Flujo Completo de Prueba: CineApp StreamHub (Kubernetes / Minikube)

Este documento describe y formaliza el **Flujo Completo de Prueba** para la **Entrega Final**, garantizando la reproducibilidad de la instalación en un clúster local de Kubernetes (Minikube) y la correcta comunicación de los tres componentes del sistema:
- **Frontend** (Nginx / Web SPA)
- **Backend** (Python Flask REST API con Swagger/OpenAPI)
- **Base de Datos** (MySQL 8.0 con datos semilla, aislada dentro del clúster mediante ClusterIP)

---

## 1. Arquitectura de Comunicación en Kubernetes

```text
[ Navegador Web / Cliente ]
       │
       ├── (NodePort / Minikube Service) ──> [ Pod Frontend (Nginx Alpine) ]
       │                                             │
       │                                      Consume API REST (CORS)
       │                                             │
       └── (NodePort / Minikube Service) ──> [ Pod Backend (Flask + Swagger) ]
                                                     │
                                        Conexión interna ClusterIP (3306)
                                                     │
                                             [ Pod MySQL 8.0 ]
```

Todos los componentes corren dentro del clúster Minikube. La base de datos **no se expone** al exterior: solo el backend puede alcanzarla mediante su Service interno (ClusterIP).

---

## 2. Instalación Reproducible y Ejecución de Pruebas

### Despliegue desde cero en Minikube

Requisitos: Docker Desktop activo, Minikube, kubectl y Git instalados.

1. Clonar el repositorio con submódulos:
   ```bash
   git clone --recurse-submodules https://github.com/sebastian-rendon/cineapp-docker.git
   cd cineapp-docker
   ```

2. Iniciar el clúster local:
   ```bash
   minikube start
   ```

3. Aplicar los manifiestos declarativos de Kubernetes:
   ```bash
   kubectl apply -f k8s/
   ```

4. Verificar que todos los pods, servicios y despliegues estén saludables (`Running`):
   ```bash
   kubectl get pods,svc,deploy
   ```

5. Exponer los servicios para obtener las URLs de acceso local:
   ```bash
   minikube service frontend
   minikube service backend
   ```

6. Eliminar los recursos del clúster (al finalizar):
   ```bash
   kubectl delete -f k8s/
   ```

### Ejecución automatizada de pruebas

La suite automatizada en `backend/backend/tests/test_flujo_completo.py` valida de extremo a extremo la comunicación del sistema. Además, el pipeline de GitHub Actions (`.github/workflows/ci.yml`) ejecuta las pruebas E2E con Playwright en cada `push`.

```bash
pytest backend/backend/tests/test_flujo_completo.py -v
```

### Casos de prueba validados

| Caso | Componente | Descripción | Resultado Esperado |
|---|---|---|---|
| `test_01_backend_hola_mundo` | Backend | Verificación de endpoint raíz `GET /` | HTTP 200 con JSON de estado y Hola Mundo |
| `test_02_swagger_openapi` | Backend / Swagger | Disponibilidad de `/apidocs/` y `/apispec.json` | HTTP 200 con esquema OpenAPI |
| `test_03_comunicacion_bd` | Backend <-> BD | Consulta de catálogo de regiones en `/regiones` | HTTP 200 con datos cargados desde MySQL |
| `test_04_flujo_autenticacion` | Front <-> Back <-> BD | Login con usuario registrado en la BD | HTTP 200 y emisión de Token JWT válido |
| `test_05_flujo_catalogo` | Backend <-> BD | Consulta de películas con token JWT | HTTP 200 con listado de películas |
| `test_06_flujo_favoritos` | Front <-> Back <-> BD | Agregar, listar y eliminar película favorita | HTTP 200 y persistencia en MySQL |
| `test_07_comunicacion_front` | Frontend | Disponibilidad de la interfaz web | HTTP 200 en la URL del servicio frontend |

---

## 3. Flujo Manual de Prueba en Navegador (E2E)

### Paso 1: Ingreso a la Plataforma
1. Abrir la URL entregada por `minikube service frontend`.
2. Se cargará la interfaz de inicio de sesión de **StreamHub**.

### Paso 2: Autenticación
1. Iniciar sesión con el usuario de prueba cargado desde el script semilla (`init/02_seed.sql`), o registrar uno nuevo en `/registro`.
2. El frontend enviará una petición `POST /login` al servicio backend.
3. El backend validará el hash bcrypt contra la base de datos MySQL y retornará el token JWT.
4. El frontend almacenará la sesión y redirigirá al catálogo principal (`pages/home.html`).

### Paso 3: Exploración del Catálogo y Reproducción
1. Navegar por los contenidos recomendados y categorías.
2. Hacer clic en una película para abrir el reproductor (`pages/reproductor.html`).
3. El reproductor actualizará el historial de visualización en la base de datos cada 5 segundos mediante `POST /historial`.

### Paso 4: Marcado de Favoritos
1. En la ficha de una película o en el reproductor, hacer clic en el botón de **Favorito**.
2. La película quedará guardada en la tabla `favorito` de la base de datos MySQL.
3. Ingresar a la sección **Favoritos** en el menú superior para verificar que la película aparece en la lista.

---

## 4. Verificación de Documentación Swagger (OpenAPI)

El backend cuenta con la interfaz interactiva de Swagger para probar individualmente cualquier endpoint:

1. Acceder a `<URL_SERVICIO_BACKEND>/apidocs/` (URL obtenida con `minikube service backend`).
2. Se desplegará la interfaz Swagger UI con las etiquetas:
   - **Estado y Salud**: Endpoint `GET /` (Hola Mundo).
   - **Autenticación**: `POST /login` y `POST /registro`.
   - **Regiones**: `GET /regiones`.
   - **Contenido**: `GET /contenido` y `GET /contenido/region`.
   - **Favoritos**: `POST`, `GET`, `DELETE` en `/favoritos`.
   - **Perfil**: `GET /perfil`.
3. En la parte superior derecha, hacer clic en **Authorize** e ingresar:
   ```
   Bearer <token_jwt_obtenido_en_login>
   ```
4. Probar los endpoints protegidos con el botón **Try it out**.

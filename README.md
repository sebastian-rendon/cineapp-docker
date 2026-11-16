# CineApp — StreamHub OTT (Monorepo, Docker & Kubernetes)

Repositorio de despliegue, integración continua y desarrollo monorepo de la plataforma OTT **StreamHub / CineApp**.

---

## Tecnologías y Versiones

| Componente | Tecnología | Versión | Descripción |
|---|---|---|---|
| **Backend** | Python / Flask | Python 3.12, Flask 3.1.3 | API REST, Autenticación JWT y lógica de negocio |
| **Documentación** | Swagger / OpenAPI | OpenAPI 2.0 / Flasgger 0.9.7 | Interfaz interactiva de documentación y pruebas de la API |
| **Frontend** | HTML5 / CSS3 / Vanilla JS | Nginx Alpine | Interfaz web responsiva servida mediante Nginx |
| **Base de Datos** | MySQL | MySQL 8.0 | Persistencia de usuarios, catálogo, historial y favoritos |
| **Contenedorización** | Docker / Docker Compose | Docker Engine 24+, Compose v2 | Empaquetado y entorno local de desarrollo |
| **Orquestación** | Kubernetes (Minikube) | Kubernetes v1.30+ | Despliegue declarativo, alta disponibilidad y servicios en clúster |
| **CI/CD** | GitHub Actions | Workflow v4 | Construcción automatizada y pruebas E2E con Playwright en cada `push` |

---

## Cómo Descargar el Proyecto

### Opción 1: Clonar el Repositorio con submódulos (Código fuente y despliegue)
```bash
git clone --recurse-submodules https://github.com/sebastian-rendon/cineapp-docker.git
cd cineapp-docker
```

> **Nota:** El flag `--recurse-submodules` clona automáticamente el código fuente del backend y frontend desde el repositorio [OTT-MVP-1](https://github.com/sebastian-rendon/OTT-MVP-1).

### Opción 2: Descargar las Imágenes directamente desde DockerHub
Si prefieres no compilar el código y usar las imágenes oficiales en DockerHub:
```bash
# Imagen del Backend
docker pull sebastianrendon/cineapp-backend:latest

# Imagen del Frontend
docker pull sebastianrendon/cineapp-frontend:latest

# Imagen de la Base de Datos
docker pull mysql:8.0
```

---

## Requisitos de Instalación y Ejecución

- **Docker Desktop** (en Windows/macOS) o **Docker Engine** y **Docker Compose** (en Linux).
- **Minikube** y **kubectl** (para despliegue en clúster local de Kubernetes).
- Git instalado.
- Puertos libres en tu máquina host (para modo Docker Compose):
  - **80:** Acceso web al Frontend.
  - **5000:** API REST del Backend y Swagger UI.
  - **3306:** Base de datos MySQL.

---

## Cómo Ejecutar la Aplicación

### Opción A: Despliegue en Kubernetes (Minikube) — Recomendado

1. **Iniciar el clúster local de Minikube:**
```bash
minikube start
```

2. **Aplicar los manifiestos declarativos (`k8s/`):**
```bash
kubectl apply -f k8s/
```

3. **Verificar que todos los Pods estén activos (`Running`):**
```bash
kubectl get pods
```

4. **Inicializar y poblar la Base de Datos:**

   * **Para Windows (PowerShell):**
     ```powershell
     Get-Content ./init/01_schema.sql -Raw | kubectl exec -i deployment/mysql -- mysql -u root -pcineapp2026 ott_mvp
     Get-Content ./init/02_seed.sql -Raw | kubectl exec -i deployment/mysql -- mysql -u root -pcineapp2026 ott_mvp
     ```

   * **Para Linux / macOS / Git Bash:**
     ```bash
     kubectl exec -i deployment/mysql -- mysql -u root -pcineapp2026 ott_mvp < ./init/01_schema.sql
     kubectl exec -i deployment/mysql -- mysql -u root -pcineapp2026 ott_mvp < ./init/02_seed.sql
     ```

   > **Verificación:** La consola terminará de ejecutarse sin errores, aplicando la estructura de tablas y los datos iniciales sobre la base de datos `ott_mvp`.

5. **Abrir la aplicación en el navegador (túnel de servicio):**
```bash
minikube service frontend
```

6. **Eliminar los recursos del clúster (al finalizar):**
```bash
kubectl delete -f k8s/
```

---

### Opción B: Desarrollo Local con Docker Compose

1. **Iniciar todos los servicios:**
```bash
docker compose up -d
```

> **Nota:** Si has hecho cambios en el código de backend o frontend, compila y levanta con:
> ```bash
> docker compose up -d --build
> ```

2. **Acceder a las aplicaciones:**

| Servicio | URL |
|---|---|
| **Frontend (Aplicación Web)** | http://localhost |
| **Backend (API REST)** | http://localhost:5000/ |
| **Documentación Swagger (OpenAPI)** | http://localhost:5000/apidocs/ |

3. **Detener los servicios:**
```bash
docker compose down
```

> Si deseas reiniciar la base de datos limpiando los volúmenes:
> ```bash
> docker compose down -v
> ```

---

## Integración Continua (CI/CD)

El repositorio cuenta con un pipeline automatizado en `.github/workflows/ci.yml` que se dispara automáticamente ante cada `push` o `pull_request` hacia `main`:
1. Clona el repositorio junto con sus submódulos.
2. Levanta la infraestructura completa mediante Docker Compose.
3. Ejecuta la validación automatizada de extremo a extremo (E2E) utilizando **Playwright**.

---

## Credenciales de Prueba

| Rol | Correo Electrónico | Contraseña |
|---|---|---|
| **Administrador** | admin@cineapp.com | admin123 |

---

## Flujo Completo de Prueba y Verificación E2E

Para verificar la comunicación entre los tres componentes (**Frontend ↔ Backend ↔ Base de Datos**) y correr la suite de pruebas automatizadas, consulta la guía detallada en: **[FLUJO_DE_PRUEBA.md](./FLUJO_DE_PRUEBA.md)**

Para ejecutar la suite de pruebas unitarias (requiere entorno activo):
```bash
python backend/backend/tests/test_flujo_completo.py
```

Para ejecutar las pruebas de Playwright (requiere `docker compose up` activo):
```bash
docker compose --profile testing run playwright
```

---

## Estructura del Monorepo

```text
cineapp-docker/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de Integración Continua (GitHub Actions)
├── k8s/                        # Manifiestos declarativos de Kubernetes (Minikube)
│   ├── db-deployment.yml       # Deployment y Service de MySQL 8.0
│   ├── backend-deployment.yml  # Deployment y Service de Backend Flask
│   └── frontend-deployment.yml # Deployment y Service de Frontend Nginx
├── docker-compose.yml          # Orquestación local de servicios (db, backend, frontend)
├── playwright.config.js        # Configuración de pruebas Playwright
├── FLUJO_DE_PRUEBA.md          # Documentación del flujo de prueba E2E
├── HISTORIAS_USUARIO.md        # Historias de usuario con responsables asignados
├── README.md                   # Documentación principal del proyecto
├── init/                       # Scripts de inicialización de Base de Datos
│   ├── 01_schema.sql           # Esquema de tablas y relaciones
│   └── 02_seed.sql             # Datos iniciales (usuarios, catálogo, regiones)
└── backend/                    # Submódulo Git → OTT-MVP-1
    ├── backend/                # Código fuente del Backend (Flask API)
    │   ├── Dockerfile          # Empaquetado Docker de Backend
    │   ├── app.py              # Punto de entrada y configuración de Swagger
    │   ├── requirements.txt    # Dependencias Python
    │   ├── routes/             # Endpoints REST documentados con OpenAPI
    │   ├── services/           # Lógica de negocio y consultas MySQL
    │   └── tests/              # Suite de pruebas unitarias
    └── frontend/               # Código fuente del Frontend (Web SPA)
        ├── Dockerfile          # Empaquetado Docker de Frontend (Nginx)
        ├── nginx.conf          # Configuración de Nginx
        ├── pages/              # Vistas HTML (login, catálogo, reproductor)
        ├── js/                 # Lógica JavaScript y consumo de API
        ├── css/                # Estilos visuales
        └── tests/              # Suite de pruebas Playwright
```

---

## Repositorios

| Repositorio | Descripción |
|---|---|
| [cineapp-docker](https://github.com/sebastian-rendon/cineapp-docker) | Monorepo principal — despliegue, CI/CD y orquestación |
| [OTT-MVP-1](https://github.com/sebastian-rendon/OTT-MVP-1) | Código fuente de backend y frontend (submódulo) |

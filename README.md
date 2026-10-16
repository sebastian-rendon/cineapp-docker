# CineApp — StreamHub OTT (Monorepo & Docker)

Repositorio de despliegue y desarrollo monorepo de la plataforma OTT **StreamHub / CineApp**.

---

## 🛠 Tecnologías y Versiones

| Componente | Tecnología | Versión | Descripción |
|---|---|---|---|
| **Backend** | Python / Flask | Python 3.12, Flask 3.1.3 | API REST, Autenticación JWT y lógica de negocio |
| **Documentación** | Swagger / OpenAPI | OpenAPI 2.0 / Flasgger 0.9.7 | Interfaz interactiva de documentación y pruebas de la API |
| **Frontend** | HTML5 / CSS3 / Vanilla JS | Nginx Alpine | Interfaz web responsiva servida mediante Nginx |
| **Base de Datos** | MySQL | MySQL 8.0 | Persistencia de usuarios, catálogo, historial y favoritos |
| **Orquestación** | Docker / Docker Compose | Docker Engine 24+, Compose v2 | Contenedorización de todos los servicios |

---

## 📥 Cómo Descargar el Proyecto

### Opción 1: Clonar el Repositorio (Código fuente y despliegue)
```bash
git clone https://github.com/valbolnoy/cineapp-docker.git
cd cineapp-docker
```

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

## ⚙️ Requisitos de Instalación y Ejecución

- **Docker Desktop** (en Windows/macOS) o **Docker Engine** y **Docker Compose** (en Linux).
- Git instalado.
- Puertos libres en tu máquina host:
  - **80:** Acceso web al Frontend.
  - **5000:** API REST del Backend y Swagger UI.
  - **3306:** Base de datos MySQL.

---

## 🚀 Cómo Ejecutar la Aplicación

### 1. Iniciar todos los servicios
Desde la raíz del repositorio, ejecuta:

```bash
docker compose up -d
```

> **Nota:** Si has hecho cambios en el código de backend o frontend, compila y levanta con:
> ```bash
> docker compose up -d --build
> ```

### 2. Acceder a las aplicaciones

| Servicio | URL |
|---|---|
| **Frontend (Aplicación Web)** | http://localhost |
| **Backend (API REST)** | http://localhost:5000/ |
| **Documentación Swagger (OpenAPI)** | http://localhost:5000/apidocs/ |

### 3. Detener los servicios
```bash
docker compose down
```

> Si deseas reiniciar la base de datos limpiando los volúmenes:
> ```bash
> docker compose down -v
> ```

---

## 🔑 Credenciales de Prueba

| Rol | Correo Electrónico | Contraseña |
|---|---|---|
| **Administrador** | admin@cineapp.com | admin123 |

---

## 🧪 Flujo Completo de Prueba y Verificación E2E

Para verificar la comunicación entre los tres componentes (**Frontend ↔ Backend ↔ Base de Datos**) y correr la suite de pruebas automatizadas, consulta la guía detallada en: **[FLUJO_DE_PRUEBA.md](./FLUJO_DE_PRUEBA.md)**

Para ejecutar la suite de pruebas automatizadas:
```bash
python backend/tests/test_flujo_completo.py
```

---

## 📂 Estructura del Monorepo

```text
cineapp-docker/
├── docker-compose.yml          # Orquestación de servicios (db, backend, frontend)
├── FLUJO_DE_PRUEBA.md          # Documentación del flujo de prueba E2E
├── README.md                   # Documentación principal del proyecto
├── init/                       # Scripts de inicialización de Base de Datos
│   ├── 01_schema.sql           # Esquema de tablas y relaciones
│   └── 02_seed.sql             # Datos iniciales (usuarios, catálogo, regiones)
├── backend/                    # Proyecto Backend (Flask API)
│   ├── Dockerfile              # Empaquetado Docker de Backend
│   ├── .dockerignore           # Exclusiones de build Docker
│   ├── app.py                  # Punto de entrada y configuración de Swagger
│   ├── requirements.txt        # Dependencias Python
│   ├── routes/                 # Endpoints REST documentados con OpenAPI
│   ├── services/               # Lógica de negocio y consultas MySQL
│   └── tests/                  # Suite de pruebas automatizadas
└── frontend/                   # Proyecto Frontend (Web SPA)
    ├── Dockerfile              # Empaquetado Docker de Frontend (Nginx)
    ├── .dockerignore           # Exclusiones de build Docker
    ├── nginx.conf              # Configuración de Nginx
    ├── pages/                  # Vistas HTML (login, catálogo, reproductor)
    ├── js/                     # Lógica JavaScript y consumo de API
    └── css/                    # Estilos visuales
```

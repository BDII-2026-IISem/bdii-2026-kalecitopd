# 🦷 OdontoNova Backend API

Backend modular desarrollado en **Django 6.1.2** y **Django REST Framework (DRF)** para el sistema **OdontoNova**, siguiendo los lineamientos de la currícula de Tecnogua. El sistema implementa un robusto módulo de seguridad basado en autenticación **JWT** y un control de acceso basado en roles con matriz de permisos (**RBAC**).

---

## 🚀 Características Principales

* **Autenticación JWT**: Integración con `djangorestframework-simplejwt` con soporte para rotación de tokens y blacklist.
* **Control de Acceso Basado en Roles (RBAC)**: Matriz de permisos dinámica (`ResourceRole` y `RoleUser`) validada mediante la clase personalizada `HasResourcePermission`.
* **Estructura Modular**: Organizado en aplicaciones independientes (`security`, `client`, `dental`).
* **Comando de Siembra (`seed_security`)**: Automatización para poblar roles, recursos y matrices iniciales en la base de datos.
* **Documentación Interactiva**: API documentada con **drf-spectacular** (Swagger UI & Redoc) con soporte integrado para `Bearer Token`.

---

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio y entrar al proyecto**:
   ```bash
   git clone <url-del-repositorio>
   cd DJANGO
Crear y activar el entorno virtual:

Bash
python -m venv venv
# En Windows (PowerShell):
.\venv\Scripts\Activate
# En Linux/macOS:
source venv/bin/activate
Instalar las dependencias:

Bash
pip install -r requirements.txt
Aplicar las migraciones a la base de datos:

Bash
python manage.py makemigrations
python manage.py migrate
Ejecutar el comando de siembra (Seeder):
Poblar los roles iniciales (Administrador, Odontólogo, Recepcionista) y los recursos del sistema:

Bash
python manage.py seed_security
Ejecutar el servidor de desarrollo:

Bash
python manage.py runserver
📚 Endpoints Principales y Documentación
Swagger UI (Documentación Interactiva): http://127.0.0.1:8000/api/docs/

ReDoc: http://127.0.0.1:8000/api/redoc/

Autenticación JWT:

Obtener Token: POST /api/token/

Refrescar Token: POST /api/token/refresh/

## Contrato de autenticación del frontend

El frontend OdontoNova usa las rutas compatibles con la guía Angular 2026:

* `POST /api/auth/login/` entrega los tokens JWT y el perfil del usuario.
* `POST /api/auth/refresh/` rota el refresh token y entrega el nuevo par.
* `POST /api/auth/logout/` revoca el refresh token presentado.
* `GET` y `PATCH /api/auth/profile/` consultan el perfil y actualizan el correo.
* `GET /api/auth/permissions/` devuelve las concesiones efectivas del usuario.
* `GET/POST/PATCH/DELETE /api/users/` administra cuentas; la contraseña nunca
  se devuelve y se almacena con el hash de Django.

La matriz de permisos sigue el RBAC existente de OdontoNova, que concede acceso
por recurso (no por método HTTP). Por eso cada concesión de la matriz usa
`method: "*"`, y la API continúa validando la autorización en cada petición.
Los permisos iniciales de usuarios se crean o sincronizan con
`python manage.py seed_security`.

El frontend mantiene los nombres de campos `snake_case` que exponen los
serializers DRF de este proyecto.

🛡️ Módulo de Seguridad y RBAC
El sistema protege los ViewSets de negocio evaluando el atributo resource_name mediante el mixin HasResourcePermission. Los códigos de respuesta HTTP implementados cumplen con los estándares de seguridad:

401 Unauthorized: Petición rechazada por ausencia o invalidez del Token JWT.

403 Forbidden: Petición rechazada porque el rol del usuario autenticado no posee permisos sobre el recurso solicitado en la matriz.

## Módulos de OdontoNova

El panel de administración y la API incluyen pacientes, odontólogos, sillones,
citas, historias clínicas y evoluciones, planes y detalles de tratamiento,
procedimientos, sesiones clínicas y pagos. Las rutas principales de negocio son
`/api/pacientes/`, `/api/citas/`, `/api/historias/`, `/api/tratamientos/`,
`/api/sesiones/` y `/api/pagos/`. Las evoluciones se registran con
`POST /api/historias/{id}/evoluciones/`.

Las citas validan la disponibilidad del odontólogo y del sillón. Los detalles
del plan permiten aprobación parcial; las sesiones solo registran cantidades
aprobadas y actualizan el total ejecutado. Los pagos confirmados actualizan el
saldo pendiente del plan. El comando `python manage.py seed_security` prepara
roles y permisos para los recursos odontológicos.

Los antiguos módulos de productos y ventas quedan fuera de las aplicaciones y
rutas activas. Sus archivos y tablas existentes no se eliminan para conservar
los datos previos.

👨‍💻 Autor
Desarrollado como parte del programa de backend avanzado con Django.
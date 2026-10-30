# StoreLab Django · Backend (Django + DRF)

Backend del laboratorio **StoreLab**: Django 5 + Django REST Framework + SimpleJWT + RBAC propio. Expone la API que consume el frontend Angular 22.

## ISS realizados

### Fase I · Business

| ISS | Qué se hizo |
|-----|-------------|
| 00 | Entorno y proyecto Django |
| 01 | Settings y selección del motor de base de datos |
| 02 | Apps `client`, `product` y `sale` |
| 03 | Custom User antes de la primera migración |
| 04 | Modelo `Client` |
| 05 | Modelos `ProductType` y `Product` |
| 06 | Modelos `Sale` y `ProductSale` |
| 07 | Serializers y JSON camelCase |
| 08 | Client con `ModelViewSet` |
| 09 | Catálogo con `ModelViewSet` |
| 10 | Disponibles con `ListAPIView` |
| 11 | Registro de venta con `APIView` |
| 12 | Consulta y anulación de ventas |
| 13 | Django Admin |
| 14 | OpenAPI (cierre Fase I) |

### Fase II · Auth con RBAC

| ISS | Qué se hizo |
|-----|-------------|
| 15 | `RefreshToken` |
| 16 | `Role`, `RoleUser`, `Resource` y `ResourceRole` |
| 17 | Login OPEN |
| 18 | Refresh con rotación |
| 19 | Logout |
| 20 | Perfil JWT con token |
| 21 | `HasResourceAccess` |
| 22 | RBAC sobre el negocio |
| 23 | CRUD de la matriz |
| 24 | Semilla RBAC y Swagger con Bearer |
| 25 | Pruebas 401 y 403 (cierre Fase II) |

## Pasos para el backend

1. **Entrar al proyecto y crear el `.env`**:
   ```bash
   cd pry-django
   printf 'DJANGO_SECRET_KEY=dev-storelab\nDJANGO_DEBUG=True\nDJANGO_ALLOWED_HOSTS=localhost,127.0.0.1\n' > .env
   ```

2. **Crear el entorno virtual e instalar dependencias**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Migrar la base de datos y crear el superusuario**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Sembrar el RBAC** (rol `admin`, recursos y asignación al usuario):
   ```bash
   python manage.py seed_rbac --username <tu_usuario>
   ```

5. **Levantar el servidor**:
   ```bash
   python manage.py runserver 8000
   ```

- API: `http://localhost:8000/api/`
- Swagger: `http://localhost:8000/api/schema/swagger-ui/`

> `API_ACCESS=open` publica el negocio sin JWT (Fase I). `API_ACCESS=rbac` exige JWT y permisos por `(método, ruta)` (Fase II).

## Endpoints principales

| Grupo | Endpoint |
|-------|----------|
| Negocio | `/api/clients/`, `/api/product-types/`, `/api/products/`, `/api/products/available/`, `/api/sales/` |
| Auth | `/api/auth/login/`, `/api/auth/refresh/`, `/api/auth/logout/`, `/api/auth/profile/`, `/api/auth/permissions/` |
| Administración | `/api/users/`, `/api/roles/`, `/api/resources/`, `/api/role-users/`, `/api/resource-roles/` |

## Autor

**Estudiante:** Kaleth Perez · **Asignatura:** Base de Datos II · **Docente:** Jaider Quintero

# StoreLab Django · Frontend Angular 22

Frontend del laboratorio **StoreLab Django**: Angular 22 (standalone + Signals), PrimeNG 22 y Tailwind CSS 4. Consume la API del backend `pry-django` (Django 5 + DRF + JWT + RBAC).

## ISS realizados

| ISS | Qué se hizo |
|-----|-------------|
| 00 | Requisitos previos (Node, Angular CLI, backend listo) |
| 01 | Bootstrap del proyecto Angular 22 con CLI |
| 01A | Esqueleto Header / Aside / contenido / Footer |
| 01B | Menú PrimeNG y primera interacción |
| 02 | Núcleo: environment, modelos, servicios y layout |
| 03 | CRUD de clientes |
| 04 | CRUD de tipos de producto |
| 05 | CRUD de productos |
| 06 | Ventas y detalle |
| 07 | Dashboard |
| 08 | Autenticación JWT y refresh |
| 09 | Guards y RBAC en la UI |
| 10 | Administración RBAC (usuarios, roles, recursos) |
| 11 | Build, calidad y resolución de problemas |

## Pasos para el frontend

1. **Levantar el backend** (`pry-django`) en `http://localhost:8000`:
   ```bash
   python manage.py migrate
   python manage.py seed_rbac --username <usuario>
   python manage.py runserver 8000
   ```
   > `API_ACCESS=open` para la Fase I (sin login) y `API_ACCESS=rbac` para la Fase II (JWT + permisos).

2. **Instalar dependencias** del frontend:
   ```bash
   cd front-storelab-django
   npm install
   ```

3. **Configurar el entorno** en `src/environments/environment.ts`:
   ```ts
   apiUrl: 'http://localhost:8000/api',   // sin "/" al final
   ```

4. **Correr el proyecto**:
   ```bash
   npm start      # http://localhost:4200
   ```

5. **Build de producción**:
   ```bash
   npm run build
   ```

## Autor

**Estudiante:** Kaleth Perez · **Asignatura:** Base de Datos II · **Docente:** Jaider Quinterodale n

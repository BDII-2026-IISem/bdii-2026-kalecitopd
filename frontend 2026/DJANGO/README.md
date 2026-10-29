# OdontoNova - Frontend

Aplicación web de OdontoNova desarrollada con Angular 22, componentes standalone, Signals, zoneless, PrimeNG 22/Aura y Tailwind CSS 4. Sigue las capas de la guía académica y adapta sus ejemplos a las entidades y los permisos reales del backend en `../../DJANGO`.

## Requisitos

- Node.js 22
- npm 10 o superior
- Backend Django disponible en `http://127.0.0.1:8000`

## Ejecutar en Ubuntu/WSL

Abre dos terminales de Ubuntu. En la primera, inicia el backend:

```bash
cd "$HOME/ia-lab/projecs/base de datos 2/BDD/DJANGO"
source venv/bin/activate
# Solo la primera vez, si aún no tienes un usuario administrador:
python manage.py createsuperuser
python manage.py runserver
```

En la segunda, inicia Angular:

```bash
cd "$HOME/ia-lab/projecs/base de datos 2/BDD/frontend 2026/DJANGO"
npm install
npm start
```

Abre `http://localhost:4200`. El proxy de desarrollo reenvía las solicitudes `/api` al servidor Django. Para entrar, usa las credenciales de un usuario de Django.

Si el backend muestra `That port is already in use`, Django ya está ejecutándose; no abras un segundo servidor. Deja esa terminal activa.

## Módulos y comportamiento

- Resumen de pacientes y citas, según los permisos del usuario.
- CRUD de pacientes, odontólogos, sillones, citas, historias clínicas, planes,
  procedimientos, detalles, sesiones clínicas y pagos.
- Registro de evoluciones desde cada historia clínica.
- Administración de usuarios, roles, asignaciones y permisos.
- Perfil del usuario y actualización de correo.
- Búsqueda local, confirmación antes de eliminar y manejo visible de errores
  401/403/validación del backend.
- Menú y rutas protegidos por los permisos efectivos del RBAC de OdontoNova.
- Renovación de JWT en un solo vuelo al recibir 401; logout revoca el refresh.

El contrato local usa `snake_case`, listas sin envoltorio y rutas DRF con slash
final. La guía muestra un backend StoreLab distinto; sus ejemplos de clientes,
productos y ventas no reemplazan los módulos odontológicos de este proyecto.

La interfaz no puede recuperar ni corregir credenciales. Si el navegador dice
“Usuario o contraseña incorrectos”, crea un usuario con
`python manage.py createsuperuser` o cambia su clave con
`python manage.py changepassword <usuario>` en la carpeta del backend.

## Validar

```bash
npm test -- --watch=false
npm run build
```

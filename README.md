# Proyecto BDD - Bases de Datos II

Este repositorio reúne dos líneas de trabajo relacionadas entre sí:

- un laboratorio de bases de datos con Docker Compose y varios motores de BD
- un proyecto web con Django y Angular siguiendo la guía académica, adaptada a la lógica real del backend y el frontend

La intención es documentar tanto la parte práctica de administración de bases de datos como la parte de desarrollo de una API y una interfaz que consumen ese backend.

## Objetivo general

Preparar un entorno de trabajo para aprender y validar:

- instalación y configuración de distintos motores de bases de datos
- gestión de usuarios, permisos y conexiones remotas
- desarrollo de una API REST con Django y DRF
- autenticación JWT y control de acceso por roles
- consumo de la API desde una interfaz Angular

## Estructura principal

```text
BDD/
├── README.md
├── DJANGO/
├── frontend 2026/
├── OdontoNova/
├── evidencias/
├── base.md
├── ...
```

## Contenido del repositorio

### 1. Laboratorio de motores de bases de datos

Se trabajó con los siguientes motores:

- MySQL 8.0
- PostgreSQL 17
- Microsoft SQL Server 2022
- Oracle Database XE 21c

Cada uno quedó configurado con Docker Compose, usando una red compartida y almacenamiento persistente para validar conexiones, creación de bases, usuarios y pruebas funcionales.

### 2. Backend Django

La carpeta `DJANGO` contiene la API principal del proyecto, con:

- Django
- Django REST Framework
- JWT
- control de permisos por recursos y roles
- estructura modular por aplicaciones

### 3. Frontend Angular

La carpeta `frontend 2026/DJANGO` contiene la aplicación web que consume la API, con Angular 22, PrimeNG y Tailwind, siguiendo la guía y adaptando el consumo a los módulos reales del proyecto.

### 4. Evidencias y modelos

En `OdontoNova/` y `evidencias/` se encuentran scripts, capturas y documentación de las pruebas realizadas, incluyendo migración, creación de tablas y validación del esquema.

## Tecnologías principales

| Tecnología | Uso |
|---|---|
| WSL2 + Ubuntu | entorno de desarrollo |
| Docker Engine | contenedores |
| Docker Compose | orquestación |
| MySQL | motor de base de datos |
| PostgreSQL | motor de base de datos |
| SQL Server | motor de base de datos |
| Oracle XE | motor de base de datos |
| Django | backend |
| DRF | API REST |
| JWT | autenticación |
| Angular 22 | frontend |

## Requisitos

- Windows con WSL2
- Docker y Docker Compose instalados
- Python 3.x
- Node.js 22+
- npm 10+

## Inicio rápido

### Backend Django

```bash
cd "$HOME/ia-lab/projecs/base de datos 2/BDD/DJANGO"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Angular

```bash
cd "$HOME/ia-lab/projecs/base de datos 2/BDD/frontend 2026/DJANGO"
npm install
npm start
```

La API del backend queda normalmente en `http://127.0.0.1:8000` y la app frontend en `http://localhost:4200`.

## Nota

Este repositorio combina trabajo académico y desarrollo práctico. La parte de motores de bases de datos sirve para comprender el funcionamiento real de varios SGBD; la parte de Django y Angular representa la aplicación concreta que consume y valida la guía de trabajo del curso.

## Estado

El proyecto está en proceso de integración y documentación, con ejercicios, pruebas, modelos y evidencia en varias carpetas del repositorio. La organización actual permite trabajar tanto la parte de infraestructura de bases de datos como la parte de aplicación web según la guía de estudio.


Los servicios esperados son:

```text
mysql-server
postgres-server
mssql-server
oracle-server
```

Los motores MySQL, PostgreSQL y SQL Server permitieron realizar operaciones sobre la base de prueba `bd_clase1`.

Oracle quedó funcionando correctamente después de solucionar el problema relacionado con el directorio de datos.

---

# Evidencias

Las evidencias de la práctica se encuentran dentro de la carpeta:

```text
Evidencias/
```

Las imágenes fueron organizadas y numeradas de acuerdo con el orden en que se realizó la actividad.

Algunas de las evidencias muestran:

- Preparación de Ubuntu y WSL2.
- Instalación de Docker.
- Verificación de Docker y Docker Compose.
- Creación de carpetas y red Docker.
- Configuración y ejecución de MySQL.
- Configuración de PostgreSQL.
- Configuración de UFW.
- Instalación y administración de SQL Server.
- Obtención de la IP de WSL.
- Configuración de Oracle.
- Error inicial del volumen de Oracle.
- Corrección de permisos.
- Conexión a Oracle.
- Creación y conexión del usuario `almacendb_admin`.

---

# Problemas encontrados y soluciones

Durante el laboratorio se presentaron algunos inconvenientes.

### MySQL

Se presentó un error durante un intento de autenticación.

**Solución:**  
Se revisó el archivo `.env` y se utilizó la contraseña configurada correctamente.

### Oracle

Durante el primer arranque se presentaron problemas con el directorio utilizado para almacenar los datos.

**Solución:**

1. Detener el contenedor.
2. Crear el directorio de Oracle.
3. Ajustar los permisos.
4. Iniciar nuevamente el servicio.
5. Verificar que el contenedor quedara en estado `healthy`.

Este procedimiento permitió que Oracle iniciara correctamente.

---

# Seguridad

Las contraseñas utilizadas durante el laboratorio son únicamente para fines académicos y no deben utilizarse en un entorno real.

Si este repositorio se comparte públicamente, se recomienda no publicar:

- Contraseñas.
- Usuarios administrativos.
- Direcciones IP sensibles.
- Información privada.
- Archivos `.env` con credenciales reales.

Para un entorno de producción se deberían utilizar secretos, usuarios con los permisos mínimos necesarios y reglas de firewall limitadas a la red requerida.

---

# Fuentes consultadas

La práctica se realizó tomando como referencia las guías proporcionadas para el laboratorio:

- Introducción y despliegue de motores mediante Docker Compose.
- Instalación y configuración de MySQL.
- Instalación y configuración de PostgreSQL.
- Instalación y configuración de Microsoft SQL Server.
- Instalación y configuración de Oracle XE.

---

# Información del trabajo

**Estudiante:** Kaleth Perez  
**Asignatura:** Base de Datos  
**Docente:** Jaider Quintero  
**Fecha:** 25 de agosto de 2026

---

# Uso de Inteligencia Artificial

Durante el desarrollo del laboratorio se utilizó **ChatGPT** como herramienta de apoyo.

La inteligencia artificial se utilizó principalmente para:

- Comprender algunos comandos.
- Identificar errores durante la configuración.
- Buscar posibles soluciones.
- Aclarar dudas sobre Docker y bases de datos.
- Comprender mejor algunos de los procedimientos realizados.

La herramienta fue utilizada como apoyo para el aprendizaje y desarrollo de la actividad, y no como reemplazo del trabajo realizado.

---

## Conclusión

La práctica permitió comprobar el funcionamiento de diferentes motores de bases de datos utilizando Docker Compose.

El uso de contenedores permitió mantener cada motor separado y facilitar su configuración. También se comprobó la importancia de utilizar almacenamiento persistente, configurar correctamente los puertos y verificar el estado de cada servicio antes de realizar las conexiones.

Finalmente, los problemas encontrados durante la autenticación de MySQL y la configuración del volumen de Oracle sirvieron para comprender mejor la importancia de revisar las variables de entorno, permisos y configuraciones de los servicios.

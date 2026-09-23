# Laboratorio de Motores de Bases de Datos con Docker Compose

## 📌 Descripción

Este proyecto corresponde a un laboratorio de bases de datos realizado utilizando **WSL2 sobre Ubuntu** y **Docker Compose**.

El objetivo principal fue preparar un entorno de trabajo donde se pudieran ejecutar diferentes motores de bases de datos de manera independiente mediante contenedores Docker.

Durante la práctica se trabajó con los siguientes motores:

- **MySQL 8.0**
- **PostgreSQL 17**
- **Microsoft SQL Server 2022**
- **Oracle Database XE 21c**

También se configuró una red Docker compartida, almacenamiento persistente y diferentes herramientas para comprobar el funcionamiento de cada motor.

---

## 🎯 Objetivos

- Preparar el entorno de trabajo con WSL2, Docker Engine y Docker Compose.
- Crear la estructura de carpetas utilizada para el laboratorio.
- Crear una red Docker compartida para los diferentes servicios.
- Desplegar los cuatro motores de bases de datos mediante contenedores.
- Verificar el funcionamiento de cada servicio.
- Crear bases de datos y usuarios de prueba.
- Configurar los puertos necesarios para las conexiones.
- Instalar las herramientas necesarias para administrar SQL Server.
- Identificar y solucionar los errores encontrados durante la instalación.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Versión / configuración |
|---|---|
| Windows | Sistema principal |
| Ubuntu | Ejecutado mediante WSL2 |
| Docker Engine | 29.7.2 |
| Docker Compose | 5.5.0 |
| MySQL | 8.0 |
| PostgreSQL | 17 |
| Microsoft SQL Server | 2022 |
| Oracle Database | XE 21c |

---

## 📁 Estructura del proyecto

La estructura principal utilizada durante el laboratorio fue:

```text
~/ia-lab/
├── services/
│   └── motores-bd/
│       ├── mysql/
│       ├── postgres/
│       ├── mssql/
│       └── oracle/
│
└── data/
    ├── mysql/
    ├── postgres/
    ├── mssql/
    └── oracle/
```

La carpeta `services/motores-bd/` contiene la configuración de los diferentes servicios, mientras que `data/` se utiliza para conservar los datos de los motores de forma persistente.

---

## 🌐 Red y puertos

Para permitir la comunicación entre los servicios se creó la red Docker:

```text
ia-lab-network
```

Los puertos utilizados fueron:

| Motor | Contenedor | Puerto |
|---|---|---:|
| MySQL | `mysql-server` | `3306` |
| PostgreSQL | `postgres-server` | `5432` |
| SQL Server | `mssql-server` | `1433` |
| Oracle XE | `oracle-server` | `1521` |

La base de trabajo utilizada fue:

```text
tecnogua
```

También se utilizó la base de prueba:

```text
bd_clase1
```

---

# 🐳 Preparación del entorno

Primero se preparó Ubuntu mediante **WSL2** y se instalaron Docker Engine y Docker Compose.

Para comprobar la instalación se utilizaron comandos como:

```bash
docker --version
docker compose version
docker run hello-world
```

El comando `hello-world` permitió comprobar que Docker podía descargar una imagen y ejecutar correctamente un contenedor.

Después se crearon las carpetas necesarias y la red compartida:

```bash
mkdir -p ~/ia-lab/services/motores-bd
mkdir -p ~/ia-lab/data
```

La red utilizada por los servicios fue:

```bash
docker network create ia-lab-network
```

---

# 🗄️ MySQL 8.0

MySQL se configuró utilizando el contenedor:

```text
mysql-server
```

y el puerto:

```text
3306
```

La base inicial utilizada fue:

```text
tecnogua
```

Después de iniciar el contenedor se verificó su estado y se realizó una conexión utilizando el cliente de MySQL.

Una de las consultas utilizadas fue:

```sql
SHOW DATABASES;
```

Con esto se comprobó que la base `tecnogua` estaba disponible.

También se dejó preparado el procedimiento para crear un usuario remoto y realizar respaldos mediante `mysqldump`.

### ⚠️ Problema encontrado

Durante una prueba de autenticación se presentó un rechazo de acceso. El problema se solucionó utilizando la contraseña configurada en el archivo `.env`.

Esto permitió comprobar la importancia de revisar correctamente las variables de configuración antes de intentar conectarse al motor.

---

# 🐘 PostgreSQL 17

PostgreSQL se configuró mediante el contenedor:

```text
postgres-server
```

utilizando el puerto:

```text
5432
```

La base inicial fue:

```text
tecnogua
```

Después de iniciar el servicio se utilizó `psql` para comprobar las bases disponibles.

También se creó una base de prueba:

```sql
CREATE DATABASE bd_clase1;
```

Posteriormente se creó el usuario:

```text
admin
```

También se configuró el acceso para que PostgreSQL pudiera escuchar en todas las interfaces.

### 🔥 Configuración del firewall

Se instaló y configuró UFW para permitir el puerto utilizado por PostgreSQL:

```text
5432
```

---

# 🟦 Microsoft SQL Server 2022

SQL Server se ejecutó mediante el contenedor:

```text
mssql-server
```

utilizando el puerto:

```text
1433
```

Una vez iniciado el servicio se utilizaron las herramientas de Microsoft para administrar la base de datos.

Se instaló:

```text
mssql-tools18
unixodbc-dev
```

y se agregó la ruta correspondiente al `PATH` para poder utilizar `sqlcmd`.

Para comprobar la instalación se verificó la ubicación de `sqlcmd`.

Con SQL Server se realizaron pruebas como:

- Listar las bases de datos.
- Crear `bd_clase1`.
- Verificar el contexto de la base.
- Crear el login `admin`.
- Comprobar la conectividad del servicio.

---

# 🟠 Oracle Database XE 21c

Oracle XE se configuró utilizando el contenedor:

```text
oracle-server
```

con el puerto:

```text
1521
```

El servicio utilizado para la conexión fue:

```text
TECNOGUA
```

### ⚠️ Problema encontrado

Durante el primer arranque de Oracle se presentaron errores relacionados con el directorio utilizado para almacenar los datos.

El contenedor tuvo que detenerse y posteriormente se creó el directorio:

```bash
mkdir -p ~/ia-lab/data/oracle
```

Después se ajustaron los permisos necesarios y se volvió a iniciar el contenedor.

En el segundo arranque Oracle quedó en estado:

```text
healthy
```

y los registros indicaron:

```text
DATABASE IS READY TO USE
```

Después se realizó una conexión mediante `SQL*Plus`.

Se consultaron los usuarios existentes y se creó el usuario/esquema:

```text
almacendb_admin
```

con los privilegios:

```text
CONNECT
RESOURCE
```

Finalmente se comprobó la conexión utilizando el servicio `TECNOGUA`.

---

# 🔎 Verificación de los servicios

Una de las comprobaciones principales fue revisar el estado de los contenedores para confirmar que los motores estuvieran funcionando correctamente.

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

# 📸 Evidencias

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

# ⚠️ Problemas encontrados y soluciones

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

# 🔐 Seguridad

Las contraseñas utilizadas durante el laboratorio son únicamente para fines académicos y no deben utilizarse en un entorno real.

Si este repositorio se comparte públicamente, se recomienda no publicar:

- Contraseñas.
- Usuarios administrativos.
- Direcciones IP sensibles.
- Información privada.
- Archivos `.env` con credenciales reales.

Para un entorno de producción se deberían utilizar secretos, usuarios con los permisos mínimos necesarios y reglas de firewall limitadas a la red requerida.

---

# 📚 Fuentes consultadas

La práctica se realizó tomando como referencia las guías proporcionadas para el laboratorio:

- Introducción y despliegue de motores mediante Docker Compose.
- Instalación y configuración de MySQL.
- Instalación y configuración de PostgreSQL.
- Instalación y configuración de Microsoft SQL Server.
- Instalación y configuración de Oracle XE.

---

# 👨‍💻 Información del trabajo

**Estudiante:** Kaleth Perez  
**Asignatura:** Base de Datos  
**Docente:** Jaider Quintero  
**Fecha:** 25 de agosto de 2026

---

# 🤖 Uso de Inteligencia Artificial

Durante el desarrollo del laboratorio se utilizó **ChatGPT** como herramienta de apoyo.

La inteligencia artificial se utilizó principalmente para:

- Comprender algunos comandos.
- Identificar errores durante la configuración.
- Buscar posibles soluciones.
- Aclarar dudas sobre Docker y bases de datos.
- Comprender mejor algunos de los procedimientos realizados.

La herramienta fue utilizada como apoyo para el aprendizaje y desarrollo de la actividad, y no como reemplazo del trabajo realizado.

---

## ✅ Conclusión

La práctica permitió comprobar el funcionamiento de diferentes motores de bases de datos utilizando Docker Compose.

El uso de contenedores permitió mantener cada motor separado y facilitar su configuración. También se comprobó la importancia de utilizar almacenamiento persistente, configurar correctamente los puertos y verificar el estado de cada servicio antes de realizar las conexiones.

Finalmente, los problemas encontrados durante la autenticación de MySQL y la configuración del volumen de Oracle sirvieron para comprender mejor la importancia de revisar las variables de entorno, permisos y configuraciones de los servicios.

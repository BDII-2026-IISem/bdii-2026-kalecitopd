 # Informe de laboratorio: motores de bases de datos con Docker Compose

 **Estudiante:** Kaleth Perez  
 **Asignatura:** Base de datos   
 **Docente:** Jaider Quintero  
 **Fecha:** 25 de agosto de 2026  

 ## 1. Introducción

 En este laboratorio se preparó un entorno de trabajo en WSL2 sobre Ubuntu y se instalaron cuatro motores de bases de datos mediante Docker Compose: MySQL 8.0, PostgreSQL 17, Microsoft SQL Server 2022 y Oracle Database XE 21c. El propósito fue comprobar el funcionamiento de los servicios, crear bases de datos y usuarios, habilitar el acceso por red y dejar documentados los pasos realizados.

 La actividad se desarrolló tomando como referencia la [guía de introducción](https://www.tecnogua.com/academic/site/bd/introduccion/) y las guías específicas de [MySQL](https://www.tecnogua.com/academic/site/bd/instalacion/mysql/), [PostgreSQL](https://www.tecnogua.com/academic/site/bd/instalacion/postgresql/), [Microsoft SQL Server](https://www.tecnogua.com/academic/site/bd/instalacion/mssql/) y [Oracle](https://www.tecnogua.com/academic/site/bd/instalacion/oracle/).

 ## 2. Objetivos

 - Preparar WSL2, Docker Engine y Docker Compose.
 - Crear la estructura de carpetas y la red Docker compartida.
 - Desplegar los cuatro motores como contenedores independientes.
 - Verificar servicios, puertos, bases de datos y usuarios.
 - Instalar las herramientas necesarias para administrar SQL Server.
 - Documentar las incidencias encontradas y su solución.

 ## 3. Entorno y configuración

 | Elemento | Configuración observada |
 | --- | --- |
 | Sistema | Windows con Ubuntu en WSL2 |
 | Orquestación | Docker Engine 29.7.2 y Docker Compose v5.5.0 |
 | Red Docker | `ia-lab-network` |
 | MySQL | 8.0, contenedor `mysql-server`, puerto `3306` |
 | PostgreSQL | 17, contenedor `postgres-server`, puerto `5432` |
 | SQL Server | 2022, contenedor `mssql-server`, puerto `1433` |
 | Oracle | XE 21c, contenedor `oracle-server`, puerto `1521` |
 | Base de trabajo | `tecnogua` |
 | Base de prueba | `bd_clase1` |

 La estructura utilizada en WSL fue `~/ia-lab/services/motores-bd/`, con una carpeta para cada motor, y `~/ia-lab/data/`, destinada a conservar los datos de forma persistente.

 ## 4. Desarrollo de la actividad

 ### 4.1 Preparación del entorno

 Se verificó la disponibilidad de Ubuntu desde Microsoft Store. Luego se instalaron Docker Engine, Docker Compose y sus dependencias. La ejecución de `docker --version`, `docker compose version` y `docker run hello-world` confirmó que el motor podía descargar imágenes y ejecutar contenedores.

 Después se crearon las carpetas de servicios y datos, se creó la red externa `ia-lab-network` y se incorporó el usuario de WSL al grupo `docker`.

 ### 4.2 MySQL

 Se configuró el servicio MySQL 8.0 con el puerto `3306`, almacenamiento persistente y la base inicial `tecnogua`. El contenedor `mysql-server` quedó en estado **healthy**. La conexión local mediante el cliente MySQL permitió ejecutar `SHOW DATABASES;` y confirmar la existencia de `tecnogua`.

 También se dejó preparado el procedimiento para crear un usuario remoto y realizar un respaldo con `mysqldump`. La evidencia muestra un primer intento de autenticación rechazado y un segundo intento exitoso; esto se resolvió utilizando la contraseña configurada en el archivo `.env`.

 ### 4.3 PostgreSQL

 Se configuró PostgreSQL 17 con el puerto `5432`, la base `tecnogua` y escucha en todas las interfaces. El contenedor `postgres-server` inició correctamente y reportó estado **healthy**. Desde `psql` se listaron las bases, se creó `bd_clase1`, se cambió a ella y se creó el usuario `admin`.

 Además, se instaló y activó UFW para permitir el puerto `5432`, dejando documentada la regla de acceso correspondiente.

 ### 4.4 Microsoft SQL Server

 Se desplegó SQL Server 2022 con el contenedor `mssql-server` y el puerto `1433`. El servicio inició correctamente y los registros mostraron la finalización de la recuperación de las bases internas. Con `sqlcmd` se listaron las bases, se creó `bd_clase1`, se verificó su contexto y se creó el login `admin`.

 Para administrar el motor desde WSL se instaló `mssql-tools18` junto con `unixodbc-dev`, se agregó `/opt/mssql-tools18/bin` al `PATH` y se verificó la ubicación de `sqlcmd`.

 ### 4.5 Oracle XE

 Se configuró Oracle XE 21c con el puerto `1521`, el servicio `TECNOGUA` y almacenamiento persistente. Durante el primer arranque se observaron errores porque el directorio de datos no estaba preparado. El contenedor se detuvo, se creó `~/ia-lab/data/oracle`, se ajustaron sus permisos y se inició nuevamente. En el segundo arranque Oracle quedó en estado **healthy** y sus registros indicaron `DATABASE IS READY TO USE`.

 Una vez disponible el servicio, se estableció una conexión mediante SQL*Plus, se consultaron los usuarios y se creó el usuario/esquema `almacendb_admin` con privilegios `CONNECT` y `RESOURCE`. La conexión se validó usando el servicio `TECNOGUA`.

 ## 5. Resultados

 - Docker y Docker Compose quedaron instalados y funcionales.
 - Se creó la red compartida `ia-lab-network`.
 - MySQL, PostgreSQL, SQL Server y Oracle quedaron desplegados con sus puertos publicados.
 - MySQL, PostgreSQL y SQL Server permitieron crear y consultar `bd_clase1`.
 - SQL Server quedó preparado para administración con `sqlcmd`.
 - Oracle quedó operativo después de corregir el directorio del volumen persistente.
 - Se habilitaron reglas UFW para los puertos `5432`, `1433` y `1521`; la evidencia no muestra la regla `3306`.

 ## 6. Conclusiones

 La práctica permitió comprobar que Docker Compose simplifica el despliegue reproducible de distintos motores de bases de datos. La separación entre servicios y datos persistentes facilita administrar cada motor de forma independiente, mientras que la red compartida y los puertos publicados permiten preparar conexiones desde herramientas como DBeaver.

 Las incidencias de autenticación de MySQL y del volumen de Oracle demostraron la importancia de verificar las variables del `.env`, los permisos de los directorios y el estado de salud de cada contenedor antes de intentar una conexión.

 ## 7. Recomendaciones de seguridad

 Las contraseñas visibles en las capturas corresponden al laboratorio y no deben reutilizarse en producción. Antes de compartir el informe públicamente se recomienda reemplazar o difuminar cualquier contraseña, IP, usuario administrativo o dato sensible que aparezca en una captura. Para un entorno real deben usarse secretos, usuarios con privilegios mínimos y reglas de firewall limitadas a la red necesaria.

 ## 8. Relación y justificación de evidencias

 Las imágenes se encuentran en la carpeta [Evidencias](Evidencias/). Se conservaron en el orden cronológico de la práctica y se renombraron para que puedan citarse fácilmente.

 | Evidencia | Qué muestra | Justificación |
 | --- | --- | --- |
 | [evidencia_01.png](Evidencias/evidencia_01.png) | Búsqueda de Ubuntu en Microsoft Store | Respalda la disponibilidad del entorno Ubuntu para WSL. |
 | [evidencia_02.png](Evidencias/evidencia_02.png) | Instalación de dependencias y repositorio de Docker | Demuestra la preparación de paquetes y fuentes necesarias. |
 | [evidencia_03.png](Evidencias/evidencia_03.png) | Descarga e instalación de componentes Docker | Evidencia el proceso de instalación de Docker Engine y Compose. |
 | [evidencia_04.png](Evidencias/evidencia_04.png) | Versiones de Docker, Compose y ejecución de Hello World | Verifica que Docker funciona y puede ejecutar un contenedor. |
 | [evidencia_05.png](Evidencias/evidencia_05.png) | Creación de carpetas, red Docker y acceso al directorio MySQL | Respalda la estructura inicial del laboratorio y la red compartida. |
 | [evidencia_06.png](Evidencias/evidencia_06.png) | Inicio de MySQL y consulta `SHOW DATABASES` | Demuestra que MySQL inició y que la base `tecnogua` está disponible. |
 | [evidencia_07.png](Evidencias/evidencia_07.png) | Cambio al directorio de PostgreSQL | Evidencia el paso de preparación del siguiente motor. |
 | [evidencia_08.png](Evidencias/evidencia_08.png) | Instalación de UFW y apertura del puerto `5432` | Justifica la configuración de firewall para PostgreSQL. |
 | [evidencia_09.png](Evidencias/evidencia_09.png) | Inicio de PostgreSQL y consulta de bases | Demuestra el despliegue correcto y la conexión con `psql`. |
 | [evidencia_10.png](Evidencias/evidencia_10.png) | Creación de `bd_clase1` y usuario `admin` en PostgreSQL | Respalda la gestión básica de base de datos y usuario. |
 | [evidencia_11.png](Evidencias/evidencia_11.png) | Reglas UFW y arranque de SQL Server | Demuestra la apertura de `1433` y el inicio de `mssql-server`. |
 | [evidencia_12.png](Evidencias/evidencia_12.png) | Logs de SQL Server y preparación del repositorio Microsoft | Respalda la disponibilidad del motor y la instalación de herramientas. |
 | [evidencia_13.png](Evidencias/evidencia_13.png) | Instalación de `mssql-tools18` y `unixodbc` | Verifica la instalación de los clientes de administración de SQL Server. |
 | [evidencia_14.png](Evidencias/evidencia_14.png) | `sqlcmd`, creación de `bd_clase1`, login `admin` e IP de WSL | Demuestra la administración del motor y la consulta de la dirección de red. |
 | [evidencia_15.png](Evidencias/evidencia_15.png) | Dirección de `eth0`, prueba de puerto y creación del Compose de Oracle | Respalda la preparación de conectividad y configuración del servicio Oracle. |
 | [evidencia_16.png](Evidencias/evidencia_16.png) | UFW, variables `.env` y primer arranque de Oracle | Documenta la configuración de `1521`, PDB `tecnogua` y el intento inicial. |
 | [evidencia_17.png](Evidencias/evidencia_17.png) | Error de volumen, corrección de permisos y segundo arranque | Justifica la solución aplicada al problema del directorio persistente. |
 | [evidencia_18.png](Evidencias/evidencia_18.png) | Oracle listo y error inicial de resolución del servicio | Registra el estado de disponibilidad y la primera conexión fallida. |
 | [evidencia_19.png](Evidencias/evidencia_19.png) | Conexión correcta a `TECNOGUA` y listado de usuarios | Demuestra la conexión funcional a Oracle Database 21c XE. |
 | [evidencia_20.png](Evidencias/evidencia_20.png) | Creación y conexión del usuario `almacendb_admin` | Verifica la creación del esquema, sus privilegios y el acceso efectivo. |

 ## 9. Fuentes consultadas

 - [Introducción: crear cuatro motores con Docker Compose](https://www.tecnogua.com/academic/site/bd/introduccion/)
 - [Instalación y configuración de MySQL](https://www.tecnogua.com/academic/site/bd/instalacion/mysql/)
 - [Instalación y configuración de PostgreSQL](https://www.tecnogua.com/academic/site/bd/instalacion/postgresql/)
 - [Instalación y configuración de Microsoft SQL Server](https://www.tecnogua.com/academic/site/bd/instalacion/mssql/)
 - [Instalación y configuración de Oracle XE](https://www.tecnogua.com/academic/site/bd/instalacion/oracle/)

 ## 10. Información del trabajo y declaración de apoyo

 **Nombre:** Kaleth Perez  
 **Profesor:** Jaider Quintero

 Utilicé como apoyo la Inteligencia Artificial, ChatGPT, durante el desarrollo del trabajo, principalmente para identificar y solucionar errores, aclarar dudas y comprender mejor algunos de los procesos realizados. Esta herramienta me permitió encontrar posibles soluciones y mejorar el desarrollo del proyecto, utilizándola como un recurso de apoyo y aprendizaje.

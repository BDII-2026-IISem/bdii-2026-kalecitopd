# 🐘 Migración de OdontoNova a PostgreSQL

Documentación y evidencias del proceso de migración del esquema de base de datos **OdontoNova** a **PostgreSQL** utilizando DBeaver y Docker.

---

## 📌 1. Scripts SQL

* **`schema.sql`**: Definición de la estructura de tablas (DDL) adaptada a PostgreSQL (`SERIAL`, `BOOLEAN`, `NUMERIC`, `TIMESTAMP`).
* **`data.sql`**: Inserción de datos de prueba (DML) para verificar la integridad relacional.

---

## 📸 2. Evidencias de Creación de Tablas (DDL)

### Tabla 1: Pacientes
![Pacientes](./img/1.png)

### Tabla 2: Odontólogos
![Odontólogos](./img/2.png)

### Tabla 3: Sillones
![Sillones](./img/3.png)

### Tabla 4: Historias Clínicas
![Historias Clínicas](./img/4.png)

### Tabla 5: Citas
![Citas](./img/5.png)

### Tabla 6: Planes de Tratamiento
![Planes de Tratamiento](./img/6.png)

### Tabla 7: Procedimientos
![Procedimientos](./img/7.png)

### Tabla 8: Detalles de Tratamiento
![Detalles de Tratamiento](./img/8.png)

### Tabla 9: Sesiones Clínicas
![Sesiones Clínicas](./img/9.png)

### Tabla 10: Pagos
![Pagos](./img/10.png)

---

## 📊 3. Modelo Entidad-Relación (ERD)

Diagrama relacional completo de las 10 tablas interconectadas del proyecto en PostgreSQL:

![Diagrama ER](./img/tablas.png)

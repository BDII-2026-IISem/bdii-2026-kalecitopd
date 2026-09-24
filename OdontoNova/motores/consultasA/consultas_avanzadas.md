# CONSULTAS AVANZADAS - ODONTONOVA

## Imágenes de los registros de cada tabla creada:

* **T1: Tabla Pacientes** -> `images/t1_pacientes.png`
* **T2: Tabla Odontólogos** -> `images/t2_odontologos.png`
* **T3: Tabla Sillones** -> `images/t3_sillones.png`
* **T4: Tabla Historias Clínicas** -> `images/t4_historias_clinicas.png`
* **T5: Tabla Citas** -> `images/t5_citas.png`
* **T6: Tabla Planes de Tratamiento** -> `images/t6_planes_tratamiento.png`
* **T7: Tabla Procedimientos** -> `images/t7_procedimientos.png`
* **T8: Tabla Detalles de Tratamiento** -> `images/t8_detalles_tratamiento.png`
* **T9: Tabla Sesiones Clínicas** -> `images/t9_sesiones_clinicas.png`
* **T10: Tabla Pagos** -> `images/t10_pagos.png`

---

## 1. Consultas avanzadas en MySQL :

#### 1.1 Mostrar algunos de los registros de la tabla pacientes (T1)
```sql
SELECT nombre, tipo_documento, numero_documento, is_active 
FROM pacientes 
LIMIT 5;
1.2 Mostrar de forma ordenada (DESC) las citas desde su fecha de inicio (T5)
SQL
SELECT id, fecha_inicio, fecha_fin, motivo, estado 
FROM citas 
ORDER BY fecha_inicio DESC;
1.3 Consultas a múltiples tablas mediante WHERE (Pacientes y Citas)
SQL
SELECT c.fecha_inicio, c.motivo, c.estado, p.nombre AS paciente_nombre
FROM citas c, pacientes p
WHERE p.id = c.paciente_id;
1.4 Consultas a múltiples tablas mediante JOIN (Pacientes, Citas y Odontólogos)
SQL
SELECT P.nombre AS paciente, O.nombre AS odontologo, C.fecha_inicio, C.motivo
FROM citas AS C
JOIN pacientes AS P ON P.id = C.paciente_id
JOIN odontologos AS O ON O.id = C.odontologo_id;
1.5 Condiciones en las Consultas o filtros en las Consultas (Citas Completadas)
SQL
SELECT P.nombre, O.nombre AS odontologo, C.fecha_inicio, C.estado
FROM citas AS C
JOIN pacientes AS P ON P.id = C.paciente_id
JOIN odontologos AS O ON O.id = C.odontologo_id
WHERE C.estado = 'COMPLETADA';
1.6 Consultas con filtros condicional LIKE (Búsqueda de Pacientes)
SQL
SELECT * 
FROM pacientes AS P 
WHERE P.nombre LIKE 'M%';
1.7 Consultas con filtros condicionales BETWEEN (Rango de Fechas en Citas)
SQL
SELECT P.nombre AS paciente, C.fecha_inicio, C.motivo, O.nombre AS odontologo
FROM citas C
JOIN pacientes P ON P.id = C.paciente_id
JOIN odontologos O ON O.id = C.odontologo_id
WHERE C.fecha_inicio BETWEEN '2026-03-01 00:00:00' AND '2026-04-30 23:59:59'
ORDER BY C.fecha_inicio ASC;
1.8 Consultas con agrupamiento GROUP BY (Total recaudado por método de pago en T10)
SQL
SELECT metodo, SUM(monto) AS TotalRecaudado, COUNT(id) AS CantidadPagos
FROM pagos
WHERE estado = 'COMPLETADO'
GROUP BY metodo
ORDER BY TotalRecaudado DESC;
1.9 Subconsultas y teoría de conjuntos (Pacientes sin citas en un periodo)
SQL
SELECT * 
FROM pacientes AS P 
WHERE P.id NOT IN (
    SELECT C.paciente_id 
    FROM citas AS C 
    WHERE C.fecha_inicio BETWEEN '2026-03-01' AND '2026-03-31'
);

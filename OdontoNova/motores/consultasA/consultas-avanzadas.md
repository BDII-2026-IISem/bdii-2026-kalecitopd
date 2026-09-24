## 1. Consultas avanzadas en MySQL :

#### 1.1 Mostrar algunos de los registros de la tabla pacientes

```sql
SELECT nombre, tipo_documento, numero_documento, is_active 
FROM pacientes 
LIMIT 5;
1.2 Mostrar de forma ordenada (DESC) las citas desde su fecha de inicio
SQL
SELECT id, fecha_inicio, fecha_fin, motivo, estado 
FROM citas 
ORDER BY fecha_inicio DESC;
1.3 Consultas a múltiples tablas mediante WHERE
SQL
SELECT c.fecha_inicio, c.motivo, c.estado, p.nombre AS paciente_nombre
FROM citas c, pacientes p
WHERE p.id = c.paciente_id;
1.4 Consultas a múltiples tablas mediante JOIN
SQL
SELECT P.nombre AS paciente, O.nombre AS odontologo, C.fecha_inicio, C.motivo
FROM citas AS C
JOIN pacientes AS P ON P.id = C.paciente_id
JOIN odontologos AS O ON O.id = C.odontologo_id;
1.5 Condiciones en las Consultas o filtros en las Consultas
Para las condiciones se utiliza la cláusula Where de la siguiente manera:

SQL
SELECT P.nombre, O.nombre AS odontologo, C.fecha_inicio, C.estado
FROM citas AS C
JOIN pacientes AS P ON P.id = C.paciente_id
JOIN odontologos AS O ON O.id = C.odontologo_id
WHERE C.estado = 'COMPLETADA';
1.6 Consultas con filtros condicional LIKE
SQL
SELECT * 
FROM pacientes AS P 
WHERE P.nombre LIKE 'M%';
1.7 Consultas con filtros condicionales BETWEEN
SQL
SELECT P.nombre AS paciente, C.fecha_inicio, C.motivo, O.nombre AS odontologo
FROM citas C
JOIN pacientes P ON P.id = C.paciente_id
JOIN odontologos O ON O.id = C.odontologo_id
WHERE C.fecha_inicio BETWEEN '2026-03-01 00:00:00' AND '2026-04-30 23:59:59'
ORDER BY C.fecha_inicio ASC;
1.8 Consultas con agrupamiento GROUP BY
Se consideran este tipo de consultas cuando tenemos valores que se repiten en los registros.

SQL
SELECT metodo, SUM(monto) AS TotalRecaudado, COUNT(id) AS CantidadPagos
FROM pagos
WHERE estado = 'COMPLETADO'
GROUP BY metodo
ORDER BY TotalRecaudado DESC;
1.9 Subconsultas y teoría de conjuntos
En las Subconsultas podemos realizar la teoría de conjuntos aplicada a las bases de datos:

Teniendo en cuenta las tablas, muestre los pacientes que no han tenido citas en una fecha de inicio específica.

SQL
SELECT * 
FROM pacientes AS P 
WHERE P.id NOT IN (
    SELECT C.paciente_id 
    FROM citas AS C 
    WHERE C.fecha_inicio BETWEEN '2026-03-01' AND '2026-03-31'
);

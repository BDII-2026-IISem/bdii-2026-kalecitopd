# CONSULTAS AVANZADAS SQL - OdontoNova

## Imagenes de los registros de cada tabla creada :

![pacientes](images/T1.png)

![odontologos](images/T2.png)

![sillones](images/T3.png)

![citas](images/T4.png)

![historias_clinicas](images/T5.png)

![planes_tratamiento](images/T6.png)

![procedimientos](images/T7.png)

![detalles_tratamiento](images/T8.png)

![sesiones_clinicas](images/T9.png)

![pagos](images/T10.png)

## 1. Consultas avanzadas en MySQL :

### 1.1 Mostrar algunos de los registros de la tabla pacientes

``` sql
SELECT nombre, tipo_documento, numero_documento, is_active FROM pacientes LIMIT 10;
```

![](images/1.png)

### 1.2 Mostrar de forma ordenada (DESC) las citas desde la mas reciente

``` sql
SELECT id, fecha_inicio, fecha_fin, motivo, estado FROM citas ORDER BY fecha_inicio DESC;
```

![](images/2.png)

### 1.3 Consultas a múltiples tablas mediante WHERE

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id;
```

![](images/3.png)

### 1.4 Consultas a múltiples tablas mediante JOIN

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
JOIN odontologos AS o ON o.id = c.odontologo_id
JOIN sillones AS s ON s.id = c.sillon_id;
```

![](images/4.png)

### 1.5 Condiciones o filtros en las Consultas

Para las condiciones se utiliza la clausula WHERE. Se repite la consulta anterior filtrando por un estado especifico de la cita.

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.estado = 'programada';
```

![](images/5.png)

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
JOIN odontologos AS o ON o.id = c.odontologo_id
WHERE c.estado = 'cancelada';
```

![](images/6.png)

### 1.6 Consultas con filtro condicional LIKE

``` sql
SELECT * FROM pacientes AS p WHERE p.nombre LIKE 'M%';
```

![](images/7.png)

**Mostrar todos los procedimientos que contengan la palabra Limpieza**

``` sql
SELECT * FROM procedimientos AS pr WHERE pr.nombre LIKE CONCAT('%', 'Limpieza', '%');
```

![](images/8.png)

**Combinacion del punto 1.5 y la implementacion del LIKE**

``` sql
SELECT c.id, p.nombre AS paciente, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
WHERE c.estado = 'cancelada' AND p.nombre LIKE 'M%';
```

![](images/9.png)

### 1.7 Consultas con filtro condicional BETWEEN

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
JOIN odontologos o ON o.id = c.odontologo_id
JOIN sillones s ON s.id = c.sillon_id
WHERE c.fecha_inicio BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
ORDER BY c.fecha_inicio ASC;
```

![](images/10.png)

**Forma 2:**

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id
  AND c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30'
ORDER BY c.fecha_inicio ASC;
```

![](images/11.png)

### 1.8 Consultas con agrupamiento GROUP BY

Se consideran este tipo de consultas cuando tenemos valores que se repiten en los registros.

**Forma 1 con el where:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, COUNT(pg.id) AS CuentaTotal, AVG(pg.monto) AS Promedio
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
WHERE pg.fecha BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
GROUP BY p.id, p.nombre
ORDER BY TotalSuma DESC;
```

![](images/12.png)

**Forma 1 (estado y metodo de pago):**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalGasto, COUNT(pg.id) AS CantidadPagos
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
WHERE pg.estado = 'pagado' AND pg.metodo = 'tarjeta'
GROUP BY p.id, p.nombre
ORDER BY TotalGasto DESC;
```

![](images/13.png)

**Forma 2 con el having:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, AVG(pg.monto) AS PromedioPago
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
GROUP BY p.id, p.nombre
HAVING SUM(pg.monto) >= 100000
ORDER BY TotalSuma DESC;
```

![](images/14.png)

**WHERE + HAVING (citas por odontologo):**

``` sql
SELECT o.id, o.nombre, COUNT(c.id) AS TotalCitas
FROM odontologos AS o
JOIN citas AS c ON c.odontologo_id = o.id
WHERE c.fecha_inicio BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
GROUP BY o.id, o.nombre
HAVING COUNT(c.id) >= 3
ORDER BY TotalCitas DESC;
```

![](images/15.png)

### 1.9 Subconsultas y teoría de conjuntos

En las Sub Consultas podemos realizar la teoría de conjuntos aplicadas a las bases de datos. Teniendo en cuenta las tablas pacientes y citas, muestre los pacientes que no tienen citas en un rango de fechas.

``` sql
SELECT * FROM pacientes AS p
WHERE p.id NOT IN (
    SELECT c.paciente_id FROM citas AS c
    WHERE c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30'
);
```

![](images/16.png)

**Forma 2:**

``` sql
SELECT p.*
FROM pacientes AS p
LEFT JOIN citas AS c ON (p.id = c.paciente_id AND c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30')
WHERE c.paciente_id IS NULL;
```

![](images/17.png)

## 2. Consultas avanzadas en PostgreSQL :

### 2.1 Mostrar algunos de los registros de la tabla pacientes

``` sql
SELECT nombre, tipo_documento, numero_documento, is_active FROM pacientes LIMIT 10;
```

![](images/18.png)

### 2.2 Mostrar de forma ordenada (DESC) las citas desde la mas reciente

``` sql
SELECT id, fecha_inicio, fecha_fin, motivo, estado FROM citas ORDER BY fecha_inicio DESC;
```

![](images/19.png)

### 2.3 Consultas a múltiples tablas mediante WHERE

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id;
```

![](images/20.png)

### 2.4 Consultas a múltiples tablas mediante JOIN

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
JOIN odontologos AS o ON o.id = c.odontologo_id
JOIN sillones AS s ON s.id = c.sillon_id;
```

![](images/21.png)

### 2.5 Condiciones o filtros en las Consultas

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.estado = 'programada';
```

![](images/22.png)

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
JOIN odontologos AS o ON o.id = c.odontologo_id
WHERE c.estado = 'cancelada';
```

![](images/23.png)

### 2.6 Consultas con filtro condicional LIKE

``` sql
SELECT * FROM pacientes AS p WHERE p.nombre LIKE 'M%';
```

![](images/24.png)

**Mostrar todos los procedimientos que contengan la palabra Limpieza**

``` sql
SELECT * FROM procedimientos AS pr WHERE pr.nombre LIKE CONCAT('%', 'Limpieza', '%');
```

![](images/25.png)

**Combinacion del punto 2.5 y la implementacion del LIKE**

``` sql
SELECT c.id, p.nombre AS paciente, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
WHERE c.estado = 'cancelada' AND p.nombre LIKE 'M%';
```

![](images/26.png)

### 2.7 Consultas con filtro condicional BETWEEN

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
JOIN odontologos o ON o.id = c.odontologo_id
JOIN sillones s ON s.id = c.sillon_id
WHERE c.fecha_inicio BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
ORDER BY c.fecha_inicio ASC;
```

![](images/27.png)

**Forma 2:**

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id
  AND c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30'
ORDER BY c.fecha_inicio ASC;
```

![](images/28.png)

### 2.8 Consultas con agrupamiento GROUP BY

**Forma 1 con el where:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, COUNT(pg.id) AS CuentaTotal, AVG(pg.monto) AS Promedio
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
WHERE pg.fecha BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
GROUP BY p.id, p.nombre
ORDER BY TotalSuma DESC;
```

![](images/29.png)

**Forma 1 (estado y metodo de pago):**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalGasto, COUNT(pg.id) AS CantidadPagos
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
WHERE pg.estado = 'pagado' AND pg.metodo = 'tarjeta'
GROUP BY p.id, p.nombre
ORDER BY TotalGasto DESC;
```

![](images/30.png)

**Forma 2 con el having:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, AVG(pg.monto) AS PromedioPago
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
GROUP BY p.id, p.nombre
HAVING SUM(pg.monto) >= 100000
ORDER BY TotalSuma DESC;
```

![](images/31.png)

**WHERE + HAVING (citas por odontologo):**

``` sql
SELECT o.id, o.nombre, COUNT(c.id) AS TotalCitas
FROM odontologos AS o
JOIN citas AS c ON c.odontologo_id = o.id
WHERE c.fecha_inicio BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
GROUP BY o.id, o.nombre
HAVING COUNT(c.id) >= 3
ORDER BY TotalCitas DESC;
```

![](images/32.png)

### 2.9 Subconsultas y teoría de conjuntos

``` sql
SELECT * FROM pacientes AS p
WHERE p.id NOT IN (
    SELECT c.paciente_id FROM citas AS c
    WHERE c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30'
);
```

![](images/33.png)

**Forma 2:**

``` sql
SELECT p.*
FROM pacientes AS p
LEFT JOIN citas AS c ON (p.id = c.paciente_id AND c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30')
WHERE c.paciente_id IS NULL;
```

![](images/34.png)

## 3. Consultas avanzadas en MSSQL :

### 3.1 Mostrar algunos de los registros de la tabla pacientes

``` sql
SELECT TOP 10 nombre, tipo_documento, numero_documento, is_active FROM pacientes;
```

![](images/35.png)

### 3.2 Mostrar de forma ordenada (DESC) las citas desde la mas reciente

``` sql
SELECT id, fecha_inicio, fecha_fin, motivo, estado FROM citas ORDER BY fecha_inicio DESC;
```

![](images/36.png)

### 3.3 Consultas a múltiples tablas mediante WHERE

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id;
```

![](images/37.png)

### 3.4 Consultas a múltiples tablas mediante JOIN

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
JOIN odontologos AS o ON o.id = c.odontologo_id
JOIN sillones AS s ON s.id = c.sillon_id;
```

![](images/38.png)

### 3.5 Condiciones o filtros en las Consultas

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.estado = 'programada';
```

![](images/39.png)

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
JOIN odontologos AS o ON o.id = c.odontologo_id
WHERE c.estado = 'cancelada';
```

![](images/40.png)

### 3.6 Consultas con filtro condicional LIKE

``` sql
SELECT * FROM pacientes AS p WHERE p.nombre LIKE 'M%';
```

![](images/41.png)

**Mostrar todos los procedimientos que contengan la palabra Limpieza**

``` sql
SELECT * FROM procedimientos AS pr WHERE pr.nombre LIKE CONCAT('%', 'Limpieza', '%');
```

![](images/42.png)

**Combinacion del punto 3.5 y la implementacion del LIKE**

``` sql
SELECT c.id, p.nombre AS paciente, c.fecha_inicio, c.estado
FROM citas AS c
JOIN pacientes AS p ON p.id = c.paciente_id
WHERE c.estado = 'cancelada' AND p.nombre LIKE 'M%';
```

![](images/43.png)

### 3.7 Consultas con filtro condicional BETWEEN

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
JOIN odontologos o ON o.id = c.odontologo_id
JOIN sillones s ON s.id = c.sillon_id
WHERE c.fecha_inicio BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
ORDER BY c.fecha_inicio ASC;
```

![](images/44.png)

**Forma 2:**

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id
  AND c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30'
ORDER BY c.fecha_inicio ASC;
```

![](images/45.png)

### 3.8 Consultas con agrupamiento GROUP BY

**Forma 1 con el where:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, COUNT(pg.id) AS CuentaTotal, AVG(pg.monto) AS Promedio
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
WHERE pg.fecha BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
GROUP BY p.id, p.nombre
ORDER BY TotalSuma DESC;
```

![](images/46.png)

**Forma 1 (estado y metodo de pago):**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalGasto, COUNT(pg.id) AS CantidadPagos
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
WHERE pg.estado = 'pagado' AND pg.metodo = 'tarjeta'
GROUP BY p.id, p.nombre
ORDER BY TotalGasto DESC;
```

![](images/47.png)

**Forma 2 con el having:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, AVG(pg.monto) AS PromedioPago
FROM pacientes AS p
JOIN planes_tratamiento AS pt ON pt.paciente_id = p.id
JOIN pagos AS pg ON pg.referencia_id = pt.id
GROUP BY p.id, p.nombre
HAVING SUM(pg.monto) >= 100000
ORDER BY TotalSuma DESC;
```

![](images/48.png)

**WHERE + HAVING (citas por odontologo):**

``` sql
SELECT o.id, o.nombre, COUNT(c.id) AS TotalCitas
FROM odontologos AS o
JOIN citas AS c ON c.odontologo_id = o.id
WHERE c.fecha_inicio BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59'
GROUP BY o.id, o.nombre
HAVING COUNT(c.id) >= 3
ORDER BY TotalCitas DESC;
```

![](images/49.png)

### 3.9 Subconsultas y teoría de conjuntos

``` sql
SELECT * FROM pacientes AS p
WHERE p.id NOT IN (
    SELECT c.paciente_id FROM citas AS c
    WHERE c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30'
);
```

![](images/50.png)

**Forma 2:**

``` sql
SELECT p.*
FROM pacientes AS p
LEFT JOIN citas AS c ON (p.id = c.paciente_id AND c.fecha_inicio BETWEEN '2026-01-01' AND '2026-06-30')
WHERE c.paciente_id IS NULL;
```

![](images/51.png)

## 4. Consultas avanzadas en Oracle :

### 4.1 Mostrar algunos de los registros de la tabla pacientes

``` sql
SELECT nombre, tipo_documento, numero_documento, is_active FROM pacientes FETCH FIRST 10 ROWS ONLY;
```

![](images/52.png)

### 4.2 Mostrar de forma ordenada (DESC) las citas desde la mas reciente

``` sql
SELECT id, fecha_inicio, fecha_fin, motivo, estado FROM citas ORDER BY fecha_inicio DESC;
```

![](images/53.png)

### 4.3 Consultas a múltiples tablas mediante WHERE

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id;
```

![](images/54.png)

### 4.4 Consultas a múltiples tablas mediante JOIN

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
JOIN odontologos o ON o.id = c.odontologo_id
JOIN sillones s ON s.id = c.sillon_id;
```

![](images/55.png)

### 4.5 Condiciones o filtros en las Consultas

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.estado = 'programada';
```

![](images/56.png)

``` sql
SELECT c.id, p.nombre AS paciente, o.nombre AS odontologo, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
JOIN odontologos o ON o.id = c.odontologo_id
WHERE c.estado = 'cancelada';
```

![](images/57.png)

### 4.6 Consultas con filtro condicional LIKE

``` sql
SELECT * FROM pacientes p WHERE p.nombre LIKE 'M%';
```

![](images/58.png)

**Mostrar todos los procedimientos que contengan la palabra Limpieza**

``` sql
SELECT * FROM procedimientos pr WHERE pr.nombre LIKE '%' || 'Limpieza' || '%';
```

![](images/59.png)

**Combinacion del punto 4.5 y la implementacion del LIKE**

``` sql
SELECT c.id, p.nombre AS paciente, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
WHERE c.estado = 'cancelada' AND p.nombre LIKE 'M%';
```

![](images/60.png)

### 4.7 Consultas con filtro condicional BETWEEN

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c
JOIN pacientes p ON p.id = c.paciente_id
JOIN odontologos o ON o.id = c.odontologo_id
JOIN sillones s ON s.id = c.sillon_id
WHERE c.fecha_inicio BETWEEN TIMESTAMP '2026-01-01 00:00:00' AND TIMESTAMP '2026-12-31 23:59:59'
ORDER BY c.fecha_inicio ASC;
```

![](images/61.png)

**Forma 2:**

``` sql
SELECT p.nombre AS paciente, o.nombre AS odontologo, s.nombre AS sillon, c.fecha_inicio, c.estado
FROM citas c, pacientes p, odontologos o, sillones s
WHERE c.paciente_id = p.id AND c.odontologo_id = o.id AND c.sillon_id = s.id
  AND c.fecha_inicio BETWEEN DATE '2026-01-01' AND DATE '2026-06-30'
ORDER BY c.fecha_inicio ASC;
```

![](images/62.png)

### 4.8 Consultas con agrupamiento GROUP BY

**Forma 1 con el where:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, COUNT(pg.id) AS CuentaTotal, AVG(pg.monto) AS Promedio
FROM pacientes p
JOIN planes_tratamiento pt ON pt.paciente_id = p.id
JOIN pagos pg ON pg.referencia_id = pt.id
WHERE pg.fecha BETWEEN TIMESTAMP '2026-01-01 00:00:00' AND TIMESTAMP '2026-12-31 23:59:59'
GROUP BY p.id, p.nombre
ORDER BY TotalSuma DESC;
```

![](images/63.png)

**Forma 1 (estado y metodo de pago):**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalGasto, COUNT(pg.id) AS CantidadPagos
FROM pacientes p
JOIN planes_tratamiento pt ON pt.paciente_id = p.id
JOIN pagos pg ON pg.referencia_id = pt.id
WHERE pg.estado = 'pagado' AND pg.metodo = 'tarjeta'
GROUP BY p.id, p.nombre
ORDER BY TotalGasto DESC;
```

![](images/64.png)

**Forma 2 con el having:**

``` sql
SELECT p.id, p.nombre, SUM(pg.monto) AS TotalSuma, AVG(pg.monto) AS PromedioPago
FROM pacientes p
JOIN planes_tratamiento pt ON pt.paciente_id = p.id
JOIN pagos pg ON pg.referencia_id = pt.id
GROUP BY p.id, p.nombre
HAVING SUM(pg.monto) >= 100000
ORDER BY TotalSuma DESC;
```

![](images/65.png)

**WHERE + HAVING (citas por odontologo):**

``` sql
SELECT o.id, o.nombre, COUNT(c.id) AS TotalCitas
FROM odontologos o
JOIN citas c ON c.odontologo_id = o.id
WHERE c.fecha_inicio BETWEEN TIMESTAMP '2026-01-01 00:00:00' AND TIMESTAMP '2026-12-31 23:59:59'
GROUP BY o.id, o.nombre
HAVING COUNT(c.id) >= 3
ORDER BY TotalCitas DESC;
```

![](images/66.png)

### 4.9 Subconsultas y teoría de conjuntos

``` sql
SELECT * FROM pacientes p
WHERE p.id NOT IN (
    SELECT c.paciente_id FROM citas c
    WHERE c.fecha_inicio BETWEEN DATE '2026-01-01' AND DATE '2026-06-30'
);
```

![](images/67.png)

**Forma 2:**

``` sql
SELECT p.*
FROM pacientes p
LEFT JOIN citas c ON (p.id = c.paciente_id AND c.fecha_inicio BETWEEN DATE '2026-01-01' AND DATE '2026-06-30')
WHERE c.paciente_id IS NULL;
```

![](images/68.png)

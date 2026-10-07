### Consulta 1: Citas completas

```sql
CREATE OR REPLACE FUNCTION sp_pg_q1_citas_completas()
RETURNS TABLE (id_cita INT, paciente VARCHAR, odontologo VARCHAR, sillon VARCHAR, fecha_hora TIMESTAMP, motivo VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT c.id_cita, (p.nombre || ' ' || p.apellido)::VARCHAR, (o.nombre || ' ' || o.apellido)::VARCHAR, s.numero_sillon::VARCHAR, c.fecha_hora, c.motivo::VARCHAR, c.estado::VARCHAR 
    FROM citas c 
    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente 
    INNER JOIN odontologos o ON c.id_odontologo = o.id_odontologo 
    INNER JOIN sillones s ON c.id_sillon = s.id_sillon 
    WHERE c.estado = 'completada'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q1_citas_completas();
```

![Resultado Consulta 1](img/1.png)

### Consulta 2: Ver historial clínico de un paciente específico

```sql
CREATE OR REPLACE FUNCTION sp_pg_q2_historial_paciente(p_id INT)
RETURNS TABLE (id_historia INT, paciente VARCHAR, antecedentes VARCHAR, diagnostico VARCHAR, fecha_creacion DATE) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT h.id_historia, (p.nombre || ' ' || p.apellido)::VARCHAR, h.antecedentes::VARCHAR, h.diagnostico::VARCHAR, h.fecha_creacion 
    FROM historias_clinicas h 
    INNER JOIN pacientes p ON h.id_paciente = p.id_paciente 
    WHERE h.id_paciente = p_id; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q2_historial_paciente(1);
```

![Resultado Consulta 2](img/2.png)

### Consulta 3: Consultar pagos ordenados por monto

```sql
CREATE OR REPLACE FUNCTION sp_pg_q3_pagos_ordenados()
RETURNS TABLE (id_pago INT, id_cita INT, monto NUMERIC, fecha_pago DATE, metodo_pago VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT p.id_pago, p.id_cita, p.monto, p.fecha_pago, p.metodo_pago::VARCHAR, p.estado::VARCHAR 
    FROM pagos p ORDER BY p.monto DESC; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q3_pagos_ordenados();
```

![Resultado Consulta 3](img/3.png)

### Consulta 4: Detalles de tratamiento y procedimientos aplicados

```sql
CREATE OR REPLACE FUNCTION sp_pg_q4_detalles_tratamiento()
RETURNS TABLE (id_detalle INT, id_plan INT, procedimiento VARCHAR, costo NUMERIC, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT d.id_detalle, d.id_plan, pr.nombre_procedimiento::VARCHAR, d.costo, d.estado::VARCHAR 
    FROM detalles_tratamiento d 
    INNER JOIN procedimientos pr ON d.id_procedimiento = pr.id_procedimiento; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q4_detalles_tratamiento();
```

![Resultado Consulta 4](img/4.png)

### Consulta 5: Resumen financiero de pagos completados

```sql
CREATE OR REPLACE FUNCTION sp_pg_q5_resumen_completados()
RETURNS TABLE (total_pagos BIGINT, suma_monto NUMERIC) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT COUNT(p.id_pago), COALESCE(SUM(p.monto), 0) 
    FROM pagos p WHERE p.estado = 'completado'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q5_resumen_completados();
```

![Resultado Consulta 5](img/5.png)

### Consulta 6: Planes de tratamiento activos

```sql
CREATE OR REPLACE FUNCTION sp_pg_q6_planes_activos()
RETURNS TABLE (id_plan INT, paciente VARCHAR, descripcion VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT pl.id_plan, (p.nombre || ' ' || p.apellido)::VARCHAR, pl.descripcion::VARCHAR, pl.estado::VARCHAR 
    FROM planes_tratamiento pl 
    INNER JOIN pacientes p ON pl.id_paciente = p.id_paciente 
    WHERE pl.estado = 'activo'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q6_planes_activos();
```

![Resultado Consulta 6](img/6.png)

### Consulta 7: Odontólogos con citas activas

```sql
CREATE OR REPLACE FUNCTION sp_pg_q7_odontologos_activos_citas()
RETURNS TABLE (id_odontologo INT, odontologo VARCHAR, especialidad VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT DISTINCT o.id_odontologo, (o.nombre || ' ' || o.apellido)::VARCHAR, o.especialidad::VARCHAR 
    FROM odontologos o 
    INNER JOIN citas c ON o.id_odontologo = c.id_odontologo 
    WHERE c.estado IN ('programada', 'completada'); 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q7_odontologos_activos_citas();
```

![Resultado Consulta 7](img/7.png)

### Consulta 8: Sesiones clínicas registradas

```sql
CREATE OR REPLACE FUNCTION sp_pg_q8_sesiones_clinicas()
RETURNS TABLE (id_sesion INT, id_cita INT, observaciones VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT s.id_sesion, s.id_cita, s.observaciones::VARCHAR, s.estado::VARCHAR 
    FROM sesiones_clinicas s; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q8_sesiones_clinicas();
```

![Resultado Consulta 8](img/8.png)

### Consulta 9: Sillones odontológicos activos

```sql
CREATE OR REPLACE FUNCTION sp_pg_q9_sillones_activos()
RETURNS TABLE (id_sillon INT, numero_sillon VARCHAR, ubicacion VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT s.id_sillon, s.numero_sillon::VARCHAR, s.ubicacion::VARCHAR, s.estado::VARCHAR 
    FROM sillones s WHERE s.estado = 'activo'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q9_sillones_activos();
```

![Resultado Consulta 9](img/9.png)

### Consulta 10: Búsqueda de paciente por documento de identidad

```sql
CREATE OR REPLACE FUNCTION sp_pg_q10_buscar_paciente_doc(p_doc VARCHAR)
RETURNS TABLE (id_paciente INT, paciente VARCHAR, documento VARCHAR, email VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT p.id_paciente, (p.nombre || ' ' || p.apellido)::VARCHAR, p.documento::VARCHAR, p.email::VARCHAR 
    FROM pacientes p WHERE p.documento = p_doc; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q10_buscar_paciente_doc('1001234567');
```

![Resultado Consulta 10](img/10.png)

### Consulta 11: Listado general de odontólogos activos

```sql
CREATE OR REPLACE FUNCTION sp_pg_q11_odontologos_activos()
RETURNS TABLE (id_odontologo INT, odontologo VARCHAR, especialidad VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT o.id_odontologo, (o.nombre || ' ' || o.apellido)::VARCHAR, o.especialidad::VARCHAR 
    FROM odontologos o WHERE o.estado = 'activo'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q11_odontologos_activos();
```

![Resultado Consulta 11](img/11.png)

### Consulta 12: Citas canceladas y sus motivos

```sql
CREATE OR REPLACE FUNCTION sp_pg_q12_citas_canceladas()
RETURNS TABLE (id_cita INT, paciente VARCHAR, motivo VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT c.id_cita, (p.nombre || ' ' || p.apellido)::VARCHAR, c.motivo::VARCHAR, c.estado::VARCHAR 
    FROM citas c 
    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente 
    WHERE c.estado = 'cancelada'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q12_citas_canceladas();
```

![Resultado Consulta 12](img/12.png)

### Consulta 13: Catálogo de procedimientos activos

```sql
CREATE OR REPLACE FUNCTION sp_pg_q13_procedimientos_activos()
RETURNS TABLE (id_procedimiento INT, procedimiento VARCHAR, costo NUMERIC) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT pr.id_procedimiento, pr.nombre_procedimiento::VARCHAR, pr.costo 
    FROM procedimientos pr WHERE pr.estado = 'activo'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q13_procedimientos_activos();
```

![Resultado Consulta 13](img/13.png)

### Consulta 14: Total de citas acumuladas por paciente

```sql
CREATE OR REPLACE FUNCTION sp_pg_q14_citas_por_paciente()
RETURNS TABLE (paciente VARCHAR, total_citas BIGINT) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT (p.nombre || ' ' || p.apellido)::VARCHAR, COUNT(c.id_cita) 
    FROM pacientes p 
    LEFT JOIN citas c ON p.id_paciente = c.id_paciente 
    GROUP BY p.id_paciente, p.nombre, p.apellido; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q14_citas_por_paciente();
```

![Resultado Consulta 14](img/14.png)

### Consulta 15: Balance de dinero pendiente por cobro

```sql
CREATE OR REPLACE FUNCTION sp_pg_q15_dinero_pendiente()
RETURNS TABLE (total_pendiente NUMERIC) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT COALESCE(SUM(p.monto), 0) 
    FROM pagos p WHERE p.estado = 'pendiente'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q15_dinero_pendiente();
```

![Resultado Consulta 15](img/15.png)

### Consulta 16: Historias clínicas activas

```sql
CREATE OR REPLACE FUNCTION sp_pg_q16_historias_activas()
RETURNS TABLE (id_historia INT, paciente VARCHAR, diagnostico VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT h.id_historia, (p.nombre || ' ' || p.apellido)::VARCHAR, h.diagnostico::VARCHAR 
    FROM historias_clinicas h 
    INNER JOIN pacientes p ON h.id_paciente = p.id_paciente 
    WHERE h.estado = 'activa'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q16_historias_activas();
```

![Resultado Consulta 16](img/16.png)

### Consulta 17: Detalles de tratamiento con costo superior a $150,000

```sql
CREATE OR REPLACE FUNCTION sp_pg_q17_detalles_mayores()
RETURNS TABLE (id_detalle INT, procedimiento VARCHAR, costo NUMERIC) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT d.id_detalle, pr.nombre_procedimiento::VARCHAR, d.costo 
    FROM detalles_tratamiento d 
    INNER JOIN procedimientos pr ON d.id_procedimiento = pr.id_procedimiento 
    WHERE d.costo > 150000; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q17_detalles_mayores();
```

![Resultado Consulta 17](img/17.png)

### Consulta 18: Pacientes ordenados cronológicamente por fecha de nacimiento

```sql
CREATE OR REPLACE FUNCTION sp_pg_q18_pacientes_por_nacimiento()
RETURNS TABLE (id_paciente INT, paciente VARCHAR, fecha_nacimiento DATE) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT p.id_paciente, (p.nombre || ' ' || p.apellido)::VARCHAR, p.fecha_nacimiento 
    FROM pacientes p ORDER BY p.fecha_nacimiento ASC; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q18_pacientes_por_nacimiento();
```

![Resultado Consulta 18](img/18.png)

### Consulta 19: Sesiones clínicas completadas

```sql
CREATE OR REPLACE FUNCTION sp_pg_q19_sesiones_completadas()
RETURNS TABLE (id_sesion INT, id_cita INT, observaciones VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT s.id_sesion, s.id_cita, s.observaciones::VARCHAR 
    FROM sesiones_clinicas s WHERE s.estado = 'completada'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q19_sesiones_completadas();
```

![Resultado Consulta 19](img/19.png)

### Consulta 20: Cruce de citas con paciente y odontólogo

```sql
CREATE OR REPLACE FUNCTION sp_pg_q20_citas_paciente_odontologo()
RETURNS TABLE (id_cita INT, paciente VARCHAR, odontologo VARCHAR, fecha_hora TIMESTAMP) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT c.id_cita, (p.nombre || ' ' || p.apellido)::VARCHAR, (o.nombre || ' ' || o.apellido)::VARCHAR, c.fecha_hora 
    FROM citas c 
    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente 
    INNER JOIN odontologos o ON c.id_odontologo = o.id_odontologo; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q20_citas_paciente_odontologo();
```

![Resultado Consulta 20](img/20.png)

### Consulta 21: Pacientes nacidos a partir del año 2010

```sql
CREATE OR REPLACE FUNCTION sp_pg_q21_pacientes_jovenes()
RETURNS TABLE (id_paciente INT, paciente VARCHAR, fecha_nacimiento DATE) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT p.id_paciente, (p.nombre || ' ' || p.apellido)::VARCHAR, p.fecha_nacimiento 
    FROM pacientes p WHERE p.fecha_nacimiento >= '2010-01-01'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q21_pacientes_jovenes();
```

![Resultado Consulta 21](img/21.png)

### Consulta 22: Estado general de agendamiento de citas

```sql
CREATE OR REPLACE FUNCTION sp_pg_q22_estado_general_citas()
RETURNS TABLE (id_cita INT, paciente VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT c.id_cita, (p.nombre || ' ' || p.apellido)::VARCHAR, c.estado::VARCHAR 
    FROM citas c INNER JOIN pacientes p ON c.id_paciente = p.id_paciente; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q22_estado_general_citas();
```

![Resultado Consulta 22](img/22.png)

### Consulta 23: Conteo consolidado de citas agrupadas por estado

```sql
CREATE OR REPLACE FUNCTION sp_pg_q23_conteo_citas_estado()
RETURNS TABLE (estado VARCHAR, total BIGINT) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT c.estado::VARCHAR, COUNT(*) FROM citas c GROUP BY c.estado; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q23_conteo_citas_estado();
```

![Resultado Consulta 23](img/23.png)

### Consulta 24: Búsqueda de odontólogos por la inicial del nombre

```sql
CREATE OR REPLACE FUNCTION sp_pg_q24_buscar_odontologos_letra(p_letra VARCHAR)
RETURNS TABLE (id_odontologo INT, odontologo VARCHAR, especialidad VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT o.id_odontologo, (o.nombre || ' ' || o.apellido)::VARCHAR, o.especialidad::VARCHAR 
    FROM odontologos o WHERE LOWER(o.nombre) LIKE LOWER(p_letra || '%'); 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q24_buscar_odontologos_letra('A');
```

![Resultado Consulta 24](img/24.png)

### Consulta 25: Pacientes registrados con estado inactivo

```sql
CREATE OR REPLACE FUNCTION sp_pg_q25_pacientes_inactivos()
RETURNS TABLE (id_paciente INT, paciente VARCHAR, documento VARCHAR, estado VARCHAR) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT p.id_paciente, (p.nombre || ' ' || p.apellido)::VARCHAR, p.documento::VARCHAR, p.estado::VARCHAR 
    FROM pacientes p WHERE p.estado = 'inactivo'; 
END; $$ LANGUAGE plpgsql;

SELECT * FROM sp_pg_q25_pacientes_inactivos();
```

![Resultado Consulta 25](img/25.png)

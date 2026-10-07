**Asignatura:** Base de Datos II  
**Proyecto:** OdontoNova  
**Motor:** PostgreSQL 16 (WSL2 / Windows)  

---

## Documentación de Funciones, Invocaciones y Resultados

### 1. Citas Completas
**Código de la Función:**
```sql
CREATE OR REPLACE FUNCTION sp_pg_q1_citas_completas()
RETURNS TABLE (id_cita INT, paciente VARCHAR, odontologo VARCHAR, sillon VARCHAR, fecha_hora TIMESTAMP, motivo VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT c.id_cita, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, (o.nombre \vert{}\vert{} ' ' \vert{}\vert{} o.apellido)::VARCHAR, s.numero_sillon::VARCHAR, c.fecha_hora, c.motivo::VARCHAR, c.estado::VARCHAR     FROM citas c     INNER JOIN pacientes p ON c.id_paciente = p.id_paciente     INNER JOIN odontologos o ON c.id_odontologo = o.id_odontologo     INNER JOIN sillones s ON c.id_sillon = s.id_sillon     WHERE c.estado = 'completada'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q1_citas_completas();
Resultado en DBeaver:

2. Historial Clínico de Paciente
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q2_historial_paciente(p_id INT)
RETURNS TABLE (id_historia INT, paciente VARCHAR, antecedentes VARCHAR, diagnostico VARCHAR, fecha_creacion DATE) AS $$ BEGIN     RETURN QUERY     SELECT h.id_historia, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, h.antecedentes::VARCHAR, h.diagnostico::VARCHAR, h.fecha_creacion     FROM historias_clinicas h     INNER JOIN pacientes p ON h.id_paciente = p.id_paciente     WHERE h.id_paciente = p_id; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q2_historial_paciente(1);
Resultado en DBeaver:

3. Pagos Ordenados por Monto
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q3_pagos_ordenados()
RETURNS TABLE (id_pago INT, id_cita INT, monto NUMERIC, fecha_pago DATE, metodo_pago VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT p.id_pago, p.id_cita, p.monto, p.fecha_pago, p.metodo_pago::VARCHAR, p.estado::VARCHAR     FROM pagos p ORDER BY p.monto DESC; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q3_pagos_ordenados();
Resultado en DBeaver:

4. Detalles de Tratamiento
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q4_detalles_tratamiento()
RETURNS TABLE (id_detalle INT, id_plan INT, procedimiento VARCHAR, costo NUMERIC, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT d.id_detalle, d.id_plan, pr.nombre_procedimiento::VARCHAR, d.costo, d.estado::VARCHAR     FROM detalles_tratamiento d     INNER JOIN procedimientos pr ON d.id_procedimiento = pr.id_procedimiento; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q4_detalles_tratamiento();
Resultado en DBeaver:

5. Resumen de Pagos Completados
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q5_resumen_completados()
RETURNS TABLE (total_pagos BIGINT, suma_monto NUMERIC) AS $$ BEGIN     RETURN QUERY     SELECT COUNT(p.id_pago), COALESCE(SUM(p.monto), 0)     FROM pagos p WHERE p.estado = 'completado'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q5_resumen_completados();
Resultado en DBeaver:

6. Planes de Tratamiento Activos
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q6_planes_activos()
RETURNS TABLE (id_plan INT, paciente VARCHAR, descripcion VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT pl.id_plan, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, pl.descripcion::VARCHAR, pl.estado::VARCHAR     FROM planes_tratamiento pl     INNER JOIN pacientes p ON pl.id_paciente = p.id_paciente     WHERE pl.estado = 'activo'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q6_planes_activos();
Resultado en DBeaver:

7. Odontólogos con Citas Activas
Código de la Función:

CREATE OR REPLACE FUNCTION sp_pg_q7_odontologos_activos_citas()
RETURNS TABLE (id_odontologo INT, odontologo VARCHAR, especialidad VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT DISTINCT o.id_odontologo, (o.nombre \vert{}\vert{} ' ' \vert{}\vert{} o.apellido)::VARCHAR, o.especialidad::VARCHAR     FROM odontologos o     INNER JOIN citas c ON o.id_odontologo = c.id_odontologo     WHERE c.estado IN ('programada', 'completada'); END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q7_odontologos_activos_citas();
Resultado en DBeaver:

8. Sesiones Clínicas
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q8_sesiones_clinicas()
RETURNS TABLE (id_sesion INT, id_cita INT, observaciones VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT s.id_sesion, s.id_cita, s.observaciones::VARCHAR, s.estado::VARCHAR     FROM sesiones_clinicas s; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q8_sesiones_clinicas();
Resultado en DBeaver:

9. Sillones Activos
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q9_sillones_activos()
RETURNS TABLE (id_sillon INT, numero_sillon VARCHAR, ubicacion VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT s.id_sillon, s.numero_sillon::VARCHAR, s.ubicacion::VARCHAR, s.estado::VARCHAR     FROM sillones s WHERE s.estado = 'activo'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q9_sillones_activos();
Resultado en DBeaver:

10. Búsqueda de Paciente por Documento
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q10_buscar_paciente_doc(p_doc VARCHAR)
RETURNS TABLE (id_paciente INT, paciente VARCHAR, documento VARCHAR, email VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT p.id_paciente, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, p.documento::VARCHAR, p.email::VARCHAR     FROM pacientes p WHERE p.documento = p_doc; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q10_buscar_paciente_doc('1001234567');
Resultado en DBeaver:

11. Odontólogos Activos
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q11_odontologos_activos()
RETURNS TABLE (id_odontologo INT, odontologo VARCHAR, especialidad VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT o.id_odontologo, (o.nombre \vert{}\vert{} ' ' \vert{}\vert{} o.apellido)::VARCHAR, o.especialidad::VARCHAR     FROM odontologos o WHERE o.estado = 'activo'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q11_odontologos_activos();
Resultado en DBeaver:

12. Citas Canceladas
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q12_citas_canceladas()
RETURNS TABLE (id_cita INT, paciente VARCHAR, motivo VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT c.id_cita, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, c.motivo::VARCHAR, c.estado::VARCHAR     FROM citas c     INNER JOIN pacientes p ON c.id_paciente = p.id_paciente     WHERE c.estado = 'cancelada'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q12_citas_canceladas();
Resultado en DBeaver:

13. Procedimientos Activos
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q13_procedimientos_activos()
RETURNS TABLE (id_procedimiento INT, procedimiento VARCHAR, costo NUMERIC) AS $$ BEGIN     RETURN QUERY     SELECT pr.id_procedimiento, pr.nombre_procedimiento::VARCHAR, pr.costo     FROM procedimientos pr WHERE pr.estado = 'activo'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q13_procedimientos_activos();
Resultado en DBeaver:

14. Total de Citas por Paciente
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q14_citas_por_paciente()
RETURNS TABLE (paciente VARCHAR, total_citas BIGINT) AS $$ BEGIN     RETURN QUERY     SELECT (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, COUNT(c.id_cita)     FROM pacientes p     LEFT JOIN citas c ON p.id_paciente = c.id_paciente     GROUP BY p.id_paciente, p.nombre, p.apellido; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q14_citas_por_paciente();
Resultado en DBeaver:

15. Dinero Pendiente por Cobro
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q15_dinero_pendiente()
RETURNS TABLE (total_pendiente NUMERIC) AS $$ BEGIN     RETURN QUERY     SELECT COALESCE(SUM(p.monto), 0)     FROM pagos p WHERE p.estado = 'pendiente'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q15_dinero_pendiente();
Resultado en DBeaver:

16. Historias Clínicas Activas
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q16_historias_activas()
RETURNS TABLE (id_historia INT, paciente VARCHAR, diagnostico VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT h.id_historia, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, h.diagnostico::VARCHAR     FROM historias_clinicas h     INNER JOIN pacientes p ON h.id_paciente = p.id_paciente     WHERE h.estado = 'activa'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q16_historias_activas();
Resultado en DBeaver:

17. Detalles de Tratamiento Mayores a $150,000
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q17_detalles_mayores()
RETURNS TABLE (id_detalle INT, procedimiento VARCHAR, costo NUMERIC) AS $$ BEGIN     RETURN QUERY     SELECT d.id_detalle, pr.nombre_procedimiento::VARCHAR, d.costo     FROM detalles_tratamiento d     INNER JOIN procedimientos pr ON d.id_procedimiento = pr.id_procedimiento     WHERE d.costo > 150000; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q17_detalles_mayores();
Resultado en DBeaver:

18. Pacientes por Fecha de Nacimiento
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q18_pacientes_por_nacimiento()
RETURNS TABLE (id_paciente INT, paciente VARCHAR, fecha_nacimiento DATE) AS $$ BEGIN     RETURN QUERY     SELECT p.id_paciente, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, p.fecha_nacimiento     FROM pacientes p ORDER BY p.fecha_nacimiento ASC; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q18_pacientes_por_nacimiento();
Resultado en DBeaver:

19. Sesiones Clínicas Completadas
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q19_sesiones_completadas()
RETURNS TABLE (id_sesion INT, id_cita INT, observaciones VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT s.id_sesion, s.id_cita, s.observaciones::VARCHAR     FROM sesiones_clinicas s WHERE s.estado = 'completada'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q19_sesiones_completadas();
Resultado en DBeaver:

20. Citas con Paciente y Odontólogo
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q20_citas_paciente_odontologo()
RETURNS TABLE (id_cita INT, paciente VARCHAR, odontologo VARCHAR, fecha_hora TIMESTAMP) AS $$ BEGIN     RETURN QUERY     SELECT c.id_cita, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, (o.nombre \vert{}\vert{} ' ' \vert{}\vert{} o.apellido)::VARCHAR, c.fecha_hora     FROM citas c     INNER JOIN pacientes p ON c.id_paciente = p.id_paciente     INNER JOIN odontologos o ON c.id_odontologo = o.id_odontologo; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q20_citas_paciente_odontologo();
Resultado en DBeaver:

21. Pacientes Nacidos Desde el 2010
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q21_pacientes_jovenes()
RETURNS TABLE (id_paciente INT, paciente VARCHAR, fecha_nacimiento DATE) AS $$ BEGIN     RETURN QUERY     SELECT p.id_paciente, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, p.fecha_nacimiento     FROM pacientes p WHERE p.fecha_nacimiento >= '2010-01-01'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q21_pacientes_jovenes();
Resultado en DBeaver:

22. Estado General de Citas
Código de la Función:

CREATE OR REPLACE FUNCTION sp_pg_q22_estado_general_citas()
RETURNS TABLE (id_cita INT, paciente VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT c.id_cita, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, c.estado::VARCHAR     FROM citas c INNER JOIN pacientes p ON c.id_paciente = p.id_paciente; END; $$ LANGUAGE plpgsql;
Invocación SQL:

SELECT * FROM sp_pg_q22_estado_general_citas();
Resultado en DBeaver:

23. Conteo de Citas por Estado
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q23_conteo_citas_estado()
RETURNS TABLE (estado VARCHAR, total BIGINT) AS $$ BEGIN     RETURN QUERY     SELECT c.estado::VARCHAR, COUNT(*) FROM citas c GROUP BY c.estado; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q23_conteo_citas_estado();
Resultado en DBeaver:

24. Búsqueda de Odontólogos por Inicial
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q24_buscar_odontologos_letra(p_letra VARCHAR)
RETURNS TABLE (id_odontologo INT, odontologo VARCHAR, especialidad VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT o.id_odontologo, (o.nombre \vert{}\vert{} ' ' \vert{}\vert{} o.apellido)::VARCHAR, o.especialidad::VARCHAR     FROM odontologos o WHERE LOWER(o.nombre) LIKE LOWER(p_letra \vert{}\vert{} '\%'); END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q24_buscar_odontologos_letra('A');
Resultado en DBeaver:

25. Pacientes Inactivos
Código de la Función:


CREATE OR REPLACE FUNCTION sp_pg_q25_pacientes_inactivos()
RETURNS TABLE (id_paciente INT, paciente VARCHAR, documento VARCHAR, estado VARCHAR) AS $$ BEGIN     RETURN QUERY     SELECT p.id_paciente, (p.nombre \vert{}\vert{} ' ' \vert{}\vert{} p.apellido)::VARCHAR, p.documento::VARCHAR, p.estado::VARCHAR     FROM pacientes p WHERE p.estado = 'inactivo'; END; $$ LANGUAGE plpgsql;
Invocación SQL:


SELECT * FROM sp_pg_q25_pacientes_inactivos();
Resultado en DBeaver:

EOF

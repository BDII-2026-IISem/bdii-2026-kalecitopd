-- =======================================================
-- SCRIPT DML: INSERCIÓN DE DATOS PARA POSTGRESQL
-- =======================================================

-- 1. Pacientes
INSERT INTO pacientes (tipo_documento, numero_documento, nombre, fecha_nacimiento, is_active) VALUES
('CC', '1098765432', 'Carlos Andrés Mendoza', '1992-05-14', TRUE),
('CC', '1012345678', 'María Fernanda Gómez', '1998-11-20', TRUE);

-- 2. Odontólogos
INSERT INTO odontologos (nombre, descripcion, is_active) VALUES
('Dr. Alejandro Silva', 'Especialista en Ortodoncia y Cirugía Maxilofacial', TRUE),
('Dra. Laura Camargo', 'Especialista en Odontopediatría y Estética Dental', TRUE);

-- 3. Sillones
INSERT INTO sillones (nombre, descripcion, is_active) VALUES
('Sillón Principal 01', 'Equipado con unidad de rayos X digital y luz LED premium', TRUE),
('Sillón Ortodoncia 02', 'Sillón ergonómico especializado para procedimientos largos', TRUE);

-- 4. Historias Clínicas
INSERT INTO historias_clinicas (paciente_id, nombre, descripcion, is_active) VALUES
(1, 'Historia Clínica - Carlos Mendoza', 'Paciente sin antecedentes alérgicos reportados', TRUE),
(2, 'Historia Clínica - María Gómez', 'Sensibilidad dental moderada tratada', TRUE);

-- 5. Citas
INSERT INTO citas (paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado) VALUES
(1, 1, 1, '2026-09-24 08:00:00', '2026-09-24 09:00:00', 'Evaluación e inicio de tratamiento', 'CONFIRMADA'),
(2, 2, 2, '2026-09-24 10:00:00', '2026-09-24 11:00:00', 'Control de rutina y mantenimiento', 'PENDIENTE');

-- 6. Planes de Tratamiento
INSERT INTO planes_tratamiento (paciente_id, nombre, descripcion, is_active) VALUES
(1, 'Plan de Ortodoncia Integral', 'Alineación dental y diseño de sonrisa', TRUE),
(2, 'Plan Preventivo y Mantenimiento', 'Limpieza general y calzas estéticas', TRUE);

-- 7. Procedimientos
INSERT INTO procedimientos (nombre, descripcion, is_active) VALUES
('Profilaxis Dental Profunda', 'Limpieza profunda con ultrasonido y pulido', TRUE),
('Ajuste de Brackets', 'Control mensual de ortodoncia y cambio de arcos', TRUE);

-- 8. Detalles de Tratamiento
INSERT INTO detalles_tratamiento (cabecera_id, item_id, cantidad, valor_unitario, total, observacion) VALUES
(1, 2, 12, 80000.00, 960000.00, 'Sesiones mensuales programadas'),
(2, 1, 1, 120000.00, 120000.00, 'Profilaxis ejecutada en primera cita');

-- 9. Sesiones Clínicas
INSERT INTO sesiones_clinicas (referencia_id, fecha_inicio, fecha_fin, total, estado, observaciones) VALUES
(1, '2026-09-24 08:00:00', '2026-09-24 09:00:00', 120000.00, 'COMPLETADA', 'Valoración inicial finalizada con éxito');

-- 10. Pagos
INSERT INTO pagos (referencia_tipo, referencia_id, metodo, monto, estado) VALUES
('PLAN_TRATAMIENTO', 1, 'TARJETA', 200000.00, 'COMPLETADO'),
('PLAN_TRATAMIENTO', 2, 'EFECTIVO', 120000.00, 'COMPLETADO');

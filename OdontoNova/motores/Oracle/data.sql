-- ============================================================
-- INSERCIÓN DE DATOS - ODONTONOVA (ORACLE DATABASE)
-- ============================================================

-- 1. Pacientes
INSERT INTO pacientes (tipo_documento, numero_documento, nombre, fecha_nacimiento)
VALUES ('CC', '1098765432', 'Carlos Mendoza', TO_DATE('1992-04-12', 'YYYY-MM-DD'));
INSERT INTO pacientes (tipo_documento, numero_documento, nombre, fecha_nacimiento)
VALUES ('CC', '1012345678', 'Ana María Gómez', TO_DATE('1998-08-25', 'YYYY-MM-DD'));

-- 2. Odontólogos
INSERT INTO odontologos (nombre, especialidad, telefono, email)
VALUES ('Dr. Roberto Silva', 'Ortodoncia', '3001234567', 'roberto.silva@odontonova.com');
INSERT INTO odontologos (nombre, especialidad, telefono, email)
VALUES ('Dra. Elena Rostrova', 'Endodoncia', '3009876543', 'elena.rostrova@odontonova.com');

-- 3. Sillones
INSERT INTO sillones (codigo, estado) VALUES ('SIL-01', 'DISPONIBLE');
INSERT INTO sillones (codigo, estado) VALUES ('SIL-02', 'EN_MANTENIMIENTO');

-- 4. Historias Clínicas
INSERT INTO historias_clinicas (paciente_id, antecedentes, alergias, grupo_sanguineo)
VALUES (1, 'Paciente hipertenso controlado.', 'Penicilina', 'O+');
INSERT INTO historias_clinicas (paciente_id, antecedentes, alergias, grupo_sanguineo)
VALUES (2, 'Sin antecedentes de importancia.', 'Ninguna', 'A+');

-- 5. Citas
INSERT INTO citas (paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado)
VALUES (1, 1, 1, TO_TIMESTAMP('2026-09-25 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2026-09-25 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Valoración Ortodoncia', 'CONFIRMADA');
INSERT INTO citas (paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado)
VALUES (2, 2, 1, TO_TIMESTAMP('2026-09-25 10:30:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2026-09-25 11:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'Limpieza Profunda', 'PENDIENTE');

-- 6. Planes de Tratamiento
INSERT INTO planes_tratamiento (paciente_id, nombre, descripcion)
VALUES (1, 'Ortodoncia Invisible', 'Tratamiento completo de alineación dental mediante alineadores invisibles.');
INSERT INTO planes_tratamiento (paciente_id, nombre, descripcion)
VALUES (2, 'Diseño de Sonrisa', 'Carillas estéticas e higiene oral previa.');

-- 7. Procedimientos
INSERT INTO procedimientos (nombre, descripcion)
VALUES ('Limpieza Profiláctica', 'Remoción de placa bacteriana y sarro.');
INSERT INTO procedimientos (nombre, descripcion)
VALUES ('Instalación de Brackets', 'Colocación de aparatología de ortodoncia.');

-- 8. Detalles de Tratamiento
INSERT INTO detalles_tratamiento (cabecera_id, item_id, cantidad, valor_unitario, total, observacion)
VALUES (1, 2, 1, 1500000.00, 1500000.00, 'Primera fase de ortodoncia.');
INSERT INTO detalles_tratamiento (cabecera_id, item_id, cantidad, valor_unitario, total, observacion)
VALUES (2, 1, 1, 120000.00, 120000.00, 'Limpieza inicial requerida.');

-- 9. Sesiones Clínicas
INSERT INTO sesiones_clinicas (referencia_id, fecha_inicio, fecha_fin, total, estado, observaciones)
VALUES (1, TO_TIMESTAMP('2026-09-25 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2026-09-25 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 150000.00, 'COMPLETADO', 'Sesión de valoración realizada exitosamente.');

-- 10. Pagos
INSERT INTO pagos (referencia_tipo, referencia_id, metodo, monto, estado)
VALUES ('PLAN_TRATAMIENTO', 1, 'TARJETA', 500000.00, 'COMPLETADO');
INSERT INTO pagos (referencia_tipo, referencia_id, metodo, monto, estado)
VALUES ('PLAN_TRATAMIENTO', 2, 'EFECTIVO', 120000.00, 'COMPLETADO');

COMMIT;

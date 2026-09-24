-- =====================================================================
-- DATOS DE PRUEBA - ODONTONOVA (SQL SERVER)
-- =====================================================================

-- 1. Pacientes
SET IDENTITY_INSERT pacientes ON;
INSERT INTO pacientes (id, tipo_documento, numero_documento, nombre, fecha_nacimiento, is_active, created_at, updated_at) VALUES
(1, 'CC', '1001234567', 'Carlos Perez', '1985-04-12', 1, GETDATE(), GETDATE()),
(2, 'CC', '1009876543', 'Ana Gomez', '1990-08-25', 1, GETDATE(), GETDATE()),
(3, 'CE', '3004567890', 'Michael Smith', '1978-12-03', 1, GETDATE(), GETDATE());
SET IDENTITY_INSERT pacientes OFF;

-- 2. Odontologos
SET IDENTITY_INSERT odontologos ON;
INSERT INTO odontologos (id, nombre, especialidad, telefono, email, is_active, created_at, updated_at) VALUES
(1, 'Dra. Maria Rodriguez', 'Ortodoncia', '3001112233', 'maria.rodriguez@odontonova.com', 1, GETDATE(), GETDATE()),
(2, 'Dr. Juan Torres', 'Endodoncia', '3104445566', 'juan.torres@odontonova.com', 1, GETDATE(), GETDATE());
SET IDENTITY_INSERT odontologos OFF;

-- 3. Sillones
SET IDENTITY_INSERT sillones ON;
INSERT INTO sillones (id, codigo, estado, is_active, created_at, updated_at) VALUES
(1, 'SILLON-01', 'Disponible', 1, GETDATE(), GETDATE()),
(2, 'SILLON-02', 'Ocupado', 1, GETDATE(), GETDATE());
SET IDENTITY_INSERT sillones OFF;

-- 4. Historias Clínicas
SET IDENTITY_INSERT historias_clinicas ON;
INSERT INTO historias_clinicas (id, paciente_id, antecedentes, alergias, grupo_sanguineo, is_active, created_at, updated_at) VALUES
(1, 1, 'Hipertensión controlada', 'Penicilina', 'O+', 1, GETDATE(), GETDATE()),
(2, 2, 'Ninguno', 'Ninguna', 'A+', 1, GETDATE(), GETDATE());
SET IDENTITY_INSERT historias_clinicas OFF;

-- 5. Citas
SET IDENTITY_INSERT citas ON;
INSERT INTO citas (id, paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado, created_at, updated_at) VALUES
(1, 1, 1, 1, '2026-06-01 08:00:00', '2026-06-01 09:00:00', 'Control de ortodoncia', 'Programada', GETDATE(), GETDATE()),
(2, 2, 2, 2, '2026-06-01 09:30:00', '2026-06-01 10:30:00', 'Dolor en molar superior', 'Programada', GETDATE(), GETDATE());
SET IDENTITY_INSERT citas OFF;

-- 6. Planes de Tratamiento
SET IDENTITY_INSERT planes_tratamiento ON;
INSERT INTO planes_tratamiento (id, paciente_id, nombre, descripcion, is_active, created_at, updated_at) VALUES
(1, 1, 'Ortodoncia Integral', 'Tratamiento correctivo con brackets metálicos', 1, GETDATE(), GETDATE()),
(2, 2, 'Endodoncia Molar', 'Tratamiento de conducto pieza 26', 1, GETDATE(), GETDATE());
SET IDENTITY_INSERT planes_tratamiento OFF;

-- 7. Procedimientos
SET IDENTITY_INSERT procedimientos ON;
INSERT INTO procedimientos (id, nombre, descripcion, is_active, created_at, updated_at) VALUES
(1, 'Instalación de Brackets', 'Colocación inicial de aparatología fija', 1, GETDATE(), GETDATE()),
(2, 'Tratamiento de Conducto', 'Limpieza y obturación de conductos radiculares', 1, GETDATE(), GETDATE());
SET IDENTITY_INSERT procedimientos OFF;

-- 8. Detalles de Tratamiento
SET IDENTITY_INSERT detalles_tratamiento ON;
INSERT INTO detalles_tratamiento (id, cabecera_id, item_id, cantidad, valor_unitario, total, observacion, created_at, updated_at) VALUES
(1, 1, 1, 1, 1500000.00, 1500000.00, 'Arancel inicial', GETDATE(), GETDATE()),
(2, 2, 2, 1, 450000.00, 450000.00, 'Pieza número 26', GETDATE(), GETDATE());
SET IDENTITY_INSERT detalles_tratamiento OFF;

-- 9. Sesiones Clínicas
SET IDENTITY_INSERT sesiones_clinicas ON;
INSERT INTO sesiones_clinicas (id, referencia_id, fecha_inicio, fecha_fin, total, estado, observaciones, created_at, updated_at) VALUES
(1, 1, '2026-06-01 08:00:00', '2026-06-01 09:00:00', 1500000.00, 'Completada', 'Primera cita de ortodoncia exitosa', GETDATE(), GETDATE());
SET IDENTITY_INSERT sesiones_clinicas OFF;

-- 10. Pagos
SET IDENTITY_INSERT pagos ON;
INSERT INTO pagos (id, referencia_tipo, referencia_id, metodo, monto, fecha, estado, created_at, updated_at) VALUES
(1, 'PLAN', 1, 'Tarjeta de Crédito', 1500000.00, '2026-06-01 09:15:00', 'Completado', GETDATE(), GETDATE());
SET IDENTITY_INSERT pagos OFF;

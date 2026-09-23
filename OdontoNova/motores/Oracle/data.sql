-- ==========================================
-- SCRIPT DML: DATOS DE PRUEBA EN ORACLE
-- ==========================================

-- 1. Insertar Pacientes
INSERT INTO pacientes (id, tipo_documento, numero_documento, nombre, fecha_nacimiento, is_active)
VALUES (1, 'CC', '1098765432', 'Carlos Andrés Mendoza', DATE '1992-05-14', 1);

INSERT INTO pacientes (id, tipo_documento, numero_documento, nombre, fecha_nacimiento, is_active)
VALUES (2, 'CC', '1012345678', 'María Fernanda Gómez', DATE '1998-11-20', 1);

INSERT INTO pacientes (id, tipo_documento, numero_documento, nombre, fecha_nacimiento, is_active)
VALUES (3, 'TI', '1055443322', 'Juan Esteban Ríos', DATE '2008-03-08', 1);

-- 2. Insertar Odontólogos
INSERT INTO odontologos (id, nombre, descripcion, is_active)
VALUES (1, 'Dr. Alejandro Silva', 'Especialista en Ortodoncia y Cirugía Maxilofacial', 1);

INSERT INTO odontologos (id, nombre, descripcion, is_active)
VALUES (2, 'Dra. Laura Camargo', 'Especialista en Odontopediatría y Estética Dental', 1);

-- 3. Insertar Sillones
INSERT INTO sillones (id, nombre, descripcion, is_active)
VALUES (1, 'Sillón Principal 01', 'Equipado con unidad de rayos X digital y luz LED premium', 1);

INSERT INTO sillones (id, nombre, descripcion, is_active)
VALUES (2, 'Sillón Ortodoncia 02', 'Sillón ergonómico especializado para procedimientos largos', 1);

-- 4. Insertar Citas
INSERT INTO citas (id, paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado)
VALUES (1, 1, 1, 1, TIMESTAMP '2026-09-24 09:00:00', TIMESTAMP '2026-09-24 10:00:00', 'Limpieza y valoración general', 'CONFIRMADA');

INSERT INTO citas (id, paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado)
VALUES (2, 2, 2, 2, TIMESTAMP '2026-09-24 10:30:00', TIMESTAMP '2026-09-24 11:30:00', 'Ajuste de ortodoncia mensual', 'PENDIENTE');

-- 5. Insertar Tratamientos
INSERT INTO tratamientos (id, nombre, descripcion, precio, is_active)
VALUES (1, 'Profilaxis Dental Profunda', 'Limpieza profunda con ultrasonido y pulido con pasta fluorada', 120000.00, 1);

INSERT INTO tratamientos (id, nombre, descripcion, precio, is_active)
VALUES (2, 'Ajuste de Brackets', 'Control mensual de ortodoncia y cambio de arcos', 80000.00, 1);

INSERT INTO tratamientos (id, nombre, descripcion, precio, is_active)
VALUES (3, 'Resina Fotocurada', 'Restauración estética directa con resina de alta densidad', 95000.00, 1);

-- 6. Insertar Cita Tratamiento
INSERT INTO cita_tratamiento (id, cita_id, tratamiento_id, cantidad, precio_unitario, subtotal)
VALUES (1, 1, 1, 1, 120000.00, 120000.00);

INSERT INTO cita_tratamiento (id, cita_id, tratamiento_id, cantidad, precio_unitario, subtotal)
VALUES (2, 2, 2, 1, 80000.00, 80000.00);

-- 7. Insertar Historias Clínicas
INSERT INTO historias_clinicas (id, paciente_id, odontologo_id, diagnostico, tratamiento_recomendado, observaciones)
VALUES (1, 1, 1, 'Gingivitis leve en sector inferior anterior', 'Profilaxis cada 6 meses y uso de enjuague de clorhexidina', 'Paciente refiere sensibilidad ocasional');

INSERT INTO historias_clinicas (id, paciente_id, odontologo_id, diagnostico, tratamiento_recomendado, observaciones)
VALUES (2, 2, 2, 'Evolución favorable del tratamiento de ortodoncia', 'Continuar alineación con arco de níquel-titanio 0.016', 'Sin molestias reportadas');

-- 8. Insertar Pagos
INSERT INTO pagos (id, cita_id, monto, metodo_pago, estado, fecha_pago)
VALUES (1, 1, 120000.00, 'NEQUI', 'COMPLETADO', TIMESTAMP '2026-09-24 09:55:00');

INSERT INTO pagos (id, cita_id, monto, metodo_pago, estado, fecha_pago)
VALUES (2, 2, 80000.00, 'EFECTIVO', 'COMPLETADO', TIMESTAMP '2026-09-24 11:25:00');

-- 9. Insertar Usuarios
INSERT INTO usuarios (id, nombre, email, password, rol, is_active)
VALUES (1, 'Administrador Principal', 'admin@odontonova.com', '$2a$12$eImiTXuWVxfM37uY4JANjOq2S./S/V54L5K4O2.8J8h33M5X2z6J.', 'ADMINISTRADOR', 1);

INSERT INTO usuarios (id, nombre, email, password, rol, is_active)
VALUES (2, 'Recepción OdontoNova', 'recepcion@odontonova.com', '$2a$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'RECEPCIONISTA', 1);

-- 10. Insertar Insumos
INSERT INTO insumos (id, nombre, descripcion, cantidad, precio_unitario, is_active)
VALUES (1, 'Guantes de Nitrilo (Caja x100)', 'Guantes descartables tamaño M', 50, 25000.00, 1);

INSERT INTO insumos (id, nombre, descripcion, cantidad, precio_unitario, is_active)
VALUES (2, 'Resina A2 Filtek 3M', 'Jeringa de resina fotocurable de 4g', 15, 85000.00, 1);

INSERT INTO insumos (id, nombre, descripcion, cantidad, precio_unitario, is_active)
VALUES (3, 'Anestesia Lidocaína 2%', 'Caja de cárpules de anestesia x50', 10, 110000.00, 1);

-- Confirmar transacción
COMMIT;

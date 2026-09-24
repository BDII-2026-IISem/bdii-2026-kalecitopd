# Documentación y Scripts SQL - OdontoNova

Este documento contiene la estructura de inserción de datos para las 10 tablas del sistema y el compendio de las 19 consultas SQL utilizadas en PostgreSQL.

---

## 1. Inserción de Datos (10 Tablas Iniciales)

```sql
-- ==========================================
-- 1. TABLA: pacientes
-- ==========================================
INSERT INTO pacientes (tipo_documento, numero_documento, nombre, fecha_nacimiento, is_active, created_at, updated_at) VALUES
('CC', '1001234567', 'Carlos Pérez', '1995-04-12', true, NOW(), NOW()),
('CC', '1001234568', 'María Rodríguez', '1992-08-22', true, NOW(), NOW()),
('TI', '1001234569', 'Juan Gómez', '2010-03-15', true, NOW(), NOW()),
('CC', '1001234570', 'Ana Martínez', '1988-11-05', true, NOW(), NOW()),
('CC', '1001234571', 'Luis Torres', '2001-07-19', false, NOW(), NOW()),
('TI', '1001234572', 'Sofía López', '2012-01-30', true, NOW(), NOW()),
('CC', '1001234573', 'Mateo Díaz', '1996-09-25', true, NOW(), NOW()),
('CC', '1001234574', 'Lucía Fernández', '1990-12-14', false, NOW(), NOW()),
('TI', '1001234575', 'David Ramírez', '2011-06-08', true, NOW(), NOW()),
('CC', '1001234576', 'Valeria Castro', '1999-02-19', true, NOW(), NOW());

-- ==========================================
-- 2. TABLA: odontologos
-- ==========================================
INSERT INTO odontologos (nombre, descripcion, is_active, created_at, updated_at) VALUES
('Dr. Alberto Vargas', 'Especialista en Ortodoncia y Ortopedia Maxilar', true, NOW(), NOW()),
('Dra. Carmen Jiménez', 'Especialista en Endodoncia avanzada', true, NOW(), NOW()),
('Dr. Roberto Mendoza', 'Periodoncista y cirujano periodontal', true, NOW(), NOW()),
('Dra. Elena Rojas', 'Cirujana Maxilofacial', true, NOW(), NOW()),
('Dr. Gabriel Silva', 'Odontopediatra infantil', true, NOW(), NOW()),
('Dra. Patricia Acosta', 'Rehabilitación Oral y Estética', true, NOW(), NOW()),
('Dr. Fernando Navarro', 'Ortodoncista clínico', true, NOW(), NOW()),
('Dra. Daniela Moreno', 'Especialista en diseño de sonrisa', true, NOW(), NOW()),
('Dr. Héctor Blanco', 'Implantólogo oral', true, NOW(), NOW()),
('Dra. Claudia Parra', 'Especialista en endodoncia y operatoria', true, NOW(), NOW());

-- ==========================================
-- 3. TABLA: sillones
-- ==========================================
INSERT INTO sillones (nombre, descripcion, is_active, created_at, updated_at) VALUES
('Sillón 1', 'Unidad dental principal de ortodoncia - Piso 1', true, NOW(), NOW()),
('Sillón 2', 'Unidad de endodoncia y rayos X - Piso 1', true, NOW(), NOW()),
('Sillón 3', 'Unidad de periodoncia e higiene - Piso 1', true, NOW(), NOW()),
('Sillón 4', 'Unidad quirúrgica maxilofacial - Piso 2', true, NOW(), NOW()),
('Sillón 5', 'Unidad infantil adaptada - Piso 2', true, NOW(), NOW()),
('Sillón 6', 'Unidad de estética y blanqueamiento - Piso 2', true, NOW(), NOW()),
('Sillón 7', 'Unidad de revisión general - Piso 3', true, NOW(), NOW()),
('Sillón 8', 'Unidad de implantología - Piso 3', true, NOW(), NOW()),
('Sillón 9', 'Unidad de urgencias - Piso 3', true, NOW(), NOW()),
('Sillón 10', 'Unidad de post-operatorio - Piso 4', false, NOW(), NOW());

-- ==========================================
-- 4. TABLA: citas
-- ==========================================
INSERT INTO citas (paciente_id, odontologo_id, sillon_id, fecha_inicio, fecha_fin, motivo, estado, created_at, updated_at) VALUES
(1, 1, 1, '2026-03-01 08:00:00', '2026-03-01 09:00:00', 'Control de ortodoncia', 'COMPLETADA', NOW(), NOW()),
(2, 2, 2, '2026-03-02 09:30:00', '2026-03-02 10:30:00', 'Dolor en muela del juicio', 'COMPLETADA', NOW(), NOW()),
(3, 3, 3, '2026-03-05 10:00:00', '2026-03-05 11:00:00', 'Limpieza y revisión general', 'COMPLETADA', NOW(), NOW()),
(4, 4, 4, '2026-03-10 14:00:00', '2026-03-10 15:30:00', 'Evaluación para cirugía', 'PENDIENTE', NOW(), NOW()),
(5, 5, 5, '2026-03-12 11:00:00', '2026-03-12 12:00:00', 'Revision dental infantil', 'CANCELADA', NOW(), NOW()),
(6, 6, 6, '2026-03-15 16:00:00', '2026-03-15 17:00:00', 'Instalación de prótesis', 'PENDIENTE', NOW(), NOW()),
(7, 1, 1, '2026-03-18 08:30:00', '2026-03-18 09:30:00', 'Ajuste de brackets', 'COMPLETADA', NOW(), NOW()),
(8, 7, 7, '2026-03-20 10:30:00', '2026-03-20 11:30:00', 'Blanqueamiento dental', 'COMPLETADA', NOW(), NOW()),
(9, 8, 8, '2026-03-22 15:00:00', '2026-03-22 16:00:00', 'Diseño de sonrisa', 'PENDIENTE', NOW(), NOW()),
(10, 2, 2, '2026-03-25 09:00:00', '2026-03-25 10:00:00', 'Tratamiento de conducto', 'COMPLETADA', NOW(), NOW());

-- ==========================================
-- 5. TABLA: historias_clinicas
-- ==========================================
INSERT INTO historias_clinicas (paciente_id, nombre, descripcion, is_active, created_at, updated_at) VALUES
(1, 'Historia General - Carlos Pérez', 'Paciente con buena higiene general, portador de aparatología fija.', true, NOW(), NOW()),
(2, 'Historia General - María Rodríguez', 'Presenta sensibilidad dental al frío y calor moderados. Alérgica a penicilina.', true, NOW(), NOW()),
(3, 'Historia General - Juan Gómez', 'Encías sanas, sin presencia de caries activas recientes.', true, NOW(), NOW()),
(4, 'Historia General - Ana Martínez', 'Requiere valoración médica por antecedentes de sangrado.', true, NOW(), NOW()),
(5, 'Historia General - Sofía López', 'Paciente pediátrico en etapa de recambio dental.', true, NOW(), NOW()),
(6, 'Historia General - Luis Torres', 'Pérdida ósea leve en zona posterior inferior.', false, NOW(), NOW()),
(7, 'Historia General - Mateo Díaz', 'Evolución favorable en tratamiento de ortodoncia.', true, NOW(), NOW()),
(8, 'Historia General - Lucía Fernández', 'Esmalte resistente, apto para procedimientos estéticos.', false, NOW(), NOW()),
(9, 'Historia General - David Ramírez', 'Dientes apiñados levemente en arcada superior.', true, NOW(), NOW()),
(10, 'Historia General - Valeria Castro', 'Infección localizada tratada con éxito mediante conductos.', true, NOW(), NOW());

-- ==========================================
-- 6. TABLA: planes_tratamiento
-- ==========================================
INSERT INTO planes_tratamiento (paciente_id, nombre, descripcion, is_active, created_at, updated_at) VALUES
(1, 'Plan Ortodoncia Avanzada', 'Instalación y controles periódicos de frenillos metálicos', true, NOW(), NOW()),
(2, 'Plan Endodoncia Molar', 'Tratamiento de conductos y reconstrucción con corona', true, NOW(), NOW()),
(3, 'Plan Profilaxis Preventiva', 'Limpieza profunda, aplicación de flúor y educación oral', true, NOW(), NOW()),
(4, 'Plan Cirugía Maxilofacial', 'Exodoncia compleja de cordales retenidas', true, NOW(), NOW()),
(5, 'Plan Odontopediatría Integral', 'Sellantes, profilaxis y control de caries infantil', true, NOW(), NOW()),
(6, 'Plan Rehabilitación Protésica', 'Colocación de prótesis removible superior', false, NOW(), NOW()),
(7, 'Plan Estética Láser', 'Blanqueamiento dental LED y pulido estético', true, NOW(), NOW()),
(8, 'Plan Implantología Unitaria', 'Fijación de implante de titanio y corona fija', true, NOW(), NOW()),
(9, 'Plan Periodoncia y Curetaje', 'Tratamiento periodontal para control de encías', true, NOW(), NOW()),
(10, 'Plan Restaurador Estético', 'Resinas compuestas en sector anterior', true, NOW(), NOW());

-- ==========================================
-- 7. TABLA: procedimientos
-- ==========================================
INSERT INTO procedimientos (nombre, descripcion, is_active, created_at, updated_at) VALUES
('Profilaxis Dental', 'Limpieza profunda y remoción de cálculo supragingival', true, NOW(), NOW()),
('Instalación de Brackets', 'Colocación inicial de aparatología ortodóntica', true, NOW(), NOW()),
('Tratamiento de Conducto', 'Endodoncia unirradicular o mular', true, NOW(), NOW()),
('Extracción Simple', 'Exodoncia de pieza dental deteriorada', true, NOW(), NOW()),
('Blanqueamiento LED', 'Clareamiento estético con luz halógena', true, NOW(), NOW()),
('Implante Dental', 'Inserción quirúrgica de tornillo de titanio', true, NOW(), NOW()),
('Resina Fotopolimerizable', 'Obturación estética por caries', true, NOW(), NOW()),
('Sellantes de Fosas y Fisuras', 'Prevención en molares jóvenes', true, NOW(), NOW()),
('Cirugía de Cordales', 'Extracción quirúrgica de muelas de juicio', true, NOW(), NOW()),
('Curetaje Periodontal', 'Limpieza profunda bajo encía', true, NOW(), NOW());

-- ==========================================
-- 8. TABLA: sesiones_clinicas
-- ==========================================
INSERT INTO sesiones_clinicas (referencia_id, fecha_inicio, fecha_fin, total, estado, observaciones, created_at, updated_at) VALUES
(1, '2026-03-01 08:00:00', '2026-03-01 09:00:00', 150000.00, 'COMPLETADA', 'Sesión de ortodoncia sin complicaciones.', NOW(), NOW()),
(2, '2026-03-02 09:30:00', '2026-03-02 10:30:00', 200000.00, 'COMPLETADA', 'Acceso cameral completado con éxito.', NOW(), NOW()),
(3, '2026-03-05 10:00:00', '2026-03-05 11:00:00', 80000.00, 'COMPLETADA', 'Profilaxis y pulido finalizado.', NOW(), NOW()),
(4, '2026-03-10 14:00:00', '2026-03-10 15:30:00', 500000.00, 'PROGRAMADA', 'Preparación para cirugía de cordales.', NOW(), NOW()),
(5, '2026-03-12 11:00:00', '2026-03-12 12:00:00', 60000.00, 'CANCELADA', 'Paciente no asistió por viaje.', NOW(), NOW()),
(6, '2026-03-15 16:00:00', '2026-03-15 17:00:00', 350000.00, 'PROGRAMADA', 'Toma de medidas para prótesis.', NOW(), NOW()),
(7, '2026-03-18 08:30:00', '2026-03-18 09:30:00', 150000.00, 'COMPLETADA', 'Cambio de arcos completado.', NOW(), NOW()),
(8, '2026-03-20 10:30:00', '2026-03-20 11:30:00', 300000.00, 'COMPLETADA', 'Blanqueamiento con excelente resultado estético.', NOW(), NOW()),
(9, '2026-03-22 15:00:00', '2026-03-22 16:00:00', 600000.00, 'PROGRAMADA', 'Mockup inicial de diseño de sonrisa.', NOW(), NOW()),
(10, '2026-03-25 09:00:00', '2026-03-25 10:00:00', 400000.00, 'COMPLETADA', 'Obturación de conductos radiculares.', NOW(), NOW());

-- ==========================================
-- 9. TABLA: detalles_tratamiento
-- ==========================================
INSERT INTO detalles_tratamiento (cabecera_id, item_id, cantidad, valor_unitario, total, observacion, created_at, updated_at) VALUES
(1, 2, 1, 150000.00, 150000.00, 'Control mensual de ortodoncia', NOW(), NOW()),
(2, 3, 1, 200000.00, 200000.00, 'Apertura y medicación conducto', NOW(), NOW()),
(3, 1, 1, 80000.00, 80000.00, 'Profilaxis general', NOW(), NOW()),
(4, 9, 1, 500000.00, 500000.00, 'Cirugía maxilofacial programada', NOW(), NOW()),
(5, 8, 1, 60000.00, 60000.00, 'Aplicación de sellantes', NOW(), NOW()),
(6, 4, 1, 350000.00, 350000.00, 'Exodoncia simple múltiple', NOW(), NOW()),
(7, 2, 1, 150000.00, 150000.00, 'Ajuste de aparatología', NOW(), NOW()),
(8, 5, 1, 300000.00, 300000.00, 'Sesión de blanqueamiento láser', NOW(), NOW()),
(9, 7, 2, 300000.00, 600000.00, 'Resinas estéticas anteriores', NOW(), NOW()),
(10, 3, 1, 400000.00, 400000.00, 'Endodoncia molar definitiva', NOW(), NOW());

-- ==========================================
-- 10. TABLA: pagos
-- ==========================================
INSERT INTO pagos (referencia_tipo, referencia_id, metodo, monto, fecha, estado, created_at, updated_at) VALUES
('cita', 1, 'tarjeta', 150000.00, '2026-03-01 09:05:00', 'COMPLETADO', NOW(), NOW()),
('cita', 2, 'efectivo', 200000.00, '2026-03-02 10:35:00', 'COMPLETADO', NOW(), NOW()),
('cita', 3, 'transferencia', 80000.00, '2026-03-05 11:05:00', 'COMPLETADO', NOW(), NOW()),
('cita', 4, 'tarjeta', 500000.00, '2026-03-10 15:35:00', 'PENDIENTE', NOW(), NOW()),
('cita', 6, 'tarjeta', 350000.00, '2026-03-15 17:05:00', 'PENDIENTE', NOW(), NOW()),
('cita', 7, 'efectivo', 150000.00, '2026-03-18 09:35:00', 'COMPLETADO', NOW(), NOW()),
('cita', 8, 'transferencia', 300000.00, '2026-03-20 11:35:00', 'COMPLETADO', NOW(), NOW()),
('cita', 9, 'tarjeta', 600000.00, '2026-03-22 16:05:00', 'PENDIENTE', NOW(), NOW()),
('cita', 10, 'efectivo', 400000.00, '2026-03-25 10:05:00', 'COMPLETADO', NOW(), NOW()),
('cita', 1, 'transferencia', 50000.00, '2026-03-28 14:00:00', 'COMPLETADO', NOW(), NOW());



-- =======================================================
-- SCRIPT DDL OFICIAL: ODONTONOVA PARA POSTGRESQL
-- =======================================================

DROP TABLE IF EXISTS pagos CASCADE;
DROP TABLE IF EXISTS sesiones_clinicas CASCADE;
DROP TABLE IF EXISTS detalles_tratamiento CASCADE;
DROP TABLE IF EXISTS procedimientos CASCADE;
DROP TABLE IF EXISTS planes_tratamiento CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS historias_clinicas CASCADE;
DROP TABLE IF EXISTS sillones CASCADE;
DROP TABLE IF EXISTS odontologos CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;

-- 1. Tabla: Pacientes
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    tipo_documento VARCHAR(20) NOT NULL,
    numero_documento VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla: Odontólogos
CREATE TABLE odontologos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla: Sillones
CREATE TABLE sillones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla: Historias Clínicas (Paciente 1:1 HistoriaClinica)
CREATE TABLE historias_clinicas (
    id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL UNIQUE REFERENCES pacientes(id) ON DELETE CASCADE,
    nombre VARCHAR(150),
    descripcion TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla: Citas (Paciente 1:N Cita, Odontologo 1:N Cita, Sillon 1:N Cita)
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    odontologo_id INT NOT NULL REFERENCES odontologos(id) ON DELETE CASCADE,
    sillon_id INT REFERENCES sillones(id) ON DELETE SET NULL,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    motivo TEXT,
    estado VARCHAR(50) DEFAULT 'PENDIENTE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabla: Planes de Tratamiento (Paciente 1:N PlanTratamiento)
CREATE TABLE planes_tratamiento (
    id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabla: Procedimientos
CREATE TABLE procedimientos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Tabla: Detalle Tratamiento (PlanTratamiento 1:N Detalle, Procedimiento 1:N Detalle)
CREATE TABLE detalles_tratamiento (
    id SERIAL PRIMARY KEY,
    cabecera_id INT NOT NULL REFERENCES planes_tratamiento(id) ON DELETE CASCADE,
    item_id INT NOT NULL REFERENCES procedimientos(id) ON DELETE CASCADE,
    cantidad INT DEFAULT 1 NOT NULL,
    valor_unitario NUMERIC(10, 2) NOT NULL,
    total NUMERIC(10, 2) NOT NULL,
    observacion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Tabla: Sesiones Clínicas (Cita 0..1:1 SesionClinica)
CREATE TABLE sesiones_clinicas (
    id SERIAL PRIMARY KEY,
    referencia_id INT UNIQUE REFERENCES citas(id) ON DELETE CASCADE,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    total NUMERIC(10, 2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'EN_PROCESO',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Tabla: Pagos (PlanTratamiento 1:N Pago)
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    referencia_tipo VARCHAR(50) DEFAULT 'PLAN_TRATAMIENTO',
    referencia_id INT NOT NULL REFERENCES planes_tratamiento(id) ON DELETE CASCADE,
    metodo VARCHAR(50) NOT NULL,
    monto NUMERIC(10, 2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'COMPLETADO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

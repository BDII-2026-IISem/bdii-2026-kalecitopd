-- =====================================================================
-- PROYECTO: OdontoNova
-- MOTOR: Microsoft SQL Server (T-SQL)
-- DESCRIPCIÓN: Esquema DDL completo de las 10 tablas del sistema
-- =====================================================================

-- 1. Tabla: Pacientes
CREATE TABLE pacientes (
id INT IDENTITY(1,1) PRIMARY KEY,
tipo_documento VARCHAR(20) NOT NULL,
numero_documento VARCHAR(50) NOT NULL UNIQUE,
nombre VARCHAR(100) NOT NULL,
fecha_nacimiento DATE NOT NULL,
is_active BIT DEFAULT 1,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE()
);

-- 2. Tabla: Odontologos
CREATE TABLE odontologos (
id INT IDENTITY(1,1) PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
especialidad VARCHAR(100) NOT NULL,
telefono VARCHAR(20),
email VARCHAR(100) NOT NULL UNIQUE,
is_active BIT DEFAULT 1,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE()
);

-- 3. Tabla: Sillones
CREATE TABLE sillones (
id INT IDENTITY(1,1) PRIMARY KEY,
codigo VARCHAR(50) NOT NULL UNIQUE,
estado VARCHAR(50) NOT NULL,
is_active BIT DEFAULT 1,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE()
);

-- 4. Tabla: Historias Clínicas
CREATE TABLE historias_clinicas (
id INT IDENTITY(1,1) PRIMARY KEY,
paciente_id INT NOT NULL,
antecedentes TEXT,
alergias TEXT,
grupo_sanguineo VARCHAR(10),
is_active BIT DEFAULT 1,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE(),
FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- 5. Tabla: Citas
CREATE TABLE citas (
id INT IDENTITY(1,1) PRIMARY KEY,
paciente_id INT NOT NULL,
odontologo_id INT NOT NULL,
sillon_id INT NOT NULL,
fecha_inicio DATETIME2 NOT NULL,
fecha_fin DATETIME2 NOT NULL,
motivo VARCHAR(255) NOT NULL,
estado VARCHAR(50) NOT NULL,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE(),
FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
FOREIGN KEY (odontologo_id) REFERENCES odontologos(id),
FOREIGN KEY (sillon_id) REFERENCES sillones(id)
);

-- 6. Tabla: Planes de Tratamiento
CREATE TABLE planes_tratamiento (
id INT IDENTITY(1,1) PRIMARY KEY,
paciente_id INT NOT NULL,
nombre VARCHAR(150) NOT NULL,
descripcion TEXT,
is_active BIT DEFAULT 1,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE(),
FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- 7. Tabla: Procedimientos
CREATE TABLE procedimientos (
id INT IDENTITY(1,1) PRIMARY KEY,
nombre VARCHAR(150) NOT NULL,
descripcion TEXT,
is_active BIT DEFAULT 1,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE()
);

-- 8. Tabla: Detalles de Tratamiento
CREATE TABLE detalles_tratamiento (
id INT IDENTITY(1,1) PRIMARY KEY,
cabecera_id INT NOT NULL,
item_id INT NOT NULL,
cantidad INT NOT NULL,
valor_unitario DECIMAL(10,2) NOT NULL,
total DECIMAL(10,2) NOT NULL,
observacion TEXT,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE(),
FOREIGN KEY (cabecera_id) REFERENCES planes_tratamiento(id),
FOREIGN KEY (item_id) REFERENCES procedimientos(id)
);

-- 9. Tabla: Sesiones Clínicas
CREATE TABLE sesiones_clinicas (
id INT IDENTITY(1,1) PRIMARY KEY,
referencia_id INT NOT NULL,
fecha_inicio DATETIME2 NOT NULL,
fecha_fin DATETIME2 NOT NULL,
total DECIMAL(10,2) NOT NULL,
estado VARCHAR(50) NOT NULL,
observaciones TEXT,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE(),
FOREIGN KEY (referencia_id) REFERENCES citas(id)
);

-- 10. Tabla: Pagos
CREATE TABLE pagos (
id INT IDENTITY(1,1) PRIMARY KEY,
referencia_tipo VARCHAR(50) NOT NULL,
referencia_id INT NOT NULL,
metodo VARCHAR(50) NOT NULL,
monto DECIMAL(10,2) NOT NULL,
fecha DATETIME2 NOT NULL,
estado VARCHAR(50) NOT NULL,
created_at DATETIME2 DEFAULT GETDATE(),
updated_at DATETIME2 DEFAULT GETDATE()
);

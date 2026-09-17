-- -----------------------------------------------------
-- DDL Script para SQL Server - Proyecto OdontoNova
-- -----------------------------------------------------

-- 1. Tabla de Usuarios (RBAC)
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active VARCHAR(20) DEFAULT 'ACTIVE' NOT NULL,
    avatar VARCHAR(255) NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- 2. Tabla de Roles (RBAC)
CREATE TABLE roles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    is_active VARCHAR(20) DEFAULT 'ACTIVE' NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- 3. Tabla Intermedia Roles-Usuarios
CREATE TABLE role_users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    role_id INT NOT NULL,
    user_id INT NOT NULL,
    is_active VARCHAR(20) DEFAULT 'ACTIVE' NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Tabla de Pacientes (OdontoNova)
CREATE TABLE pacientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo_documento VARCHAR(20) NOT NULL,
    numero_documento VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    is_active VARCHAR(20) DEFAULT 'ACTIVE' NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- 5. Tabla de Citas (Agendamiento)
CREATE TABLE citas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    paciente_id INT NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    estado VARCHAR(30) DEFAULT 'PROGRAMADA' NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

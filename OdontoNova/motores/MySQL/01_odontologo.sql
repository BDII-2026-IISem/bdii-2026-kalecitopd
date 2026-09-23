CREATE DATABASE IF NOT EXISTS clinica_dental;
USE clinica_dental;

CREATE TABLE IF NOT EXISTS odontologo (
    id_odontologo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

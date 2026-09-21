CREATE DATABASE IF NOT EXISTS ott_mvp;
USE ott_mvp;

CREATE TABLE region (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES region(id)
);

CREATE TABLE tarjeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    vencimiento VARCHAR(7) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE contenido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    ruta_portada VARCHAR(500) NOT NULL,
    ruta_video VARCHAR(500) NOT NULL,
    duracion INT NOT NULL,
    anio INT NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contenido_region (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenido_id INT NOT NULL,
    region_id INT NOT NULL,
    FOREIGN KEY (contenido_id) REFERENCES contenido(id),
    FOREIGN KEY (region_id) REFERENCES region(id)
);

CREATE TABLE favorito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    contenido_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (contenido_id) REFERENCES contenido(id)
);

CREATE TABLE dislike (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    contenido_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (contenido_id) REFERENCES contenido(id)
);

CREATE TABLE historial_reproduccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    contenido_id INT NOT NULL,
    progreso_segundos INT NOT NULL DEFAULT 0,
    ultima_vez DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (contenido_id) REFERENCES contenido(id)
);

CREATE TABLE sesion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    token TEXT NOT NULL,
    expira_en DATETIME NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);
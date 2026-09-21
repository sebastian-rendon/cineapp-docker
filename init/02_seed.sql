USE ott_mvp;

INSERT INTO region (id, nombre, codigo) VALUES
(1,'Colombia','CO'),
(2,'Estados Unidos','US'),
(3,'México','MX'),
(4,'España','ES'),
(5,'Argentina','AR'),
(6,'Corea del Sur','KR'),
(7,'Reino Unido','GB'),
(8,'Australia','AU'),
(9,'Canadá','CA'),
(10,'Chile','CL'),
(11,'Brasil','BR'),
(12,'Guatemala','GT'),
(13,'Indonesia','ID'),
(14,'Japón','JP'),
(15,'Francia','FR'),
(16,'Bélgica','BE'),
(17,'Portugal','PT');

-- Usuario inicial (contraseña: admin123)
INSERT INTO usuario (nombre, apellido, correo, contrasena, region_id) VALUES
('Admin', 'CineApp', 'admin@cineapp.com', '$2b$12$Kf47AgmA1mPlnhRTv/3N/efAynKv11h4dCEZjnWeo8Y03wjBlqOGe', 1);

INSERT INTO contenido
(id,titulo,descripcion,categoria,ruta_portada,ruta_video,duracion,anio,creado_en)
VALUES

(1,'Interstellar','Viaje espacial para salvar la humanidad.','Ciencia Ficción','interstellar.jpg','interstellar.mp4',169,2014,NOW()),

(2,'Parasite','Familia pobre se infiltra en una familia rica.','Drama','parasite.jpg','parasite.mp4',132,2019,NOW()),

(3,'Mad Max: Fury Road','Acción en un mundo postapocalíptico.','Acción','madmax.jpg','madmax.mp4',120,2015,NOW()),

(4,'El Laberinto del Fauno','Fantasía durante la guerra española.','Terror','fauno.jpg','fauno.mp4',118,2006,NOW()),

(5,'Superbad','Comedia estudiantil.','Comedia','superbad.jpg','superbad.mp4',113,2007,NOW()),

(6,'Roma','Drama mexicano.','Drama','roma.jpg','roma.mp4',135,2018,NOW()),

(7,'The Raid','Operación policial en Indonesia.','Acción','raid.jpg','raid.mp4',101,2011,NOW()),

(8,'REC','Película de terror española.','Terror','rec.jpg','rec.mp4',78,2007,NOW()),

(9,'Relatos Salvajes','Historias de humor negro.','Comedia','relatos.jpg','relatos.mp4',122,2014,NOW()),

(10,'Train to Busan','Supervivencia durante un brote zombie.','Acción','busan.jpg','busan.mp4',118,2016,NOW()),

(11,'La Llorona','Película guatemalteca de terror.','Terror','llorona.jpg','llorona.mp4',97,2019,NOW()),

(12,'Dune','La lucha por Arrakis.','Ciencia Ficción','dune.jpg','dune.mp4',155,2021,NOW()),

(13,'Cidade de Deus','Historia criminal en Brasil.','Drama','cidade.jpg','cidade.mp4',130,2002,NOW()),

(14,'Oldboy','Historia de venganza.','Acción','oldboy.jpg','oldboy.mp4',120,2003,NOW()),

(15,'El Secreto de sus Ojos','Investigación policial argentina.','Drama','ojos.jpg','ojos.mp4',129,2009,NOW()),

(16,'Get Out','Terror psicológico.','Terror','getout.jpg','getout.mp4',104,2017,NOW()),

(17,'Intouchables','Comedia dramática francesa.','Comedia','intouchables.jpg','intouchables.mp4',112,2011,NOW()),

(18,'Akira','Anime clásico japonés.','Ciencia Ficción','akira.jpg','akira.mp4',124,1988,NOW()),

(19,'Tropa de Elite','Policía en Brasil.','Acción','tropa.jpg','tropa.mp4',115,2007,NOW()),

(20,'El Orfanato','Terror español.','Terror','orfanato.jpg','orfanato.mp4',105,2007,NOW());

INSERT INTO contenido_region (contenido_id, region_id) VALUES

-- Interstellar
(1,1),(1,2),(1,3),(1,4),

-- Parasite
(2,1),(2,3),(2,5),(2,4),(2,6),

-- Mad Max
(3,2),(3,3),(3,7),(3,8),

-- El Laberinto del Fauno
(4,1),(4,3),(4,4),(4,5),

-- Superbad
(5,2),(5,9),(5,7),(5,8),

-- Roma
(6,1),(6,3),(6,5),(6,4),(6,10),

-- The Raid
(7,13),(7,2),(7,7),(7,8),

-- REC
(8,4),(8,1),(8,3),(8,5),(8,15),

-- Relatos Salvajes
(9,5),(9,1),(9,3),(9,4),(9,10),

-- Train to Busan
(10,6),(10,2),(10,3),(10,4),

-- La Llorona
(11,12),(11,3),(11,1),(11,4),(11,5),

-- Dune
(12,2),(12,7),(12,9),(12,8),(12,3),(12,4),

-- Cidade de Deus
(13,11),(13,1),(13,5),(13,4),(13,17),

-- Oldboy
(14,6),(14,2),(14,7),(14,14),

-- El Secreto de sus Ojos
(15,5),(15,1),(15,3),(15,4),(15,10),

-- Get Out
(16,2),(16,7),(16,9),(16,8),(16,15),

-- Intouchables
(17,15),(17,4),(17,1),(17,3),(17,16),

-- Akira
(18,14),(18,2),(18,3),(18,4),(18,15),

-- Tropa de Elite
(19,11),(19,1),(19,5),(19,17),(19,4),

-- El Orfanato
(20,4),(20,1),(20,3),(20,5),(20,15);
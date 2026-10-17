# Historias de Usuario — StreamHub OTT (CineApp)

Proyecto: **STREAMHUB / CineApp**

---

## Equipo de trabajo

| Nombre | Rol principal | Correo |
|---|---|---|
| Juan Sebastián Lopez Yarce | Frontend | jlopez709@soyudemedellin.edu.co |
| Nicol Valeria Atehortua Atehortua | Documentación | natehortua970@soyudemedellin.edu.co |
| Alejandra Escobar Chavarriaga | Base de datos | aescobar618@soyudemedellin.edu.co |
| Sebastián Rendón Grisales | Backend / API | serendon312@soyudemedellin.edu.co |

---

## Historias de usuario

| ID | Historia de usuario | Criterios de aceptación | Módulo | Prioridad | Estado | Responsable |
|---|---|---|---|---|---|---|
| HU-01 | Como usuario final, quiero registrarme con mi nombre, correo, contraseña y región, para poder acceder a la plataforma con un catálogo personalizado desde mi primer ingreso | El registro se completa exitosamente y el usuario queda almacenado con la contraseña cifrada (RF-01) · No se permite un correo duplicado (RN-02) | Autenticación | Alta | Completado | Sebastián Rendón Grisales |
| HU-02 | Como usuario final, quiero iniciar sesión con mi correo y contraseña, para acceder de forma segura a mi catálogo y a mi historial | El usuario recibe un token JWT válido que le permite acceder a los endpoints protegidos (RF-02) · El token expira a las 2 horas (RN-06) | Autenticación | Alta | Completado | Sebastián Rendón Grisales |
| HU-03 | Como usuario final, quiero ver únicamente el catálogo disponible en mi región, para no encontrar contenido que no puedo reproducir | El usuario solo visualiza películas asignadas a su región (RF-05, RN-01) · Cada película muestra título, descripción, categoría, año, duración y portada (RF-06) | Catálogo por región | Alta | Completado | Juan Sebastián Lopez Yarce |
| HU-04 | Como usuario final, quiero que el sistema guarde mi progreso de reproducción y lo retome automáticamente, para continuar viendo una película exactamente donde la dejé | El progreso se guarda cada 10 s y al pausar (RF-10) · El video reanuda automáticamente en el segundo exacto registrado (RF-12) · No se duplican registros de progreso por película (RN-05) | Reproductor y seguir viendo | Alta | Completado | Sebastián Rendón Grisales |
| HU-05 | Como usuario final, quiero marcar películas como favoritas o con dislike, para recibir recomendaciones más relevantes según mis gustos | La película se agrega/elimina de favoritos de forma inmediata (RF-13) · El contenido con dislike queda excluido de las recomendaciones (RF-08, RN-04) · Un mismo contenido no puede ser favorito y dislike a la vez (RN-08) | Favoritos, dislikes y recomendaciones | Media | Completado | Nicol Valeria Atehortua Atehortua |
| HU-06 | Como usuario final, quiero buscar películas por título, género o descripción, para encontrar contenido específico sin navegar todo el catálogo | Los resultados se actualizan mientras el usuario escribe, mostrando coincidencias por título, género o descripción (RF-15) | Búsqueda | Media | Completado | Juan Sebastián Lopez Yarce |
| HU-07 | Como usuario final, quiero recibir recomendaciones personalizadas basadas en mis favoritos, para descubrir contenido relevante según mis gustos | Las películas recomendadas corresponden a las categorías que el usuario ha marcado como favoritas (RF-07) · El contenido con dislike no aparece en recomendaciones (RF-08, RN-09) | Recomendaciones | Media | Completado | Alejandra Escobar Chavarriaga |
| HU-08 | Como usuario final, quiero consultar mi perfil con mis datos registrados, para verificar mi información en la plataforma | El usuario puede visualizar su nombre, correo y región registrados en su cuenta (RF-17) | Perfil de usuario | Baja | Completado | Nicol Valeria Atehortua Atehortua |
| HU-09 | Como usuario final, quiero cerrar sesión de forma segura, para proteger mi cuenta en dispositivos compartidos | Al cerrar sesión el token es eliminado del cliente y el usuario es redirigido a la pantalla de inicio (RF-03) | Autenticación | Alta | Completado | Sebastián Rendón Grisales |
| HU-10 | Como usuario final, quiero recuperar mi contraseña mediante mi correo registrado, para recuperar el acceso a mi cuenta si la olvido | La contraseña se actualiza correctamente en la base de datos y el usuario puede iniciar sesión con la nueva contraseña (RF-04) | Autenticación | Alta | Completado | Alejandra Escobar Chavarriaga |

---

## Resumen por responsable

| Responsable | Historias asignadas | Módulos |
|---|---|---|
| Sebastián Rendón Grisales | HU-01, HU-02, HU-04, HU-09 | Autenticación, Reproductor |
| Juan Sebastián Lopez Yarce | HU-03, HU-06 | Catálogo, Búsqueda |
| Nicol Valeria Atehortua Atehortua | HU-05, HU-08 | Favoritos/Dislikes, Perfil |
| Alejandra Escobar Chavarriaga | HU-07, HU-10 | Recomendaciones, Recuperar contraseña |

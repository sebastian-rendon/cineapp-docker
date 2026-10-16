document.addEventListener("DOMContentLoaded", async () => {

    if (!isAuthenticated()) {
        window.location.replace("index.html");
        return;
    }

    const parametros = new URLSearchParams(window.location.search);
    const id = parametros.get("id");

    if (!id) {
        window.location.href = "home.html";
        return;
    }

    try {

        const respuesta = await getContenido(id);
        const pelicula = respuesta.contenido;

        document.getElementById("video-title").textContent = pelicula.titulo;
        document.getElementById("video-description").textContent = pelicula.descripcion;
        document.getElementById("detalle-categoria").textContent = pelicula.categoria;
        document.getElementById("detalle-anio").textContent = pelicula.anio;
        document.getElementById("detalle-duracion").textContent = pelicula.duracion + " min";

        const video = document.getElementById("video");

        video.poster = `${API_BASE_URL}/static/portadas/${pelicula.ruta_portada}`;
        video.src = `${API_BASE_URL}/static/peliculas/${pelicula.ruta_video}`;
        video.load();

        // -------- CARGAR PROGRESO GUARDADO --------
        try {
            const historialPayload = await apiRequest("/seguir-viendo", { method: "GET" });
            const items = historialPayload?.contenido || [];
            const item = items.find(i => i.id === parseInt(id));
            if (item && item.progreso_segundos > 0) {
                video.addEventListener("loadedmetadata", () => {
                    video.currentTime = item.progreso_segundos;
                }, { once: true });
            }
        } catch (e) {}

        // -------- GUARDAR PROGRESO CADA 10 SEGUNDOS --------

        let ultimoGuardado = 0;

        video.addEventListener("timeupdate", () => {

            const tiempo = Math.floor(video.currentTime);

            if (tiempo - ultimoGuardado >= 10) {

                ultimoGuardado = tiempo;

                apiRequest("/historial", {
                    method: "POST",
                    body: JSON.stringify({
                        contenido_id: parseInt(id),
                        progreso_segundos: tiempo
                    })
                }).catch(() => {});

            }

        });

        video.addEventListener("ended", () => {

            apiRequest("/historial", {
                method: "POST",
                body: JSON.stringify({
                    contenido_id: parseInt(id),
                    progreso_segundos: Math.floor(video.duration)
                })
            }).catch(() => {});

        });

        // -------- GUARDAR PROGRESO AL PAUSAR --------
        video.addEventListener("pause", () => {
            if (video.currentTime > 0) {
                apiRequest("/historial", {
                    method: "POST",
                    body: JSON.stringify({
                        contenido_id: parseInt(id),
                        progreso_segundos: Math.floor(video.currentTime)
                    })
                }).catch(() => {});
            }
        });

    } catch (error) {
        alert(error.message);
        window.location.href = "home.html";
    }

    // -------- FAVORITOS --------
    const btnFav = document.getElementById("btn-fav");

    if (btnFav) {
        btnFav.addEventListener("click", async () => {
            try {
                await agregarFavorito(id);
                btnFav.textContent = "Guardado";
                btnFav.classList.add("is-active");
            } catch (error) {
                alert(error.message);
            }
        });
    }

    // -------- DISLIKES --------
    const btnDislike = document.getElementById("btn-dislike");
    let tieneDislike = false;

    if (btnDislike) {
        btnDislike.addEventListener("click", async () => {
            try {
                if (!tieneDislike) {
                    await agregarDislike(id);
                    btnDislike.textContent = "Quitar dislike";
                    btnDislike.classList.add("is-active");
                    tieneDislike = true;
                } else {
                    await eliminarDislike(id);
                    btnDislike.textContent = "Dar dislike";
                    btnDislike.classList.remove("is-active");
                    tieneDislike = false;
                }
            } catch (error) {
                alert(error.message);
            }
        });
    }
});
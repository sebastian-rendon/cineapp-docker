document.addEventListener("DOMContentLoaded", async () => {
  if (!isAuthenticated()) {
    window.location.replace("index.html");
    return;
  }

  const favoritesList = document.getElementById("favorites-list");
  if (!favoritesList) return;

  function normalizeFavorites(payload) {
    const source = payload?.favoritos || payload?.items || payload?.data || payload;
    if (Array.isArray(source)) return source;
    if (Array.isArray(payload?.results)) return payload.results;
    return [];
  }

  try {
    const payload = await getFavorites();
    const favorites = normalizeFavorites(payload);

    // 1. Primero renderiza las tarjetas
    favoritesList.innerHTML = favorites.length
      ? favorites.map(item => `
        <article class="favorite-card glass-panel">
          <div class="favorite-card__poster" style="background-image:url('${API_BASE_URL}/static/portadas/${item.ruta_portada}');background-size:cover;background-position:center;"></div>
          <div class="favorite-card__content">
            <div class="favorite-card__top">
              <div>
                <p class="favorite-card__genre">${item.categoria}</p>
                <h2>${item.titulo}</h2>
              </div>
              <span class="favorite-card__year">${item.anio}</span>
            </div>
            <p class="favorite-card__description">${item.descripcion}</p>
            <div class="favorite-card__footer">
              <span>${item.duracion} min</span>
              <a class="btn-home-nav" href="reproductor.html?id=${item.id}">Ver ahora</a>
              <button class="btn-home-nav btn-home-nav--ghost eliminar-favorito" data-id="${item.id}">Quitar</button>
            </div>
          </div>
        </article>`).join("")
      : '<p class="favorites-empty">Aún no tienes películas guardadas.</p>';

    // 2. Después agrega los eventos a los botones
    document.querySelectorAll(".eliminar-favorito").forEach(boton => {
      boton.addEventListener("click", async () => {
        const id = boton.dataset.id;
        try {
          await eliminarFavorito(id);
          boton.closest(".favorite-card").remove();
        } catch (error) {
          alert(error.message);
        }
      });
    });

  } catch (error) {
    favoritesList.innerHTML = `<p class="favorites-empty">${error.message || "No se pudieron cargar tus favoritos."}</p>`;
  }
});

document.addEventListener("DOMContentLoaded", async () => {
  if (!isAuthenticated()) {
    window.location.replace("index.html");
    return;
  }

  const session = getSession();
  const userName =
    session?.nombre ||
    session?.name ||
    session?.email?.split("@")[0] ||
    "usuario";

  const heroContainer = document.getElementById("hero");
  const rowsContainer = document.getElementById("rows");
  const searchInput = document.getElementById("search");
  const userPill = document.getElementById("user-pill");

  if (userPill) {
    userPill.textContent = `Hola, ${userName}`;
  }

  let catalogItems = [];

  const CATEGORIAS = ["Acción", "Comedia", "Drama", "Terror", "Ciencia Ficción"];

  // ── Normalización ────────────────────────────────────────────────────────────

  function normalizeItem(item) {
    return {
      id: item.id,
      title: item.titulo,
      year: item.anio,
      duration: `${item.duracion} min`,
      genre: item.categoria,
      description: item.descripcion,
      poster: `${API_BASE_URL}/static/portadas/${item.ruta_portada}`,
      video: `${API_BASE_URL}/static/peliculas/${item.ruta_video}`,
      rating: "★",
      badge: "Nuevo",
    };
  }

  // ── Tarjeta estándar ─────────────────────────────────────────────────────────

  function createCard(item) {
    return `
      <article class="home-card" data-id="${item.id}">
        <a href="reproductor.html?id=${item.id}" class="home-card__link">
          <div
            class="home-card__poster"
            style="
              background-image: url('${item.poster}');
              background-size: cover;
              background-position: center;
            "
          >
            <span class="home-card__badge">${item.badge}</span>
          </div>
        </a>
        <div class="home-card__content">
          <div class="home-card__meta">
            <span>${item.genre}</span>
            <span>${item.year}</span>
          </div>
          <h3>${item.title}</h3>
          <p>${item.description}</p>
          <div class="home-card__footer">
            <span>${item.duration}</span>
            <span>★ ${item.rating}</span>
          </div>
        </div>
      </article>
    `;
  }

  // ── Seguir viendo ────────────────────────────────────────────────────────────

  function createCardSeguirViendo(item) {
    const porcentaje = item.duracion_total
      ? Math.min(
          Math.round((item.progreso_segundos / item.duracion_total) * 100),
          100
        )
      : 0;

    return `
      <article class="home-card" data-id="${item.id}">
        <a href="reproductor.html?id=${item.id}" class="home-card__link">
          <div
            class="home-card__poster"
            style="
              background-image: url('${API_BASE_URL}/static/portadas/${item.ruta_portada}');
              background-size: cover;
              background-position: center;
            "
          >
            <span class="home-card__badge">Continuar</span>
            <div style="
              position: absolute;
              bottom: 0;
              left: 0;
              width: ${porcentaje}%;
              height: 4px;
              background: #e50914;
            "></div>
          </div>
        </a>
        <div class="home-card__content">
          <h3>${item.titulo}</h3>
          <p>${item.descripcion}</p>
          <div class="home-card__footer">
            <span>${porcentaje}% visto</span>
          </div>
        </div>
      </article>
    `;
  }

  async function renderSeguirViendo() {
    try {
      const payload = await apiRequest("/seguir-viendo", { method: "GET" });
      const items = payload?.contenido || [];

      if (items.length === 0) return "";

      return `
        <section class="home-row" aria-label="Seguir viendo">
          <div class="home-row__head">
            <h2>Seguir viendo</h2>
          </div>
          <div class="home-grid">
            ${items.map(createCardSeguirViendo).join("")}
          </div>
        </section>
      `;
    } catch (error) {
      console.error("Error cargando seguir viendo:", error);
      return "";
    }
  }

  // ── Categorías ───────────────────────────────────────────────────────────────

  async function renderCategorias() {
    let seccionesHTML = "";

    for (const categoria of CATEGORIAS) {
      try {
        const payload = await getContenidoPorCategoria(categoria);
        const peliculas = (payload?.contenido || []).map(normalizeItem);

        if (peliculas.length === 0) continue;

        seccionesHTML += `
          <section class="home-row" aria-label="${categoria}">
            <div class="home-row__head">
              <h2>${categoria}</h2>
            </div>
            <div class="home-grid">
              ${peliculas.map(createCard).join("")}
            </div>
          </section>
        `;
      } catch (error) {
        console.error(`Error cargando categoría ${categoria}:`, error);
      }
    }

    return seccionesHTML;
  }

  // ── Renderizado del catálogo ─────────────────────────────────────────────────

  function renderCatalog(query = "") {
    const normalized = query.toLowerCase().trim();

    const visibleItems = catalogItems.filter((item) => {
      const hayMatch = [item.title, item.genre, item.description, item.year]
        .join(" ")
        .toLowerCase()
        .includes(normalized);
      return normalized ? hayMatch : true;
    });

    heroContainer.innerHTML = "";
    rowsContainer.innerHTML = "";

    if (!normalized && visibleItems.length) {
      const featured = visibleItems[0];
      heroContainer.innerHTML = `
        <div class="home-hero__panel" style="background: ${featured.accent};">
          <div>
            <p class="home-hero__eyebrow">Hoy en StreamHub</p>
            <h2>${featured.title}</h2>
            <p>${featured.description}</p>
            <div class="home-hero__actions">
              <a
                class="home-hero__button"
                href="reproductor.html?id=${featured.id}"
              >
                Reproducir
              </a>
              <button
                id="hero-fav"
                class="home-hero__button home-hero__button--ghost"
                type="button"
              >
                Agregar a favoritos
              </button>
            </div>
          </div>
        </div>
      `;

      const heroFav = document.getElementById("hero-fav");

      if (heroFav) {
        heroFav.addEventListener("click", async () => {
          try {
            await agregarFavorito(featured.id);
            heroFav.textContent = "Guardado";
            heroFav.disabled = true;
          } catch (error) {
            alert(error.message);
          }
        });
      }
    }

    if (normalized && !visibleItems.length) {
      rowsContainer.innerHTML =
        '<p class="home-empty">No encontramos resultados para esa búsqueda.</p>';
      return;
    }

    rowsContainer.innerHTML = `
      <section class="home-row" aria-label="Contenido recomendado">
        <div class="home-row__head">
          <h2>Recomendado para ti</h2>
          <a href="favoritos.html">Ver todos</a>
        </div>
        <div class="home-grid">
          ${visibleItems.map(createCard).join("")}
        </div>
      </section>
      <div id="seguir-viendo-container"></div>
      <div id="categorias-container"></div>
    `;

    if (!normalized) {
      renderSeguirViendo().then((html) => {
        const container = document.getElementById("seguir-viendo-container");
        if (container) container.innerHTML = html;
      });

      renderCategorias().then((html) => {
        const container = document.getElementById("categorias-container");
        if (container) container.innerHTML = html;
      });
    }
  }

  // ── Búsqueda ─────────────────────────────────────────────────────────────────

  if (searchInput) {
    searchInput.addEventListener("input", async (event) => {
      const texto = event.target.value.trim();

      if (texto === "") {
        renderCatalog();
        return;
      }

      try {
        const respuesta = await buscarContenido(texto);
        catalogItems = (respuesta.resultados || []).map(normalizeItem);
        renderCatalog(texto);
      } catch (error) {
        console.error(error);
      }
    });
  }

  // ── Navegación ───────────────────────────────────────────────────────────────

  document.getElementById("btn-home")?.addEventListener("click", () => {
    heroContainer.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.getElementById("btn-favs")?.addEventListener("click", () => {
    window.location.href = "favoritos.html";
  });

  document.getElementById("btn-profile")?.addEventListener("click", () => {
    window.location.href = "perfil.html";
  });

  document.getElementById("btn-logout")?.addEventListener("click", async () => {
    try {
      await apiRequest("/cerrar-sesion", { method: "POST" });
    } catch (e) {}
    clearSession();
    window.location.href = "index.html";
  });

  // ── Carga inicial ────────────────────────────────────────────────────────────

  try {
    const payload = await getRecomendaciones();
    const source = payload?.recomendaciones || [];
    catalogItems = source.map(normalizeItem);
    renderCatalog();
  } catch (error) {
    rowsContainer.innerHTML = `
      <p class="home-empty">${error.message || "No se pudo cargar el catálogo."}</p>
    `;
  }
});
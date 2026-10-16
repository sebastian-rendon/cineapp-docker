document.addEventListener("DOMContentLoaded", () => {
  if (isAuthenticated()) {
    window.location.replace("home.html");
    return;
  }

  const form = document.getElementById("registerForm");
  const registerBtn = document.getElementById("registerBtn");
  const formSuccess = document.getElementById("formSuccess");

  const nombreInput = document.getElementById("nombre");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirmPassword");
  const regionSelect = document.getElementById("region");
  const termsCheckbox = document.getElementById("terms");

  const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const MIN_PASSWORD_LENGTH = 8;
  const REDIRECT_URL = "home.html";

  // ── Cargar regiones desde el backend ──────────────────────
  async function cargarRegiones() {
    try {
      const regiones = await apiRequest("/regiones", {
        method: "GET",
        auth: false
      });

      regionSelect.innerHTML = '<option value="" disabled selected>Selecciona tu región</option>';

      regiones.forEach(region => {
        const option = document.createElement("option");
        option.value = region.id;
        option.textContent = region.nombre;
        regionSelect.appendChild(option);
      });
    } catch (error) {
      console.error("No se pudieron cargar las regiones:", error);
    }
  }

  cargarRegiones();
  // ──────────────────────────────────────────────────────────

  document.querySelectorAll(".toggle-password").forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", () => {
      const targetId = toggleBtn.getAttribute("data-target");
      const targetInput = document.getElementById(targetId);
      if (!targetInput) return;

      const isHidden = targetInput.type === "password";
      targetInput.type = isHidden ? "text" : "password";
      toggleBtn.setAttribute("aria-pressed", String(isHidden));
      toggleBtn.setAttribute("aria-label", isHidden ? "Ocultar contraseña" : "Mostrar contraseña");
    });
  });

  function setError(fieldName, message) {
    const group = form.querySelector(`[data-field="${fieldName}"]`);
    const errorEl = document.getElementById(`${fieldName}Error`);
    if (!group || !errorEl) return;
    group.classList.add("has-error");
    errorEl.textContent = message;
  }

  function clearError(fieldName) {
    const group = form.querySelector(`[data-field="${fieldName}"]`);
    const errorEl = document.getElementById(`${fieldName}Error`);
    if (!group || !errorEl) return;
    group.classList.remove("has-error");
    errorEl.textContent = "";
  }

  function validateNombre() {
    const value = nombreInput.value.trim();
    if (value === "") { setError("nombre", "Ingresa tu nombre completo."); return false; }
    if (value.length < 3) { setError("nombre", "El nombre debe tener al menos 3 caracteres."); return false; }
    clearError("nombre");
    return true;
  }

  function validateEmail() {
    const value = emailInput.value.trim();
    if (value === "") { setError("email", "Ingresa tu correo electrónico."); return false; }
    if (!EMAIL_REGEX.test(value)) { setError("email", "Ingresa un correo electrónico válido."); return false; }
    clearError("email");
    return true;
  }

  function validatePassword() {
    const value = passwordInput.value;
    if (value === "") { setError("password", "Ingresa una contraseña."); return false; }
    if (value.length < MIN_PASSWORD_LENGTH) { setError("password", `La contraseña debe tener al menos ${MIN_PASSWORD_LENGTH} caracteres.`); return false; }
    clearError("password");
    return true;
  }

  function validateConfirmPassword() {
    const value = confirmPasswordInput.value;
    if (value === "") { setError("confirmPassword", "Confirma tu contraseña."); return false; }
    if (value !== passwordInput.value) { setError("confirmPassword", "Las contraseñas no coinciden."); return false; }
    clearError("confirmPassword");
    return true;
  }

  function validateRegion() {
    if (regionSelect.value === "") { setError("region", "Selecciona tu región."); return false; }
    clearError("region");
    return true;
  }

  function validateTerms() {
    if (!termsCheckbox.checked) { setError("terms", "Debes aceptar los términos y condiciones."); return false; }
    clearError("terms");
    return true;
  }

  nombreInput.addEventListener("input", () => { if (nombreInput.value.trim() !== "") clearError("nombre"); });
  emailInput.addEventListener("input", () => { if (emailInput.value.trim() !== "") clearError("email"); });
  passwordInput.addEventListener("input", () => {
    if (passwordInput.value !== "") clearError("password");
    if (confirmPasswordInput.value !== "") validateConfirmPassword();
  });
  confirmPasswordInput.addEventListener("input", () => { if (confirmPasswordInput.value !== "") clearError("confirmPassword"); });
  regionSelect.addEventListener("change", () => clearError("region"));
  termsCheckbox.addEventListener("change", () => { if (termsCheckbox.checked) clearError("terms"); });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const validations = [
      validateNombre(),
      validateEmail(),
      validatePassword(),
      validateConfirmPassword(),
      validateRegion(),
      validateTerms()
    ];

    const isFormValid = validations.every(Boolean);

    if (!isFormValid) {
      const firstInvalidGroup = form.querySelector(".has-error");
      if (firstInvalidGroup) {
        const focusable = firstInvalidGroup.querySelector("input, select");
        if (focusable) focusable.focus();
      }
      return;
    }

    const btnLabel = registerBtn.querySelector("span");

    registerBtn.disabled = true;
    registerBtn.classList.add("is-loading");
    btnLabel.textContent = "Creando cuenta...";

    try {
      const createdUser = await registerUser({
        nombre: nombreInput.value.trim().split(" ")[0],
        apellido: nombreInput.value.trim().split(" ").slice(1).join(" ") || "N/A",
        email: emailInput.value.trim(),
        password: passwordInput.value,
        region_id: parseInt(regionSelect.value)
      });

      if (!createdUser || createdUser.success === false) {
        registerBtn.classList.remove("is-loading");
        registerBtn.disabled = false;
        btnLabel.textContent = "Crear cuenta";
        setError("email", createdUser?.mensaje || "No se pudo crear la cuenta.");
        return;
      }

      registerBtn.classList.remove("is-loading");
      registerBtn.classList.add("is-success");
      btnLabel.textContent = "¡Cuenta creada!";
      formSuccess.classList.add("is-visible");

      setTimeout(() => {
        window.location.href = REDIRECT_URL;
      }, 1000);

    } catch (error) {
      registerBtn.classList.remove("is-loading");
      registerBtn.disabled = false;
      btnLabel.textContent = "Crear cuenta";
      setError("email", error.message || "No se pudo crear la cuenta.");
    }
  });
});
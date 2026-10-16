document.addEventListener("DOMContentLoaded", async () => {
  if (!isAuthenticated()) {
    window.location.replace("index.html");
    return;
  }

  const session = getSession();

  const profileName = document.getElementById("profile-name");
  const profileEmail = document.getElementById("profile-email");
  const profileNameDetail = document.getElementById("profile-name-detail");
  const profileEmailDetail = document.getElementById("profile-email-detail");
  const profilePlan = document.getElementById("profile-plan");
  const profileRegion = document.getElementById("profile-region");
  const profileWatchtime = document.getElementById("profile-watchtime");

  function renderProfile(data) {
    const nombreCompleto = `${data.nombre} ${data.apellido}`;
    if (profileName) profileName.textContent = nombreCompleto;
    if (profileEmail) profileEmail.textContent = data.correo;
    if (profileNameDetail) profileNameDetail.textContent = nombreCompleto;
    if (profileEmailDetail) profileEmailDetail.textContent = data.correo;
    if (profileRegion) profileRegion.textContent = data.region;
    if (profilePlan) profilePlan.textContent = "Plan Básico";
    if (profileWatchtime) profileWatchtime.textContent = "0 h";
  }

  try {
    const respuesta = await getProfile();
    renderProfile(respuesta.usuario);
  } catch (error) {
    console.error(error);
  }

});
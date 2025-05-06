function openAsignModal(userId) {
  fetch('/stratiview/check_sesion/', {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then((response) => {
    if (response.status === 403) {
      window.location.href = '/stratiview/auth/sign_in/'; 
    }
  })
  .catch((error) => {
    console.error('Error en keep-alive:', error);
  });

  const id = (sel) => document.getElementById(sel);
  const loading = id("loading-asign-user");
  const content = id("content-asign-user");
  const modalEl = id("modalAsignRoutes");
  const modal = new bootstrap.Modal(modalEl);
  const btnSave = id("asign-btn-save");


  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnSave.hidden = true;
  modal.show();

  // Obtener los datos de la panorama
  fetch(`/stratiview/users/get_user_routes/${userId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar");
      return response.json();
    })
    .then((data) => {
      id("asign-user-id").value = data.id;
      id("asign-user-email").value = data.email;
      id("asign-user-full_name").value = data.first_name + " " + data.last_name;

      // Marcar rutas asignadas
      document.querySelectorAll('input[name="routes"]').forEach((checkbox) => {
        checkbox.checked = data.routes.includes(parseInt(checkbox.value));
      });

      // Mostrar contenido real y ocultar spinner
      loading.style.display = "none";
      content.style.display = "flex";

      btnSave.hidden = false;
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de asignacion");
      console.error(error);
    });
}

window.openAsignModal = openAsignModal; 


document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("routeSearch");
  const checkboxes = document.querySelectorAll("#routesContainer .form-check");

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const filter = this.value.toLowerCase().trim();

      checkboxes.forEach((checkbox) => {
        const label = checkbox.querySelector("label").innerText.toLowerCase();
        const visible = label.includes(filter);
        checkbox.style.display = visible ? "block" : "none";
      });
    });
  }
});
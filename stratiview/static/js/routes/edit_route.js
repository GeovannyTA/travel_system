function openEditModal(routeId) {
  fetch("/stratiview/check_sesion/", {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (response.status === 403) {
        window.location.href = "/stratiview/auth/sign_in/";
      }
    })
    .catch((error) => {
      console.error("Error en keep-alive:", error);
    });

  const id = (sel) => document.getElementById(sel);
  const loading = id("loading-edit-route");
  const content = id("content-edit-route");
  const modalEl = id("modalEditRoute");
  const modal = new bootstrap.Modal(modalEl);
  const btnSave = id("edit-btn-save");
  const btnEnable = id("edit-btn-enable");

  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnSave.hidden = true;
  btnEnable.hidden = true;
  modal.show();

  // Obtener los datos de la panorama
  fetch(`/stratiview/routes/get_route/${routeId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar el recorrido.");
      return response.json();
    })
    .then((data) => {
      id("edit-route-id").value = data.id;
      id("edit-route-name").value = data.name;
      id("edit-route-description").value = data.description;
      id("edit-route-state").value = data.state;

      // Mostrar contenido real y ocultar spinner
      loading.style.display = "none";
      content.style.display = "flex";
      btnSave.hidden = false;

      if (data.is_deleted === true) {
        btnEnable.hidden = false;
      }
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de edición.");
      console.error(error);
    });
}

window.openEditModal = openEditModal;

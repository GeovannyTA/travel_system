function openDeleteModal(routeId) {
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
  const loading = id("loading-delete-route");
  const content = id("content-delete-route");
  const modalEl = id("modalDeleteRoute");
  const modal = new bootstrap.Modal(modalEl);
  const btnDeleteRoute = id("btn-delete-route");

  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnDeleteRoute.hidden = true;
  modal.show();

  // Obtener los datos del recorrido
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
        console.log(data);
      id("delete-route-id").value = data.id;
      id("delete-route-name").value = data.name;

      // Mostrar contenido real y ocultar spinner
      loading.style.display = "none";
      content.style.display = "flex";
      btnDeleteRoute.hidden = false;
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de edición.");
    });
}

window.openDeleteModal = openDeleteModal;

function openDeleteModal(panoramaId) {
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
  
  // Funcion flecha para obtener el elemento por su id
  const id = (sel) => document.getElementById(sel);
  const loading = id("loader");
  const content = id("modal-content");
  const modalEl = id("modalDeletePanorama");
  const modal = new bootstrap.Modal(modalEl);
  const btnDeletePanorama = id("btn-delete-panorama");

  loading.style.display = "block";
  content.style.display = "none";
  btnDeletePanorama.hidden = true;
  modal.show();

  // Obtener los datos del panorama a eliminar
  fetch(`/stratiview/panoramas/get_panorama/${panoramaId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest"
    }
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      id("delete-panorama-id").value = data.id;
      id("delete-panorama-route-name").value = data.route_name;
      id("delete-panorama-name").value = data.panorama_name;

      loading.style.display = "none";
      content.style.display = "block";
      btnDeletePanorama.hidden = false;

      modalEl.addEventListener("hidden.bs.modal", () => {
        // Limpiar el modal al cerrarlo
        id("delete-panorama-id").value = "";
        id("delete-panorama-route-name").value = "";
        id("delete-panorama-name").value = "";

        if (modalEl.contains(document.activeElement)) {
          document.activeElement.blur(); // Quitar foco del botón activo
        }

        const fallbackFocus = document.querySelector("#fallback-focus #btn-close");
      });
    })
    .catch((error) => {
      console.error(error);
    });
}

window.openDeleteModal = openDeleteModal;
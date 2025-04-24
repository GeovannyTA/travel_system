function openDeleteModal(panoramaId) {
  // Funcion flecha para obtener el elemento por su id
  const id = (sel) => document.getElementById(sel);
  const loading = id("loader");
  const content = id("modal-content");
  const modalEl = id("modalDeletePanorama");
  const modal = new bootstrap.Modal(modalEl);

  loading.style.display = "block";
  content.style.display = "none";
  modal.show();

  // Obtener los datos del panorama a eliminar
  fetch(`/panoramas/get_panorama/${panoramaId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest"
    }
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      id("panorama-id").value = data.id;
      id("panorama-state-name").value = data.state_name;
      id("panorama-name").value = data.panorama_name;

      loading.style.display = "none";
      content.style.display = "block";

      modalEl.addEventListener("hidden.bs.modal", () => {
        // Limpiar el modal al cerrarlo
        id("panorama-id").value = "";
        id("panorama-state-name").value = "";
        id("panorama-name").value = "";

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
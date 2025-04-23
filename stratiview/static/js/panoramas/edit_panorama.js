import { Viewer } from "@photo-sphere-viewer/core";
let viewer = null;

function openEditModal(panoramaId) {
  fetch(`/panoramas/get_panorama/${panoramaId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      const id = (sel) => document.getElementById(sel);
      const loading = id("loading-edit-panorama");
      const content = id("modal-content");

      // Mostrar loader y ocultar contenido
      loading.style.display = "block";
      content.style.display = "none";

      const modalEl = id("modalEditPanorama");
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
      
      id("edit-panorama-id").value = data.id;
      id("edit-panorama-state-id").value = data.state_id;
      id("edit-panorama-name").value = data.panorama_name;
      id("edit-panorama-latitude").value = data.latitude;
      id("edit-panorama-longitude").value = data.longitude;
      id("edit-panorama-direction").value = data.direction;

      // Crear visor
      viewer = new Viewer({
        container: id("panorama-preview-image"),
        panorama: data.url,
        defaultYaw: data.direction,
        mousewheel: false,
        keyboard: false,
        navbar: false,
        touchmoveTwoFingers: false,
        moveInertia: false,
        mousemove: false,
        fisheye: false,
      });

      viewer.addEventListener("ready", () => {
        setTimeout(() => viewer.zoom(0), 100);
      });

      // Input de dirección
      const directionInput = id("edit-panorama-direction");
      if (directionInput) {
        directionInput.addEventListener("input", () => {
          const yawDegrees = parseFloat(directionInput.value) || 0;
          viewer.setOption("sphereCorrection", { pan: `${yawDegrees}deg` });
        });
      }

      // Ocultar loader y mostrar contenido
      loading.style.display = "none";
      content.style.display = "flex";

      // Al cerrar modal
      modalEl.addEventListener("hidden.bs.modal", () => {
        if (viewer) viewer.destroy();
        viewer = null;
        id("panorama-preview-image").innerHTML = "";
      });
    })
    .catch((error) => {
      alert("Error al abrir el modal de edición.");
      console.error(error);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".btn-edit-panorama").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panoramaId = btn.dataset.panoramaId;
      openEditModal(panoramaId);
    });
  });
});

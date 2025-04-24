import { Viewer } from "@photo-sphere-viewer/core";
let viewer = null;

function openEditModal(panoramaId) {
  const id = (sel) => document.getElementById(sel);
  const loading = id("loading-edit-panorama");
  const content = id("content-edit-panorama");
  const modalEl = id("modalEditPanorama");
  const modal = new bootstrap.Modal(modalEl);

  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  modal.show();

  // Obtener los datos de la panorama
  fetch(`/stratiview/panoramas/get_panorama/${panoramaId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      id("edit-panorama-id").value = data.id;
      id("edit-panorama-state-id").value = data.state_id;
      id("edit-panorama-name").value = data.panorama_name;
      id("edit-panorama-latitude").value = data.latitude;
      id("edit-panorama-longitude").value = data.longitude;
      id("edit-panorama-direction").value = data.direction;
      console.log(data.direction)

      // Crear visor
      viewer = new Viewer({
        container: id("panorama-preview-image"),
        panorama: data.url,
        loadingImg: "https://beautiful-einstein.51-79-98-210.plesk.page/recorrido3602/public/assets/img/lgstratimex.webp",
        mousewheel: false,
        keyboard: false,
        navbar: false,
        touchmoveTwoFingers: false,
        moveInertia: false,
        mousemove: false,
        fisheye: false,
      });

      viewer.addEventListener("ready", () => {
        setTimeout(() => {
          viewer.zoom(0);
          const yawDegrees = parseFloat(data.direction) || 0;
          viewer.setOption("sphereCorrection", { pan: `${yawDegrees}deg` });
        }, 100);
      });

      const directionInput = id("edit-panorama-direction");
      if (directionInput) {
        directionInput.addEventListener("input", () => {
          const yawDegrees = parseFloat(directionInput.value) || 0;
          viewer.setOption("sphereCorrection", { pan: `${yawDegrees}deg` });
        });
      }

      // Mostrar contenido real y ocultar spinner
      loading.style.display = "none";
      content.style.display = "flex";

      // Destruir visor al cerrar
      modalEl.addEventListener("hidden.bs.modal", () => {
        if (viewer) viewer.destroy();
        viewer = null;
        id("panorama-preview-image").innerHTML = "";
        
        if (modalEl.contains(document.activeElement)) {
          document.activeElement.blur(); // Quitar foco del botón activo
        }

        const fallbackFocus = document.querySelector(".btn-edit-panorama");
        fallbackFocus?.focus();
      });
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de edición.");
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

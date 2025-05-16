import { Viewer } from "@photo-sphere-viewer/core";
let viewer = null;

function openEditModal(panoramaId) {
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
  const loading = id("loading-edit-panorama");
  const content = id("content-edit-panorama");
  const modalEl = id("modalEditPanorama");
  const modal = new bootstrap.Modal(modalEl);
  const btnSaveEditPanorama = id("btn-save-edit-panorama");
  const btnEnablePanorama = id("edit-btn-enable");

  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnSaveEditPanorama.hidden = true;
  btnEnablePanorama.hidden = true;
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
      id("edit-panorama-route-id").value = data.route_id;
      id("edit-panorama-name").value = data.panorama_name;
      id("edit-panorama-latitude").value = data.latitude;
      id("edit-panorama-longitude").value = data.longitude;
      id("edit-panorama-direction").value = data.direction;
      id("is-default").checked = data.is_default;

      // Crear visor
      viewer = new Viewer({
        container: id("panorama-preview-image"),
        panorama: data.url,
        loadingImg: "https://beautiful-einstein.51-79-98-210.plesk.page/static/images/lgstratiview.webp",
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
      btnSaveEditPanorama.hidden = false;

      if (data.is_deleted === true) {
        btnEnablePanorama.hidden = false;
      }
      
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
    });
}

window.openEditModal = openEditModal;
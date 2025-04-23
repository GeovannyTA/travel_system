import { Viewer } from "@photo-sphere-viewer/core";
let viewer = null;

function openEditModal(panoramaId) {
  fetch(`/panoramas/get_panorama/${panoramaId}/`)
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      document.getElementById("edit-panorama-id").value = data.id;
      document.getElementById("edit-panorama-state-id").value = data.state_id;
      document.getElementById("edit-panorama-name").value = data.panorama_name;
      document.getElementById("edit-panorama-latitude").value = data.latitude;
      document.getElementById("edit-panorama-longitude").value = data.longitude;
      document.getElementById("edit-panorama-direction").value = data.direction;

      // Cargar visor
      viewer = new Viewer({
        container: document.querySelector("#panorama-preview-image"),
        panorama: data.url,
        defaultYaw: data.direction,
        defaultZoomLvl: 50,
        mousewheel: false, 
        keyboard: false,   
        navbar: false,    
        touchmoveTwoFingers: false, 
        useXmpData: false, 
        moveInertia: false,
        mousemove: false,
        fisheye: false,
        draggable: false, 
      });
      
      const modal = new bootstrap.Modal(
        document.getElementById("modalEditPanorama")
      );
      modal.show();
    })
    .catch((error) => {
      alert("Hubo un error al cargar los datos de la panorámica.");
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const directionInput = document.getElementById("edit-panorama-direction");

  function aplicarDireccion() {
    const yawDegrees = parseFloat(directionInput.value) || 0;
    console.log("Aplicando dirección:", yawDegrees);

    if (viewer) {
      viewer.setOption("sphereCorrection", {
        pan: `${yawDegrees}deg`,
      });
    }
  }

  directionInput.addEventListener("input", aplicarDireccion);
});


// Agregar evento para destruir el visor al cerrar el modal y limpiar el contenedor
document.getElementById("modalEditPanorama").addEventListener("hidden.bs.modal", () => {
  if (viewer) {
    viewer.destroy();
    viewer = null;
  }

  document.getElementById("panorama-preview-image").innerHTML = "";
});

window.openEditModal = openEditModal;

import { Viewer } from "@photo-sphere-viewer/core";
let viewer = null;

function openEditModal(panoramaId) {
  fetch(`/panoramas/get_panorama/${panoramaId}/`)
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      console.log(data);
      document.getElementById("edit-panorama-id").value = data.id;
      document.getElementById("edit-panorama-state-id").value = data.state_id;
      document.getElementById("edit-panorama-name").value = data.panorama_name;
      document.getElementById("edit-panorama-latitude").value = data.latitude;
      document.getElementById("edit-panorama-longitude").value = data.longitude;
      document.getElementById("edit-panorama-altitude").value = data.altitude;
      document.getElementById("edit-panorama-direction").value = data.direction;
      document.getElementById("edit-panorama-orientation").value = data.orientation;

      // Cargar visor
      const viewer = new Viewer({
        container: document.querySelector("#panorama-preview-image"),
        panorama: data.url,
      });
      
      const modal = new bootstrap.Modal(
        document.getElementById("modalEditPanorama")
      );
      modal.show();
    })
    .catch((error) => {
      console.error(error);
      alert("Hubo un error al cargar los datos de la panorámica.");
    });
}

function aplicarDireccion() {
  const yawDegrees =
    parseFloat(document.getElementById("panorama-direction").value) || 0;
  const yawRadians = (yawDegrees * Math.PI) / 180;
  if (viewer && panorama) {
    viewer.tweenControlCenter(
      new THREE.Vector3(Math.sin(yawRadians), 0, Math.cos(yawRadians)),
      500
    );
  }
}

// Agregar evento para destruir el visor al cerrar el modal y limpiar el contenedor
document.getElementById("modalEditPanorama").addEventListener("hidden.bs.modal", () => {
  if (viewer) {
    viewer.destroy();
    viewer = null;
  }

  document.getElementById("panorama-preview-image").innerHTML = "";
});

window.openEditModal = openEditModal;

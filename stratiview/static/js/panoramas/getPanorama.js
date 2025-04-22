function openEditModal(panoramaId) {
  fetch(`/panoramas/edit_panorama/${panoramaId}/`)
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      document.getElementById("panorama-id").value = data.id;
      document.getElementById("state").value = data.state_id;
      document.getElementById("name").value = data.name;
      document.getElementById("latitude").value = data.latitude;
      document.getElementById("longitude").value = data.longitude;
      document.getElementById("altitude").value = data.altitude;
      const modal = new bootstrap.Modal(
        document.getElementById("modalEditarPanorama")
      );
      modal.show();
    })
    .catch((error) => {
      console.error(error);
      alert("Hubo un error al cargar los datos de la panorámica.");
    });
}

function openDeleteModal(panoramaId) {
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
      document.getElementById("panorama-id").value = data.id;
      document.getElementById("panorama-state-name").value = data.state_name;
      document.getElementById("panorama-name").value = data.panorama_name;

      const modal = new bootstrap.Modal(
        document.getElementById("modalDeletePanorama")
      );
      modal.show();
    })
    .catch((error) => {
      console.error(error);
      alert("Hubo un error al cargar los datos de la panorámica.");
    });
}

window.openDeleteModal = openDeleteModal;
function addMarker(event) {
  event.preventDefault();

  const nodeId = document.getElementById("marker-node").value;
  const key = document.getElementById("marker-key").value;
  const account = document.getElementById("marker-account").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;

  const url = `/stratiview/markers/add_marker/?marker-node=${encodeURIComponent(
    nodeId
  )}&marker-key=${encodeURIComponent(
    key
  )}&marker-account=${encodeURIComponent(
    account
  )}&marker-yaw=${yaw}&marker-pitch=${pitch}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        if (window.currentMarkerId) {
          window.markersPlugin.updateMarker({
            id: window.currentMarkerId,
            image: window.baseUrl + "pictos/pin-blue.png",
          });
        }

        const formContainer = document.getElementById("form-predio-submit");
        if (formContainer) {
          formContainer.style.display = "none";
        }
      }
    })
    .catch((error) => {
      console.error("Error al enviar el marcador:", error);
    });
}

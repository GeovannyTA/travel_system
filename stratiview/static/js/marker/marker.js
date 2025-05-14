function addMarker(event) {
  event.preventDefault();

  const key = document.getElementById("marker-key").value;
  const account = document.getElementById("marker-account").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;

  const url = `/stratiview/markers/add_marker/?marker-key=${encodeURIComponent(
    key
  )}&marker-account=${encodeURIComponent(
    account
  )}&marker-yaw=${yaw}&marker-pitch=${pitch}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.success) {
        console.log("Marcador agregado sin recargar la página");

        console.log(window.currentMarkerId);
        if (window.currentMarkerId) {
          window.markersPlugin.updateMarker({
            id: window.currentMarkerId,
            image: window.baseUrl + "pictos/pin-blue.png",
            content: null,
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

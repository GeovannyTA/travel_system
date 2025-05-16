function addMarker(event) {
  event.preventDefault();

  const nodeId = document.getElementById("marker-node").value;
  const key = document.getElementById("marker-key").value;
  const account = document.getElementById("marker-account").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;

  const url = `/stratiview/markers/add_marker/?marker-node=${encodeURIComponent(
    nodeId
  )}&marker-key=${encodeURIComponent(key)}&marker-account=${encodeURIComponent(
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

function addRouteMarker(event) {
  event.preventDefault();

  const nodeId = document.getElementById("marker-node").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;
  const type_route = document.getElementById("marker-type-route").value;

  const url = `/stratiview/markers/add_route_marker/?marker-node=${encodeURIComponent(
    nodeId
  )}&marker-yaw=${yaw}&marker-pitch=${pitch}&marker-type=${type_route}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        if (window.currentMarker) {
          console.log("currentMarker", window.currentMarker);
          window.markersPlugin.updateMarker({
            id: window.currentMarker.id,
            image: window.baseUrl + "pictos/pin-red.png",
          });
        }

        const formContainer = document.getElementById("form-tour-submit");
        if (formContainer) {
          formContainer.style.display = "none";
        }
      }
    })
    .catch((error) => {
      console.error("Error al enviar el marcador:", error);
    });
}

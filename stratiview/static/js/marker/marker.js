function addMarker(event) {
  event.preventDefault();

  const nodeId = document.getElementById("marker-node").value;
  const key = document.getElementById("marker-key").value;
  const account = document.getElementById("marker-account").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;

  const type_current_use = document.getElementById("marker-type-current_use")?.value || "";
  const type_update_use = document.getElementById("marker-type-update_use")?.value || "";
  const type = document.getElementById("marker-type")?.value || "";
  const size = document.getElementById("marker-size")?.value || "";
  const observation = document.getElementById("marker-observation")?.value || "";

  const url = `/stratiview/markers/add_marker/?marker-node=${encodeURIComponent(nodeId)}&marker-key=${encodeURIComponent(key)}&marker-account=${encodeURIComponent(account)}&marker-yaw=${yaw}&marker-pitch=${pitch}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        if (window.currentMarker) {
          // contenido tipo tarjeta
          const contentHTML = `
            <div class="form d-flex flex-column gap-2" style="width: 260px;">
              <h4>Detalle del predio</h4>
              <p><strong>Clave:</strong> ${key || "N/D"}</p>
              <p><strong>Cuenta:</strong> ${account || "N/D"}</p>
              <p><strong>Uso actual:</strong> ${type_current_use || "N/D"}</p>
              <p><strong>Uso actualizado:</strong> ${type_update_use || "N/D"}</p>
              <p><strong>Tipo de predio:</strong> ${type || "N/D"}</p>
              <p><strong>Tamaño:</strong> ${size || "N/D"}</p>
              <p><strong>Observación:</strong> ${observation || "Sin observaciones"}</p>
            </div>
          `;

          window.markersPlugin.updateMarker({
            id: window.currentMarker.id,
            image: window.baseUrlStratiview + "icons/m-house.png",
            size: { width: 50, height: 50 },
            tooltip: key,
            content: contentHTML,
            data: {
              generated: true,
              marker_type: "predio",
              key,
              account,
              type_current_use,
              type_update_use,
              type,
              size,
              observation
            },
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
  const type = document.getElementById("marker-type").value;
  const routeId = document.getElementById("marker-route")?.value;

  const url = `/stratiview/markers/add_route_marker/?marker-node=${encodeURIComponent(
    nodeId
  )}&marker-yaw=${encodeURIComponent(
    yaw
  )}&marker-pitch=${encodeURIComponent(
    pitch
  )}&marker-type=${encodeURIComponent(
    type
  )}&marker-route=${encodeURIComponent(
    routeId
  )}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && window.currentMarker) {
        const recorridoIcons = {
          vehicle: window.baseUrlStratiview + "route-type/rt-vehicle.png",
          air: window.baseUrlStratiview + "route-type/rt-air.png",
          inside: window.baseUrlStratiview + "route-type/rt-inside.png",
          walk: window.baseUrlStratiview + "route-type/rt-walk.png",
        };

        const recorridoLabels = {
          vehicle: "Recorrido en vehículo",
          air: "Recorrido aéreo",
          inside: "Recorrido interior",
          walk: "Recorrido a pie",
        };

        const icon = recorridoIcons[type] || recorridoIcons.vehicle;
        const label = recorridoLabels[type] || "Recorrido";

        const contentHTML = `
          <div class="form d-flex flex-column gap-2">
            <h4>${label}</h4>
            <p><strong>Ruta:</strong> ${routeId || "Sin nombre"}</p>
            <button class="btn btn-primary" onclick="irAlRecorrido(${routeId})">
              <i class="fa-solid fa-route"></i> Ir al recorrido
            </button>
          </div>
        `;

        window.markersPlugin.updateMarker({
          id: window.currentMarker.id,
          image: icon,
          size: { width: 50, height: 50 },
          tooltip: label,
          content: contentHTML,
          data: {
            generated: true,
            marker_type: "recorrido",
            route_id: routeId,
            type,
          },
        });

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
function addMarker(event) {
  const propertyUseIcons = {
    comercial: baseUrlLocal + "markers/property/p-trade.png",
    industrial: baseUrlLocal + "markers/property/p-industry.png",
    equipamiento: baseUrlLocal + "markers/property/p-equipment.png",
    mixto: baseUrlLocal + "markers/property/p-mixted.png",
    residencial: baseUrlLocal + "markers/property/p-house.png",
  };

  event.preventDefault();

  const nodeId = document.getElementById("marker-node").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;

  const updated_use = document.getElementById("marker-type-current_use")?.value || "";
  const property_type = document.getElementById("marker-type")?.value || "";
  const business_name = document.getElementById("marker-name")?.value || "";
  const land_position = document.getElementById("marker-position")?.value || "";
  const size = document.getElementById("marker-size")?.value || "";
  const observation = document.getElementById("marker-observation")?.value || "";

  const url = `/stratiview/markers/add_marker/` +
    `?marker-node=${encodeURIComponent(nodeId)}` +
    `&marker-yaw=${encodeURIComponent(yaw)}` +
    `&marker-pitch=${encodeURIComponent(pitch)}` +
    `&marker-type-current_use=${encodeURIComponent(updated_use)}` +
    `&marker-type=${encodeURIComponent(property_type)}` +
    `&marker-name=${encodeURIComponent(business_name)}` +
    `&marker-position=${encodeURIComponent(land_position)}` +
    `&marker-size=${encodeURIComponent(size)}` +
    `&marker-observation=${encodeURIComponent(observation)}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && window.currentMarker) {
        const contentHTML = `
          <div class="form d-flex flex-column gap-2" style="width: 260px;">
            <h4>Detalle del predio</h4>
            <p><strong>Nombre:</strong> ${business_name || "N/D"}</p>
            <p><strong>Uso actualizado:</strong> ${updated_use || "N/D"}</p>
            <p><strong>Tipo de predio:</strong> ${property_type || "N/D"}</p>
            <p><strong>Posición:</strong> ${land_position || "N/D"}</p>
            <p><strong>Tamaño:</strong> ${size || "N/D"}</p>
            <p><strong>Observación:</strong> ${observation || "Sin observaciones"}</p>
          </div>
        `;

        const icon = propertyUseIcons[updated_use.replace(/\s+/g, "_").toLowerCase()];
        
        window.markersPlugin.updateMarker({
          id: window.currentMarker.id,
          image: icon,
          size: { width: 50, height: 50 },
          tooltip: business_name,
          content: contentHTML,
          data: {
            generated: true,
            marker_type: "predio",
            updated_use,
            property_type,
            business_name,
            land_position,
            size,
            observation,
            is_saved: true
          },
        });

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
  )}&marker-yaw=${encodeURIComponent(yaw)}&marker-pitch=${encodeURIComponent(
    pitch
  )}&marker-type=${encodeURIComponent(type)}&marker-route=${encodeURIComponent(
    routeId
  )}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && window.currentMarker) {
        const recorridoIcons = {
          vehiculo: window.baseUrlLocal + "markers/route-type/rt-vehicle.png",
          aereo: window.baseUrlLocal + "markers/route-type/rt-air.png",
          interior:
            window.baseUrlLocal + "markers/route-type/rt-inside.png",
          a_pie:
            window.baseUrlLocal + "markers/route-type/rt-walk.png",
        };

        const recorridoLabels = {
          vehiculo: "Recorrido en vehículo",
          aereo: "Recorrido aéreo",
          interior: "Recorrido interior",
          a_pie: "Recorrido a pie",
        };

        const icon = recorridoIcons[type].replace(/\s+/g, "_").toLowerCase() || recorridoIcons.vehiculo;
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
            marker_type: "tour",
            route_id: routeId,
            type,
            is_saved: true
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


function addObjectMarker(event) {
  event.preventDefault();

  const nodeId = document.getElementById("marker-node").value;
  const yaw = document.getElementById("marker-yaw").value;
  const pitch = document.getElementById("marker-pitch").value;
  const name = document.getElementById("marker-name").value;
  const description =
    document.getElementById("marker-description")?.value || "";

  const url = `/stratiview/markers/add_object_marker/?marker-node=${encodeURIComponent(
    nodeId
  )}&marker-yaw=${encodeURIComponent(yaw)}&marker-pitch=${encodeURIComponent(
    pitch
  )}&marker-name=${encodeURIComponent(
    name
  )}&marker-description=${encodeURIComponent(description)}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && window.currentMarker) {
        const contentHTML = `
            <div class="form d-flex flex-column gap-2" style="width: 260px;">
              <h4>Detalle del objeto</h4>
              <p><strong>Nombre:</strong> ${name || "N/D"}</p>
              <p><strong>Observación:</strong> ${
                description || "Sin descripcción"
              }</p>
            </div>
          `;
        
        window.markersPlugin.updateMarker({
          id: window.currentMarker.id,
          image: window.baseUrlLocal + "markers/markers_type/m-object.png",
          size: { width: 50, height: 50 },
          tooltip: name,
          content: contentHTML,
          data: {
            generated: true,
            marker_type: "object",
            is_saved: true
          },
        });

        const formContainer = document.getElementById("form-object-submit");
        if (formContainer) {
          formContainer.style.display = "none";
        }
      }
    })
    .catch((error) => {
      console.error("Error al enviar el marcador:", error);
    });
}

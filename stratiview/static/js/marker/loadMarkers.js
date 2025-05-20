export function loadPredioMarkers(nodeId, markersPlugin, baseUrlLocal) {
  const propertyUseIcons = {
    comercial: baseUrlLocal + "markers/property/p-trade.png",
    industrial: baseUrlLocal + "markers/property/p-industry.png",
    equipamiento: baseUrlLocal + "markers/property/p-equipment.png",
    mixto: baseUrlLocal + "markers/property/p-mixted.png",
    residencial: baseUrlLocal + "markers/property/p-house.png",
  };


  fetch(`/stratiview/markers/get_markers/?marker-node=${nodeId}`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (Array.isArray(data)) {
        data.forEach((marker) => {
          const icon = propertyUseIcons[marker.updated_use.replace(/\s+/g, "_").toLowerCase()];

          markersPlugin.addMarker({
            id: marker.id.toString(),
            image: icon,
            position: {
              yaw: parseFloat(marker.yaw),
              pitch: parseFloat(marker.pitch),
            },
            size: { width: 45, height: 45 },
            anchor: "bottom center",
            tooltip: marker.key,
            content: `
              <div class="form d-flex flex-column gap-2" style="width: 260px;">
                <h4>Detalle del predio</h4>
                <p><strong>Negocio:</strong> ${marker.business_name || "N/D"}</p>
                <p><strong>Tipo de predio:</strong> ${
                  marker.property_type || "N/D"
                }</p>
                <p><strong>Tamaño:</strong> ${
                  marker.size?.[0]
                  ? marker.size[0].toUpperCase() + marker.size.slice(1)
                  : "N/D"
                }</p>
                <p><strong>Posición del predio:</strong> ${
                  marker.land_position?.[0]
                  ? marker.land_position[0].toUpperCase() + marker.land_position.slice(1)
                  : "N/D"
                }</p>
                <p><strong>Observación:</strong> ${
                  marker.updated_use?.[0]
                  ? marker.updated_use[0].toUpperCase() + marker.updated_use.slice(1)
                  : "N/D"
                }</p>
              </div>
            `,
            data: { ...marker },
          });
        });
      }
    })
    .catch((error) => {
      console.error("Error al obtener marcadores:", error);
    });
}

export function loadRouteMarkers(nodeId, markersPlugin, baseUrlLocal) {
  const recorridoIcons = {
    vehiculo: baseUrlLocal + "markers/route-type/rt-vehicle.png",
    aereo: baseUrlLocal + "markers/route-type/rt-air.png",
    interior: baseUrlLocal + "markers/route-type/rt-inside.png",
    a_pie: baseUrlLocal + "markers/route-type/rt-walk.png",
  };

  fetch(`/stratiview/markers/get_route_markers/?marker-node=${nodeId}`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      if (Array.isArray(data)) {
        data.forEach((marker) => {
          const icon = recorridoIcons[marker.type.replace(/\s+/g, "_").toLowerCase()];
          markersPlugin.addMarker({
            id: `route-${marker.id.toString()}`,
            image: icon,
            position: {
              yaw: parseFloat(marker.yaw),
              pitch: parseFloat(marker.pitch),
            },
            size: { width: 45, height: 45 },
            anchor: "bottom center",
            tooltip: marker.route_name,
            data: { ...marker },
            content: `
              <div class="form d-flex flex-column gap-2">
                <h4>Ir al recorrido</h4>
                <p><strong>Ruta:</strong> ${
                  marker.route_name || "Sin nombre"
                }</p>
                <button class="btn btn-primary" onclick="irAlRecorrido(${
                  marker.route_id
                })">
                  <i class="fa-solid fa-route"></i> Ir al recorrido
                </button>
              </div>
            `,
          });
        });
      }
    })
    .catch((error) => {
      console.error("Error al obtener marcadores:", error);
    });
}


export function loadObjectMarkers(nodeId, markersPlugin, baseUrlLocal) {
  fetch(`/stratiview/markers/get_object_markers/?marker-node=${nodeId}`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (Array.isArray(data)) {
        data.forEach((marker) => {
          markersPlugin.addMarker({
            id: marker.id.toString(),
            image: baseUrlLocal + "markers/markers_type/m-object.png",
            position: {
              yaw: parseFloat(marker.yaw),
              pitch: parseFloat(marker.pitch),
            },
            size: { width: 45, height: 45 },
            anchor: "bottom center",
            tooltip: marker.name,
            content: `
              <div class="form d-flex flex-column gap-2" style="width: 260px;">
                <h4>Detalle del objeto</h4>
                <p><strong>Name:</strong> ${marker.name || "N/D"}</p>
                <p><strong>Observación:</strong> ${
                  marker.description || "Sin descripcción"
                }</p>
              </div>
            `,
            data: { ...marker },
          });
        });
      }
    })
    .catch((error) => {
      console.error("Error al obtener marcadores:", error);
    });
}
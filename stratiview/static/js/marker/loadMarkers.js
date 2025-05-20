export function loadAllMarkers(nodeId, markersPlugin, baseUrlStratiview) {
  const endpoints = {
    predios: `/stratiview/markers/get_markers/?marker-node=${nodeId}`,
    rutas: `/stratiview/markers/get_route_markers/?marker-node=${nodeId}`,
    objetos: `/stratiview/markers/get_object_markers/?marker-node=${nodeId}`,
  };

  Promise.all(
    Object.values(endpoints).map((url) =>
      fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } }).then((res) =>
        res.json()
      )
    )
  )
    .then(([predios, rutas, objetos]) => {
      renderPredios(predios, markersPlugin, baseUrlStratiview);
      renderRutas(rutas, markersPlugin, baseUrlStratiview);
      renderObjetos(objetos, markersPlugin, baseUrlStratiview);
    })
    .catch((error) => {
      console.error("Error al obtener marcadores:", error);
    });
}


function renderPredios(data, markersPlugin, baseUrlStratiview) {
  const icons = {
    comercial: baseUrlStratiview + "markers/property/p-trade.png",
    industrial: baseUrlStratiview + "markers/property/p-industry.png",
    equipamiento: baseUrlStratiview + "markers/property/p-equipment.png",
    mixto: baseUrlStratiview + "markers/property/p-mixted.png",
    residencial: baseUrlStratiview + "markers/property/p-house.png",
  };

  data.forEach((m) => {
    const icon = icons[m.updated_use?.toLowerCase()] || icons.residencial;
    markersPlugin.addMarker({
      id: m.id.toString(),
      image: icon,
      position: { yaw: parseFloat(m.yaw), pitch: parseFloat(m.pitch) },
      size: { width: 45, height: 45 },
      anchor: "bottom center",
      tooltip: m.business_name || "Predio",
      content: `
        <div class="form d-flex flex-column gap-2" style="width: 260px;">
          <h4>Detalle del predio</h4>
          <p><strong>Negocio:</strong> ${m.business_name || "N/D"}</p>
          <p><strong>Tipo:</strong> ${m.property_type || "N/D"}</p>
          <p><strong>Tamaño:</strong> ${m.size || "N/D"}</p>
          <p><strong>Posición:</strong> ${m.land_position || "N/D"}</p>
          <p><strong>Observación:</strong> ${m.observation || "Sin observaciones"}</p>
        </div>`,
      data: { ...m },
    });
  });
}


function renderRutas(data, markersPlugin, baseUrlStratiview) {
  const icons = {
    vehiculo: baseUrlStratiview + "markers/route-type/rt-vehicle.png",
    aereo: baseUrlStratiview + "markers/route-type/rt-air.png",
    interior: baseUrlStratiview + "markers/route-type/rt-inside.png",
    a_pie: baseUrlStratiview + "markers/route-type/rt-walk.png",
  };

  data.forEach((m) => {
    const icon = icons[m.type?.replace(/\s+/g, "_").toLowerCase()] || icons.vehiculo;
    markersPlugin.addMarker({
      id: `route-${m.id}`,
      image: icon,
      position: { yaw: parseFloat(m.yaw), pitch: parseFloat(m.pitch) },
      size: { width: 45, height: 45 },
      anchor: "bottom center",
      tooltip: m.route_name,
      content: `
        <div class="form d-flex flex-column gap-2">
          <h4>Ir al recorrido</h4>
          <p><strong>Ruta:</strong> ${m.route_name || "Sin nombre"}</p>
          <button class="btn btn-primary" onclick="irAlRecorrido(${m.route_id})">
            <i class="fa-solid fa-route"></i> Ir al recorrido
          </button>
        </div>`,
      data: { ...m },
    });
  });
}


function renderObjetos(data, markersPlugin, baseUrlStratiview) {
  const icon = baseUrlStratiview + "markers/markers_type/m-object.png";
  data.forEach((m) => {
    markersPlugin.addMarker({
      id: m.id.toString(),
      image: icon,
      position: { yaw: parseFloat(m.yaw), pitch: parseFloat(m.pitch) },
      size: { width: 45, height: 45 },
      anchor: "bottom center",
      tooltip: m.name || "Objeto",
      content: `
        <div class="form d-flex flex-column gap-2" style="width: 260px;">
          <h4>Detalle del objeto</h4>
          <p><strong>Nombre:</strong> ${m.name || "N/D"}</p>
          <p><strong>Observación:</strong> ${m.description || "Sin descripcción"}</p>
        </div>`,
      data: { ...m },
    });
  });
}


window.irAlRecorrido = function (route_id) {
  if (!route_id) {
    alert("ID de recorrido no válido.");
    return;
  }

  const isPublic = window.location.href.includes("/public/");
  const basePath = isPublic ? "/stratiview/viewer/public/" : "/stratiview/viewer/";

  const url = `${basePath}${route_id}/`;
  window.open(url, "_blank");
};

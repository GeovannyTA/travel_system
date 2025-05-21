// eventos.js

import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { utils } from "@photo-sphere-viewer/core";
import { loadAllMarkers } from "../marker/loadMarkers.js";

export function configEvents(viewer) {
  const markersPlugin = viewer.getPlugin(MarkersPlugin);
  const tourPlugin = viewer.getPlugin(VirtualTourPlugin);

  viewer.addEventListener("ready", () => {
    const loader = document.getElementById("custom-loader");
    const instructions = document.getElementById("instructions-toggle");

    if (loader) loader.style.display = "none";
    if (instructions) instructions.style.display = "block";
  });

  new utils.Animation({
    properties: {
      pitch: { start: -Math.PI / 2, end: 0 },
      yaw: { start: Math.PI / 2, end: 0 },
      zoom: { start: 0, end: 50 },
      maxFov: { start: 180, end: 90 },
      fisheye: { start: 2, end: 0 },
    },
    duration: 3800,
    easing: "inOutQuad",
    onTick: (properties) => {
      viewer.setOptions({
        fisheye: properties.fisheye,
        maxFov: properties.maxFov,
      });
      viewer.rotate({ yaw: properties.yaw, pitch: properties.pitch });
      viewer.zoom(properties.zoom);
    },
  }).then(() => {
    viewer.setOptions({ mousemove: true, mousewheel: true });
    markersPlugin.addMarker({
      id: "marker-logo",
      type: "image",
      image: window.baseUrlStratiview + "logo-viewer.png",
      anchor: "center center",
      position: { yaw: 0, pitch: 10 },
      size: { width: 320, height: 320 },
      style: { opacity: "0.86" },
    });
  });

  tourPlugin.addEventListener("node-changed", (event) => {
    const nodeId = event.node.id;
    markersPlugin.clearMarkers();
    loadAllMarkers(nodeId, markersPlugin, window.baseUrlStratiview);

    markersPlugin.addMarker({
      id: "marker-logo",
      type: "image",
      image: window.baseUrlStratiview + "logo-viewer.png",
      anchor: "center center",
      position: { yaw: 0, pitch: 10 },
      size: { width: 320, height: 320 },
      style: { opacity: "0.86" },
    });
  });

  let ctrlPressed = false;
  window.addEventListener("keydown", (e) => (ctrlPressed = e.ctrlKey));
  window.addEventListener("keyup", (e) => (ctrlPressed = e.ctrlKey));

  viewer.addEventListener("dblclick", ({ data }) => {
    if (!window.is_admin) return;

    const id = "#" + Math.random();
    const position = { yaw: data.yaw, pitch: data.pitch };
    const size = { width: 40, height: 40 };
    const anchor = "bottom center";
    const imageProperty =
      window.baseUrlStratiview + "markers/markers_type/m-property.png";
    const imageTour =
      window.baseUrlStratiview + "markers/markers_type/m-tour.png";

    if (!data.rightclick) {
      markersPlugin.addMarker({
        id,
        position,
        image: imageProperty,
        size,
        anchor,
        tooltip: "Marcador de predio",
        data: { generated: true, marker_type: "property", is_saved: false },
        content: document.getElementById("form-predio").innerHTML,
      });
    } else if (data.rightclick) {
      markersPlugin.addMarker({
        id,
        position,
        image: imageTour,
        size,
        anchor,
        tooltip: "Marcador de recorrido",
        data: { generated: true, marker_type: "tour", is_saved: false },
        content: document.getElementById("form-tour").innerHTML,
      });
    }
  });

  viewer.addEventListener("click", ({ data }) => {
    if (!window.is_admin) return;

    if (ctrlPressed && !data.rightclick) {
      markersPlugin.addMarker({
        id: "#" + Math.random(),
        position: { yaw: data.yaw, pitch: data.pitch },
        image: window.baseUrlStratiview + "markers/markers_type/m-object.png",
        size: { width: 40, height: 40 },
        anchor: "bottom center",
        tooltip: "Marcador de objeto",
        data: { generated: true, marker_type: "object", is_saved: false },
        content: document.getElementById("form-object").innerHTML,
      });
    }
  });

  markersPlugin.addEventListener("select-marker", ({ marker, rightClick }) => {
    if (marker.data?.generated) {
      window.currentMarker = marker;
      const currentNode = tourPlugin.getCurrentNode();
      const type = marker?.data?.marker_type;

      if (type === "tour") {
        fetch("/stratiview/viewer/get_routes/", {
          headers: { "X-Requested-With": "XMLHttpRequest" },
        })
          .then((res) => res.json())
          .then((rutas) => {
            const rutaSelect = document.getElementById("marker-route");
            if (!rutaSelect) return;
            rutaSelect.innerHTML = "";
            rutas.forEach((ruta) => {
              const option = document.createElement("option");
              option.value = ruta.id;
              option.textContent = ruta.name;
              rutaSelect.appendChild(option);
            });
          })
          .catch((err) => {
            console.error("Error al cargar rutas:", err);
            const rutaSelect = document.getElementById("marker-route");
            if (rutaSelect) {
              rutaSelect.innerHTML = `<option value="">No se pudieron cargar las rutas</option>`;
            }
          });
      }

      if (currentNode) {
        setTimeout(() => {
          const nodeInput = document.getElementById("marker-node");
          const yawInput = document.getElementById("marker-yaw");
          const pitchInput = document.getElementById("marker-pitch");

          if (nodeInput && yawInput && pitchInput) {
            nodeInput.value = currentNode.id;
            yawInput.value = marker.config.position["yaw"];
            pitchInput.value = marker.config.position["pitch"];
          }
        }, 1000);
      }

      setTimeout(() => {
        const usoSelect = document.getElementById("marker-type-current_use");
        const tipoSelect = document.getElementById("marker-type");

        if (!usoSelect || !tipoSelect) return;

        const tipoPorUso = {
          Comercial: [
            "Alimentos y bebidas",
            "Abarrotes",
            "Estéticas",
            "Comercios diversos",
            "Venta de ropa",
            "Autolavado",
            "Venta de autopartes",
            "Tiendas de conveniencia",
            "Clínicas de salud",
            "Clínicas veterinaria",
            "Papelería",
            "Gasolineras",
            "Gaseras",
          ],
          Industrial: [
            "Nave de producción",
            "Nave de manufactura",
            "Bodega",
            "Plaza comercial",
          ],
          Equipamiento: [
            "Hoteles",
            "Hospitales",
            "Teatros",
            "Iglesias",
            "Escuelas",
            "Oficinas",
          ],
          Mixto: ["1 cortina", "2 cortinas", "3 o más"],
          Habitacional: ["Habitacional"],
        };

        usoSelect.addEventListener("change", () => {
          const selectedUso = usoSelect.value;
          const tipos = tipoPorUso[selectedUso] || [];

          tipos.forEach((tipo) => {
            const option = document.createElement("option");
            option.value = tipo;
            option.textContent = tipo;
            tipoSelect.appendChild(option);
          });

          tipoSelect.disabled = tipos.length === 0;
        });
      }, 1000);

      if (marker.data?.is_saved === false) {
        if (rightClick && ctrlPressed) {
          markersPlugin.removeMarker(marker);
        }
      }
    }
  });

  window.markersPlugin = markersPlugin;
  window.tourPlugin = tourPlugin;
}

function openViewerVR() {
  const currentNode = tourPlugin.getCurrentNode();
  console.log("Current node: ", currentNode.id);
  
  if (!currentNode.id) {
    alert("ID de la panorama no válido.");
    return;
  }

  const isPublic = window.location.href.includes("/public/");
  const basePath = isPublic ? "/stratiview/viewer/vr_viewer/public/" : "/stratiview/viewer/vr_viewer/";

  const url = `${basePath}${currentNode.id}/`;
  window.open(url, "_blank");
};

window.openViewerVR = openViewerVR
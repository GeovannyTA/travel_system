// eventos.js

import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { utils } from "@photo-sphere-viewer/core";
import { loadObjectMarkers, loadPredioMarkers, loadRouteMarkers } from "../marker/loadMarkers.js";

export function configEvents(viewer) {
  const markersPlugin = viewer.getPlugin(MarkersPlugin);
  const tourPlugin = viewer.getPlugin(VirtualTourPlugin);

  viewer.addEventListener("ready", () => {
    const loader = document.getElementById("custom-loader");
    if (loader) loader.style.display = "none";
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
      image: window.baseUrlLocal + "logo-viewer.png",
      anchor: "center center",
      position: { yaw: 0, pitch: 10 },
      size: { width: 320, height: 320 },
      style: { opacity: "0.86" },
    });
  });

  tourPlugin.addEventListener("node-changed", (event) => {
    const nodeId = event.node.id;
    markersPlugin.clearMarkers();
    loadPredioMarkers(nodeId, markersPlugin, window.baseUrlLocal);
    loadRouteMarkers(nodeId, markersPlugin, window.baseUrlLocal);
    loadObjectMarkers(nodeId, markersPlugin, window.baseUrlLocal);
  });

  let ctrlPressed = false;
  window.addEventListener("keydown", (e) => (ctrlPressed = e.ctrlKey));
  window.addEventListener("keyup", (e) => (ctrlPressed = e.ctrlKey));

  viewer.addEventListener("dblclick", ({ data }) => {
    const id = "#" + Math.random();
    const position = { yaw: data.yaw, pitch: data.pitch };
    const size = { width: 40, height: 40 };
    const anchor = "bottom center";
    const imageProperty = window.baseUrlLocal + "markers/markers_type/m-property.png";
    const imageTour = window.baseUrlLocal + "markers/markers_type/m-tour.png";

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
    if (ctrlPressed && !data.rightclick) {
      markersPlugin.addMarker({
        id: "#" + Math.random(),
        position: { yaw: data.yaw, pitch: data.pitch },
        image: window.baseUrlLocal + "markers/markers_type/m-object.png",
        size: { width: 40, height: 40 },
        anchor: "bottom center",
        tooltip: "Marcador de objeto",
        data: { generated: true, marker_type: "object", is_saved: false},
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

          console.log(nodeInput)
          console.log(yawInput)
          console.log(pitchInput)
          if (nodeInput && yawInput && pitchInput) {
            nodeInput.value = currentNode.id;
            yawInput.value = marker.config.position["yaw"];
            pitchInput.value = marker.config.position["pitch"];
          }
        }, 1000);
      }

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

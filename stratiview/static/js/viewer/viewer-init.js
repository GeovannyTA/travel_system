// viewer-init.js
import { Viewer, utils } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { PlanPlugin } from "@photo-sphere-viewer/plan-plugin";
import { CompassPlugin } from "@photo-sphere-viewer/compass-plugin";

import { configEvents } from "./events.js";

const container = document.getElementById("photosphere");
const route_id = container.dataset.routeId;
const baseUrl = "https://photo-sphere-viewer-data.netlify.app/assets/";
const baseUrlLocal = "http://127.0.0.1:8000/static/images/";
const baseUrlStratiview =
  "https://beautiful-einstein.51-79-98-210.plesk.page/static/images/";

fetch(`/stratiview/viewer/get_nodes/${route_id}/`, {
  headers: { "X-Requested-With": "XMLHttpRequest" },
})
  .then((response) => response.json())
  .then(({ nodes, default_node_id }) => {
    if (!nodes || nodes.length === 0) {
      alert("No se encontraron nodos para el recorrido.");
      return;
    }

    const viewer = new Viewer({
      container,
      caption: "&copy; Metro IQ",
      navbar: ["zoom", "caption", "move", "fullscreen"],
      minFov: 70,
      plugins: [
        [
          PlanPlugin,
          {
            visibleOnLoad: true,
            defaultZoom: 18,
            position: "bottom left",
            layers: [
              {
                name: "Mapa de calles",
                urlTemplate: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                attribution: "&copy; StratiView",
              },
              {
                name: "Mapa satelital",
                urlTemplate:
                  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attribution: "&copy; StratiView",
              },
            ],
          },
        ],
        [CompassPlugin],
        [
          VirtualTourPlugin,
          {
            positionMode: "gps",
            renderMode: "3d",
            startNodeId: default_node_id || nodes[0].id,
            dataMode: "client",
            preload: true,
            transitionOptions: {
              speed: "15rpm",
              effect: "fade",
              rotation: true,
              showLoader: false,
            },
            showLoader: false,
            nodes,
          },
        ],
        [MarkersPlugin],
      ],
    });

    // Exponer variables globales útiles para otros scripts
    window.viewer = viewer;
    window.baseUrl = baseUrl;
    window.baseUrlStratiview = baseUrlStratiview;
    window.baseUrlLocal = baseUrlLocal;

    configEvents(viewer);
  })
  .catch((error) => console.error("Error cargando nodos:", error));


function toggleInstructions() {
  const box = document.getElementById("instructions-box");
  if (box.style.display == "block") {
    box.style.display = "none";
  } else {
    box.style.display = "block";
  }
}


window.toggleInstructions = toggleInstructions
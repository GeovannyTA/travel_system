// viewer-init.js
import { Viewer, utils } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { PlanPlugin } from "@photo-sphere-viewer/plan-plugin";
import { CompassPlugin } from "@photo-sphere-viewer/compass-plugin";
import { StereoPlugin } from '@photo-sphere-viewer/stereo-plugin';
import { GyroscopePlugin } from '@photo-sphere-viewer/gyroscope-plugin';
import { configEvents } from "./events.js";

const container = document.getElementById("photosphere");
const route_id = container.dataset.routeId;
const node_id = container.dataset.nodeId;
const baseUrl = "https://photo-sphere-viewer-data.netlify.app/assets/";
const baseUrlStratiview =
  "https://beautiful-einstein.51-79-98-210.plesk.page/static/images/";

fetch(`/stratiview/viewer/get_nodes/${route_id}/${node_id}`, {
  headers: { "X-Requested-With": "XMLHttpRequest" },
})
  .then((response) => response.json())
  .then(({ nodes, default_node_id }) => {
    const startNodeId = (parseInt(node_id) === 0)
      ? default_node_id
      : parseInt(node_id);

    console.log("Nodo inicial", startNodeId)

    if (!nodes || nodes.length === 0) {
      alert("No se encontraron nodos para el recorrido.");
      return;
    }

    const viewer = new Viewer({
      container,
      caption: "&copy; Metro IQ",
      // navbar: ["zoom", "caption", "move", "fullscreen", { id: "stereo", title: "VR", className: "custom-vr", content: "🎮" }],
      navbar: ["zoom", "caption", "move", "fullscreen", "stereo", 
        { 
          id: "prueba", 
          title: "Prueba", 
          className: "custom-vr", 
          content: "🎮", 
          onClick: () => { 
            openViewerVR(); 
          }
        }
      ],
      minFov: 70,
      plugins: [
        [
          PlanPlugin,
          {
            visibleOnLoad: true,
            defaultZoom: 20, // ← aquí aumentas el zoom por defecto
            maxZoom: 25, 
            minZoom: 16,  
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
        [StereoPlugin],
        [GyroscopePlugin],
        [
          VirtualTourPlugin,
          {
            positionMode: "gps",
            renderMode: "3d",
            startNodeId: startNodeId,
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
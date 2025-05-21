// viewer-init.js
import { Viewer, utils } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { PlanPlugin } from "@photo-sphere-viewer/plan-plugin";
import { CompassPlugin } from "@photo-sphere-viewer/compass-plugin";
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
      navbar: ["zoom", "caption", "move", "fullscreen", 
        { 
          id: "prueba", 
          title: "Prueba", 
          className: "custom-vr", 
          content: `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-headset-vr" viewBox="0 0 16 16">
              <path d="M8 1.248c1.857 0 3.526.641 4.65 1.794a5 5 0 0 1 2.518 1.09C13.907 1.482 11.295 0 8 0 4.75 0 2.12 1.48.844 4.122a5 5 0 0 1 2.289-1.047C4.236 1.872 5.974 1.248 8 1.248"/>
              <path d="M12 12a4 4 0 0 1-2.786-1.13l-.002-.002a1.6 1.6 0 0 0-.276-.167A2.2 2.2 0 0 0 8 10.5c-.414 0-.729.103-.935.201a1.6 1.6 0 0 0-.277.167l-.002.002A4 4 0 1 1 4 4h8a4 4 0 0 1 0 8"/>
            </svg>
          `,
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
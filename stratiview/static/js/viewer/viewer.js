import { Viewer } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { PlanPlugin } from "@photo-sphere-viewer/plan-plugin";
import { TileLayer } from "leaflet";
import { CompassPlugin } from "@photo-sphere-viewer/compass-plugin";
const container = document.getElementById("photosphere");
const route_id = container.dataset.routeId;

const baseUrl = "https://photo-sphere-viewer-data.netlify.app/assets/";

fetch(`/stratiview/viewer/get_nodes/${route_id}/`, {
  headers: {
    "X-Requested-With": "XMLHttpRequest",
  },
})
  .then((response) => response.json())
  .then((nodes) => {
    if (!nodes || nodes.length === 0) {
      alert("No se encontraron nodos para el recorrido.");
      return;
    }

    const viewer = new Viewer({
      container: container,
      loadingImg: baseUrl + "loader.gif",
      caption: "&copy; Estrategas de México",
      navbar: [
        'zoom',
        'caption',
        'move',
        'fullscreen',
      ],
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
                attribution: "&copy; Estrategas de México",
              },
              {
                name: "Mapa satelital",
                urlTemplate:
                  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attribution: "&copy; Estrategas de México",
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
            startNodeId: nodes[0].id,
            dataMode: "client",
            preload: true,
            transitionOptions: {
              showLoader: false,
              speed: "15rpm",
              effect: "fade",
              rotation: true,
            },
            nodes: nodes,
          },
        ],
        [MarkersPlugin],
      ],
    });

    const markersPlugin = viewer.getPlugin(MarkersPlugin);
    const tourPlugin = viewer.getPlugin(VirtualTourPlugin);

    tourPlugin.addEventListener('node-changed', (e) => {
      markersPlugin.setMarkers([{
        id: 'marker-1',
        type: 'image',
        image: 'https://beautiful-einstein.51-79-98-210.plesk.page/static/images/logo-viewer.png',
        anchor: 'center center',
        position: { yaw: 0, pitch: 10},
        size: { width: 320, height: 320 },
        style: {
          opacity: '0.84',
        },
      }]);
    });
  })
  .catch((error) => {
    console.error("Error cargando nodos:", error);
  });

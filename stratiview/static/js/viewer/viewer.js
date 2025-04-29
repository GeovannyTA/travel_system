import { Viewer } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { PlanPlugin } from "@photo-sphere-viewer/plan-plugin";
import { TileLayer } from "leaflet";
import { CompassPlugin } from "@photo-sphere-viewer/compass-plugin";

const baseUrl = "https://photo-sphere-viewer-data.netlify.app/assets/";

fetch("/stratiview/viewer/get_nodes/", {
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
      container: document.getElementById("photosphere"),
      loadingImg: baseUrl + "loader.gif",
      // loadingImg: "/recorrido3602/public/assets/img/loader.gif",
      caption: "&copy; Estrategas de México",
      navbar: false,
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
        // [MarkersPlugin, {}],
        [
          VirtualTourPlugin,
          {
            positionMode: "gps",
            renderMode: "3d",
            startNodeId: nodes[0].id, // Usamos el primero como punto inicial
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
      ],
    });

    const planPlugin = viewer.getPlugin(PlanPlugin);

    // Espera a que el mapa esté completamente cargado
    viewer.once("ready", () => {
      const leafletMap = planPlugin.map;

      // Recorremos todos los marcadores
      leafletMap.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
          // Cambiar el ícono del marcador
          const customIcon = L.icon({
            iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
            iconSize: [32, 32],
            iconAnchor: [16, 32],
          });

          layer.setIcon(customIcon);
        }
      });
    });

    const tourPlugin = viewer.getPlugin(VirtualTourPlugin);
  })
  .catch((error) => {
    console.error("Error cargando nodos:", error);
  });

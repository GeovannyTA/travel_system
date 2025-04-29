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
            visibleOnLoad: false,
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
      ],
    });

    const tourPlugin = viewer.getPlugin(VirtualTourPlugin);
    const toggleBtn = document.getElementById("toggle-menu-btn");
    const panelMenu = document.getElementById("panel-nodos");

    toggleBtn.addEventListener("click", () => {
      panelMenu.classList.toggle("show");
    });

    // Generar panel jerárquico de navegación
    const panel = document.getElementById("panel-nodos");

    // Agrupar nodos por estado y ruta
    const estructura = {};

    nodes.forEach((nodo) => {
      const estado = nodo.state;
      const ruta = nodo.route;

      if (!estructura[estado]) estructura[estado] = {};
      if (!estructura[estado][ruta]) estructura[estado][ruta] = [];

      estructura[estado][ruta].push(nodo);
    });

    let isFirstEstado = true;
    const estadoElements = [];

    for (const estado in estructura) {
      const estadoContainer = document.createElement("div");
      estadoContainer.className = "estado-container";

      const estadoHeader = document.createElement("button");
      estadoHeader.className = "estado-header";
      estadoHeader.innerText = `⏷ ${estado}`; // por defecto desplegado

      const rutasDiv = document.createElement("div");
      rutasDiv.className = "rutas-list";

      if (!isFirstEstado) {
        rutasDiv.classList.add("hidden");
        estadoHeader.innerText = `⏵ ${estado}`;
      } else {
        estadoHeader.classList.add("active"); // color por defecto
      }

      estadoHeader.addEventListener("click", () => {
        estadoElements.forEach(({ header, rutas }) => {
          rutas.classList.add("hidden");
          header.innerText = `⏵ ${header.dataset.estado}`;
          header.classList.remove("active");
        });

        rutasDiv.classList.remove("hidden");
        estadoHeader.innerText = `⏷ ${estado}`;
        estadoHeader.classList.add("active");
      });

      for (const ruta in estructura[estado]) {
        const btn = document.createElement("button");
        btn.innerText = ruta;
        btn.className = "nodo-btn";
        btn.addEventListener("click", () => {
          const primerNodo = estructura[estado][ruta][0];
          if (primerNodo) {
            tourPlugin.setCurrentNode(primerNodo.id);
          }
        });
        rutasDiv.appendChild(btn);
      }

      estadoHeader.dataset.estado = estado;

      estadoContainer.appendChild(estadoHeader);
      estadoContainer.appendChild(rutasDiv);
      panel.appendChild(estadoContainer);

      estadoElements.push({ header: estadoHeader, rutas: rutasDiv });

      isFirstEstado = false;
    }
  })
  .catch((error) => {
    console.error("Error cargando nodos:", error);
  });

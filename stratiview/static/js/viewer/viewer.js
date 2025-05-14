import { Viewer, utils } from "@photo-sphere-viewer/core";
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
      caption: "&copy; Estrategas de México",
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
              speed: "15rpm",
              effect: "fade",
              rotation: true,
              showLoader: false,
            },
            showLoader: false,
            nodes: nodes,
          },
        ],
        [MarkersPlugin],
      ],
    });

    viewer.addEventListener("ready", () => {
      const loader = document.getElementById("custom-loader");
      if (loader) loader.style.display = "none";
    });

    const markersPlugin = viewer.getPlugin(MarkersPlugin);
    const tourPlugin = viewer.getPlugin(VirtualTourPlugin);

    window.viewer = viewer;
    window.markersPlugin = markersPlugin;
    window.baseUrl = baseUrl;
    
    viewer.setOptions({
      mousemove: false,
      mousewheel: false,
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
      viewer.setOptions({
        mousemove: true,
        mousewheel: true,
      });

      markersPlugin.setMarkers([
        {
          id: "marker-1",
          type: "image",
          image:
            "https://beautiful-einstein.51-79-98-210.plesk.page/static/images/logo-viewer.png",
          anchor: "center center",
          position: { yaw: 0, pitch: 10 },
          size: { width: 320, height: 320 },
          style: {
            opacity: "0.86",
          },
        },
      ]);
    });

    viewer.addEventListener("dblclick", ({ data }) => {
      if (!data.rightclick) {
        markersPlugin.addMarker({
          id: "#" + Math.random(),
          position: { yaw: data.yaw, pitch: data.pitch },
          image: baseUrl + "pictos/pin-red.png",
          size: { width: 32, height: 32 },
          anchor: "bottom center",
          tooltip: "Marcador de predio",
          data: {
            generated: true,
          },
          content: document.getElementById("form-predio").innerHTML,
        });
      }
    });

    let ctrlPressed = false;

    window.addEventListener("keydown", (e) => {
      if (e.ctrlKey) ctrlPressed = true;
    });
    window.addEventListener("keyup", () => {
      ctrlPressed = false;
    });

    markersPlugin.addEventListener(
      "select-marker",
      ({ marker, rightClick }) => {
        if (marker.data?.generated) {
          console.log("Marcador generado", marker);
          window.currentMarkerId = marker.id;
          // Pasar la información del marcador a los inputs
          setTimeout(() => {
            const yawInput = document.getElementById("marker-yaw");
            const pitchInput = document.getElementById("marker-pitch");

            yawInput.value = marker.config.position["yaw"];
            pitchInput.value = marker.config.position["pitch"];
          }, 1000);
          if (rightClick && ctrlPressed) {
            if (marker.definition === baseUrl + "pictos/pin-red.png") {
              markersPlugin.removeMarker(marker);
            }
          }
        }
      }
    );
  })
  .catch((error) => {
    console.error("Error cargando nodos:", error);
  });
import { Viewer, utils } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { VirtualTourPlugin } from "@photo-sphere-viewer/virtual-tour-plugin";
import { PlanPlugin } from "@photo-sphere-viewer/plan-plugin";
import { TileLayer } from "leaflet";
import { CompassPlugin } from "@photo-sphere-viewer/compass-plugin";
const container = document.getElementById("photosphere");
const route_id = container.dataset.routeId;
const baseUrl = "https://photo-sphere-viewer-data.netlify.app/assets/";
const baseUrlStratiview = "https://beautiful-einstein.51-79-98-210.plesk.page/static/images/"
// route-type/lgstratiview.webp
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
            startNodeId: nodes[0].id,
            // startNodeId: nodes[50].id,
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

    tourPlugin.addEventListener("node-changed", (event) => {
      const nodeId = event.node.id;

      // Limpia todos los marcadores anteriores
      markersPlugin.clearMarkers();

      // Llama a tu vista Django para obtener los marcadores del nodo actual
      fetch(`/stratiview/markers/get_markers/?marker-node=${nodeId}`, {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (Array.isArray(data)) {
            data.forEach((marker) => {
              markersPlugin.addMarker({
              id: marker.id.toString(),
              image: baseUrlStratiview + "stratiview_marker.png",
              position: {
                yaw: parseFloat(marker.yaw),
                pitch: parseFloat(marker.pitch),
              },
              size: { width: 40, height: 40 },
              anchor: "bottom center",
              tooltip: marker.key,
              content: `
                <div class="form d-flex flex-column gap-2" style="width: 260px;">
                  <h4>Detalle del predio</h4>
                  <p><strong>Clave:</strong> ${marker.key || "N/D"}</p>
                  <p><strong>Cuenta:</strong> ${marker.account || "N/D"}</p>
                  <p><strong>Uso actual:</strong> ${marker.type_current_use || "N/D"}</p>
                  <p><strong>Uso actualizado:</strong> ${marker.type_update_use || "N/D"}</p>
                  <p><strong>Tipo de predio:</strong> ${marker.type || "N/D"}</p>
                  <p><strong>Tamaño:</strong> ${marker.size || "N/D"}</p>
                  <p><strong>Observación:</strong> ${marker.observation || "Sin observaciones"}</p>
                </div>
              `,
              data: { ...marker },
            });
            });
          } else {
            console.warn("No se obtuvieron marcadores:", data);
          }
        })
        .catch((error) => {
          console.error("Error al obtener marcadores:", error);
        });
      
      const recorridoIcons = {
        vehicle: baseUrlStratiview + "route-type/rt-vehicle.png",
        air: baseUrlStratiview + "route-type/rt-air.png",
        inside: baseUrlStratiview + "route-type/rt-inside.png",
        walk: baseUrlStratiview + "route-type/rt-walk.png",
      };
      fetch(`/stratiview/markers/get_route_markers/?marker-node=${nodeId}`, {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (Array.isArray(data)) {
            data.forEach((marker) => {
              const icon = recorridoIcons[marker.type] || recorridoIcons.default;
              markersPlugin.addMarker({
                id: marker.id.toString(),
                image: icon,
                position: {
                  yaw: parseFloat(marker.yaw),
                  pitch: parseFloat(marker.pitch),
                },
                size: { width: 40, height: 40 },
                anchor: "bottom center",
                tooltip: marker.route_name,
                data: { ...marker },
                content: `
                  <div class="form d-flex flex-column gap-2">
                    <h4>Ir al recorrido</h4>
                    <p><strong>Ruta:</strong> ${marker.route_name || "Sin nombre"}</p>
                    <button class="btn btn-primary" onclick="irAlRecorrido(${marker.route_id})">
                      <i class="fa-solid fa-route"></i> Ir al recorrido
                    </button>
                  </div>
                `,
              });
            });
          } else {
            console.warn("No se obtuvieron marcadores:", data);
          }
        })
        .catch((error) => {
          console.error("Error al obtener marcadores:", error);
        });
    });

    window.viewer = viewer;
    window.markersPlugin = markersPlugin;
    window.baseUrl = baseUrl;
    window.baseUrlStratiview = baseUrlStratiview;
    
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

      markersPlugin.addMarker({
        id: "marker-logo",
        type: "image",
        image: baseUrlStratiview + "logo-viewer.png",
        anchor: "center center",
        position: { yaw: 0, pitch: 10 },
        size: { width: 320, height: 320 },
        style: {
          opacity: "0.86",
        },
      });

    });

    viewer.addEventListener("dblclick", ({ data }) => {
      if (!data.rightclick) {
        markersPlugin.addMarker({
          id: "#" + Math.random(),
          position: { yaw: data.yaw, pitch: data.pitch },
          image: baseUrlStratiview + "stratiView_marker.png",
          size: { width: 40, height: 40 },
          anchor: "bottom center",
          tooltip: "Marcador de predio",
          data: {
            generated: true,
            marker_type: "predio",
          },
          content: document.getElementById("form-predio").innerHTML,
        });
      } else {
        markersPlugin.addMarker({
          id: "#" + Math.random(),
          position: { yaw: data.yaw, pitch: data.pitch },
          image: baseUrlStratiview + "stratiView_marker.png",
          size: { width: 40, height: 40 },
          anchor: "bottom center",
          tooltip: "Marcador de recorrido",
          data: {
            generated: true,
            marker_type: "recorrido", 
          },
          content: document.getElementById("form-tour").innerHTML,
        });
      }
    });


    let ctrlPressed = false;

    window.addEventListener("keydown", (e) => {
      if (e.ctrlKey) ctrlPressed = true;
    });

    window.addEventListener("keyup", (e) => {
      if (!e.ctrlKey) ctrlPressed = false;
    });

    markersPlugin.addEventListener("select-marker", ({ marker, rightClick }) => {
      if (marker.data?.generated) {
        // current marker
        window.currentMarker = marker;
        const currentNode = tourPlugin.getCurrentNode();
        const type = marker?.data?.marker_type;

        if (type === "recorrido") {
          fetch("/stratiview/viewer/get_routes/", {
            headers: {
              "X-Requested-With": "XMLHttpRequest",
            },
          })
            .then((res) => res.json())
            .then((rutas) => {
              const rutaSelect = document.getElementById("marker-route");
              if (!rutaSelect) return;

              rutaSelect.innerHTML = ""; // Limpia

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

        // Solo eliminar si es clic derecho + Ctrl + Shift
        if (rightClick && ctrlPressed) {
          markersPlugin.removeMarker(marker);
        }
      }
    });
  })
  .catch((error) => {
    console.error("Error cargando nodos:", error);
  });


window.irAlRecorrido = function (routeId) {
  if (!routeId) {
    alert("Ruta no válida");
    return;
  }
  window.location.href = `/stratiview/viewer/${routeId}/`;
};
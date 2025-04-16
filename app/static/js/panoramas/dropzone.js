const dropzone = document.getElementById("dropzone");
const input = document.getElementById("images");
const preview = document.getElementById("preview");

dropzone.addEventListener("click", () => input.click());

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("bg-light");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("bg-light");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  input.files = e.dataTransfer.files;
  showPreview(input.files);
});

input.addEventListener("change", () => {
  showPreview(input.files);
});

function showPreview(files) {
  preview.innerHTML = "";
  Array.from(files).forEach((file, index) => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const col = document.createElement("div");
      col.className = "col-4 mb-3 position-relative";

      col.innerHTML = `
          <div class="position-relative">
            <button type="button" class="btn-close position-absolute top-0 end-0 m-2" aria-label="Cerrar"></button>
            <img src="${e.target.result}" class="img-fluid rounded border shadow" alt="preview">
          </div>
        `;

      // Evento para eliminar la imagen
      col.querySelector(".btn-close").addEventListener("click", () => {
        col.remove();
        // Si deseas también eliminar el archivo del input, necesitarías gestionarlo con un FileList personalizada (más complejo)
      });

      preview.appendChild(col);
    };
    reader.readAsDataURL(file);
  });
}

function cancelUpload() {
  const preview = document.getElementById("preview");
  const input = document.getElementById("images");
  preview.innerHTML = "";
  input.value = null;
}

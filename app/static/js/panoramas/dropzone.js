const dropzone = document.getElementById("dropzone");
const input = document.getElementById("images");
const preview = document.getElementById("preview");
const cancelButton = document.getElementById("btn-cancel");

dropzone.addEventListener("click", () => input.click());

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
  Array.from(files).forEach((file) => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const col = document.createElement("div");
      col.className = "col-4 mb-3";
      col.innerHTML = `
            <img src="${e.target.result}" class="img-fluid rounded border shadow" alt="preview">
          `;
      preview.appendChild(col);
    };
    reader.readAsDataURL(file);
  });
}

cancelButton.addEventListener("click", () => {
  const preview = document.getElementById("preview");
  const input = document.getElementById("images");
  preview.innerHTML = "";
  input.value = null;
});

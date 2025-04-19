const dropzone = document.getElementById("dropzone");
const input = document.getElementById("images");
const fileCount = document.getElementById("file-count");
const state = document.getElementById("state")


// Crear un objeto DataTransfer para manejar los archivos
const dataTransfer = new DataTransfer();

// Valor por defecto del File count
fileCount.textContent = "0 archivo(s) seleccionado(s)";

// Manejar clic en el área de dropzone para abrir el selector de archivos
dropzone.addEventListener("click", () => input.click());

// Cambiar estilo al arrastrar archivos sobre el dropzone
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("bg-light");
});

// Revertir estilo al salir del área de dropzone
dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("bg-light");
});

// Manejar archivos soltados en el dropzone
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("bg-light");
  const newFiles = Array.from(e.dataTransfer.files);
  addFiles(newFiles);
});

// Manejar selección de archivos mediante el input
input.addEventListener("change", () => {
  const newFiles = Array.from(input.files);
  newFiles.forEach((newFile) => {
    const isDuplicate = Array.from(dataTransfer.files).some(
      (existingFile) =>
        existingFile.name === newFile.name &&
        existingFile.size === newFile.size
    );

    if (!isDuplicate) {
      dataTransfer.items.add(newFile);
    }
  });

  input.files = dataTransfer.files;
  updateFileCount();
});

// Función para agregar archivos evitando duplicados
function addFiles(files) {
  files.forEach((newFile) => {
    const isDuplicate = Array.from(dataTransfer.files).some(
      (existingFile) =>
        existingFile.name === newFile.name &&
        existingFile.size === newFile.size &&
        existingFile.lastModified === newFile.lastModified
    );

    if (!isDuplicate) {
      dataTransfer.items.add(newFile);
    }
  });

  input.files = dataTransfer.files;
  updateFileCount();
}

function updateFileCount() {
  fileCount.textContent = `${dataTransfer.files.length} archivo(s) seleccionado(s)`;
}

function cancelUpload() {
  while (dataTransfer.items.length > 0) {
    dataTransfer.items.remove(0);
  }
  const newDataTransfer = new DataTransfer();
  input.files = newDataTransfer.files;
  dropzone.classList.remove("bg-light");
  fileCount.textContent = "0 archivo(s) seleccionado(s)";
  state.selectedIndex = 0;
}

function clearFiles() {
  while (dataTransfer.items.length > 0) {
    dataTransfer.items.remove(0);
  }
  const newDataTransfer = new DataTransfer();
  input.files = newDataTransfer.files;
  dropzone.classList.remove("bg-light");
  fileCount.textContent = "0 archivo(s) seleccionado(s)";
  state.selectedIndex = 0;
}

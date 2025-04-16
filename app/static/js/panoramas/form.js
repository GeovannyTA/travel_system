document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#modalAgregarPanorama form");
  const btnSave = document.getElementById("btn-save");
  const btnClear = document.getElementById("btn-clear");
  const btnCancel = document.getElementById("btn-cancel");
  const dropzone = document.querySelector("#dropzone");
  const btnClose = document.getElementById("btn-close");

  form.addEventListener("submit", () => {
    // Desactivar botones
    btnSave.disabled = true;
    btnClear.disabled = true;
    btnCancel.disabled = true;
    btnClose.disabled = true;
    
    // Cambiar apariencia del botón guardar
    btnSave.innerHTML = `<i class="fas fa-spinner fa-spin spinner-custom"></i> Subiendo...`;

    // Bloquear interacción con dropzone
    dropzone.classList.add("disabled");
  });
});

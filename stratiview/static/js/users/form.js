document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#modalAddUser form");
  const btnSave = document.getElementById("btn-save");
  const btnClear = document.getElementById("btn-clear");
  const btnCancel = document.getElementById("btn-cancel");
  const dropzone = document.querySelector("#dropzone");
  const btnClose = document.getElementById("btn-close");
  const areaSelect = document.getElementById("add-user-area");
  const rolSelect = document.getElementById("add-user-rol");

  // Función modular para actualizar los roles según el área seleccionada
  function updateRolOptions(areaSelect, rolSelect, areaRolesMap) {
    const selectedAreaId = areaSelect.value;
    rolSelect.innerHTML = "";

    if (areaRolesMap[selectedAreaId]) {
      areaRolesMap[selectedAreaId].forEach(function (rol) {
        const option = document.createElement("option");
        option.value = rol.id;
        option.textContent = rol.name;
        rolSelect.appendChild(option);
      });
    }
  }

  // Escuchar cuando cambie el área
  areaSelect.addEventListener("change", function () {
    updateRolOptions(areaSelect, rolSelect, areaRolesMap);
  });

  // Escuchar el submit del formulario
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

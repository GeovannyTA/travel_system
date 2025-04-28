function openEditModal(panoramaId) {
  const id = (sel) => document.getElementById(sel);
  const loading = id("loading-edit-user");
  const content = id("content-edit-user");
  const modalEl = id("modalEditUser");
  const modal = new bootstrap.Modal(modalEl);
  const btnUnlock = id("edit-btn-unlock");
  const btnSave = id("edit-btn-save");
  const btnResetPassword = id("edit-btn-reset_password");
  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnUnlock.hidden = true;
  btnResetPassword.hidden = true;
  btnSave.hidden = true;
  modal.show();

  // Obtener los datos de la panorama
  fetch(`/stratiview/users/get_user/${panoramaId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      id("edit-user-id").value = data.id;
      id("edit-user-email").value = data.email;
      id("edit-user-first_name").value = data.first_name;
      id("edit-user-last_name").value = data.last_name;
      id("edit-user-username").value = data.username;
      id("edit-user-phone").value = data.phone;
      id("edit-user-state").value = data.state_id;

      // Mostrar contenido real y ocultar spinner
      loading.style.display = "none";
      content.style.display = "flex";
      btnSave.hidden = false;
      btnResetPassword.hidden = false;

      if (data.is_locked) {
        btnUnlock.hidden = false;
      }
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de edición.");
      console.error(error);
    });
}

window.openEditModal = openEditModal; 
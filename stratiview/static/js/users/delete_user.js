function openDeleteModal(userId) {
  const id = (sel) => document.getElementById(sel);
  const loading = id("loading-delete-user");
  const content = id("content-delete-user");
  const modalEl = id("modalDeleteUser");
  const modal = new bootstrap.Modal(modalEl);
  const btnDeleteUser = id("btn-delete-user");

  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnDeleteUser.hidden = true;
  modal.show();

  // Obtener los datos de la panorama
  fetch(`/stratiview/users/get_user/${userId}/`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar panorama.");
      return response.json();
    })
    .then((data) => {
      id("delete-user-id").value = data.id;
      id("delete-user-first_name").value = data.first_name;
      id("delete-user-last_name").value = data.last_name;
      id("delete-user-username").value = data.username;

      // Mostrar contenido real y ocultar spinner
      loading.style.display = "none";
      content.style.display = "flex";
      btnDeleteUser.hidden = false;
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de edición.");
      console.error(error);
    });
}

window.openDeleteModal = openDeleteModal; 
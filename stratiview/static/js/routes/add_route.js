function openAddModal() {
  fetch("/stratiview/check_sesion/", {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (response.status === 403) {
        window.location.href = "/stratiview/auth/sign_in/";
      }
    })
    .catch((error) => {
      console.error("Error en keep-alive:", error);
    });

  const id = (sel) => document.getElementById(sel);
  const modalEl = id("modalAddRoute");
  const modal = new bootstrap.Modal(modalEl);

  // Mostrar el modal
  modal.show();
}

window.openAddModal = openAddModal;

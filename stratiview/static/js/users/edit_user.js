function openEditModal(userId) {
  fetch('/stratiview/check_sesion/', {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then((response) => {
    if (response.status === 403) {
      window.location.href = '/stratiview/auth/sign_in/'; 
    }
  })
  .catch((error) => {
    console.error('Error en keep-alive:', error);
  });

  const id = (sel) => document.getElementById(sel);
  const loading = id("loading-edit-user");
  const content = id("content-edit-user");
  const modalEl = id("modalEditUser");
  const modal = new bootstrap.Modal(modalEl);
  const btnUnlock = id("edit-btn-unlock");
  const btnSave = id("edit-btn-save");
  const btnResetPassword = id("edit-btn-reset_password");
  const btnEnableUser = id("edit-btn-enable_user")
  const areaSelect = id("edit-user-area");
  const rolSelect = id("edit-user-rol"); 


  // Mostrar el modal
  loading.style.display = "block";
  content.style.display = "none";
  btnUnlock.hidden = true;
  btnResetPassword.hidden = true;
  btnSave.hidden = true;
  btnEnableUser.hidden = true;
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

      if (data.is_active === false) {
        btnEnableUser.hidden = false;
      }

      // Configurar Área y Rol
      if (data.area_id) {
        areaSelect.value = data.area_id;
        rolSelect.innerHTML = "";

        if (areaRolesMap[data.area_id]) {
          areaRolesMap[data.area_id].forEach(function (rol) {
            const option = document.createElement("option");
            option.value = rol.id;
            option.textContent = rol.name;
            rolSelect.appendChild(option);
          });
        } else {
          const option = document.createElement("option");
          option.value = "";
          option.textContent = "-- Sin roles disponibles --";
          rolSelect.appendChild(option);
        }

        if (data.rol_id) {
          rolSelect.value = data.rol_id;
        }
      }

      areaSelect.addEventListener("change", function () {
        const selectedAreaId = this.value;
      
        rolSelect.innerHTML = "";
      
        if (areaRolesMap[selectedAreaId]) {
          areaRolesMap[selectedAreaId].forEach(function (rol) {
            const option = document.createElement("option");
            option.value = rol.id;
            option.textContent = rol.name;
            rolSelect.appendChild(option);
          });
        } else {
          const option = document.createElement("option");
          option.value = "";
          option.textContent = "-- Sin roles disponibles --";
          rolSelect.appendChild(option);
        }
      });
    })
    .catch((error) => {
      window.alert("Error al abrir el modal de edición.");
      console.error(error);
    });
}

window.openEditModal = openEditModal; 
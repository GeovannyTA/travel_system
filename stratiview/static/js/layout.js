// Funcion para ocultar el menu de hamburguesa
document.addEventListener("DOMContentLoaded", function () {
  const closeBtn = document.getElementById("closeMenuBtn");
  const navbarCollapse = document.getElementById("navbarSupportedContent");

  if (closeBtn && navbarCollapse) {
    closeBtn.addEventListener("click", function () {
      const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);
      if (collapseInstance) {
        collapseInstance.hide();
      }
    });
  }
});

// Funcion para ocultar el mensaje de alerta
alert = document.getElementById("alert");
if (alert) {
  setTimeout(() => {
    alert.style.display = "none";
  }, 3500);
}

document.addEventListener("DOMContentLoaded", function () {
  const navbarCollapse = document.getElementById("navbarSupportedContent");
  const navbarBackdrop = document.getElementById("navbar-backdrop");
  const closeBtn = document.getElementById("closeMenuBtn");

  if (navbarCollapse) {
    navbarCollapse.addEventListener("show.bs.collapse", () => {
      navbarBackdrop.style.display = "block";
    });

    navbarCollapse.addEventListener("hide.bs.collapse", () => {
      navbarBackdrop.style.display = "none";
    });
  }

  if (navbarBackdrop) {
    navbarBackdrop.addEventListener("click", () => {
      const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);
      if (collapseInstance) {
        collapseInstance.hide();
      }
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);
      if (collapseInstance) {
        collapseInstance.hide();
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-predio-submit");

  console.log("Form:", form);
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
      clave: form["marker-key"].value,
      cuenta: form["marker-account"].value,
      uso_actual: form["marker-type-current_use"].value,
      uso_actualizado: form["marker-type-update_use"].value,
      tipo: form["marker-type"].value,
      tamano: form["marker-size"].value,
      observacion: form["marker-observation"].value,
    };

    fetch(form.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.success) {
          alert("Marcador guardado correctamente.");
          form.reset();
        } else {
          alert("Error: " + res.error);
        }
      })
      .catch((err) => {
        console.error("Error al enviar:", err);
      });
  });

  // Función para obtener el token CSRF desde la cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

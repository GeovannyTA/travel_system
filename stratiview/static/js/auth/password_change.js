document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('passwordChangeForm');
  const newPassword1 = document.getElementById('new_password1');
  const newPassword2 = document.getElementById('new_password2');
  const alertDiv = document.getElementById('alert-info');

  form.addEventListener('submit', function (event) {
    const password = newPassword1.value;
    const confirmPassword = newPassword2.value;

    // Validación de complejidad
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

    if (!regex.test(password)) {
      event.preventDefault();
      alertDiv.innerHTML = '<p class="text-danger">La nueva contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.</p>';
      return;
    }

    if (password !== confirmPassword) {
      event.preventDefault();
      alertDiv.innerHTML = '<p class="text-danger">Las contraseñas no coinciden.</p>';
    }
  });
});
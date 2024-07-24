document.getElementById('register-button').addEventListener('click', function(event) {
    var username = document.getElementById('username-input');
    var email = document.getElementById('email-input');
    var password = document.getElementById('password-input');
    var confirm = document.getElementById('confirm-input');
    var errorMessage = document.getElementById('error-message')

    errorMessage.textContent = "";

    var error = false;

    if (username.value.trim().length < 8 || username.value.trim().length > 32) {
        username.style.borderColor = "red";
        errorMessage.textContent += "El nombre de usuario debe tener entre 8 y 32 caracteres. ";
        error = true;
    } else {
        username.style.borderColor = "";
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value.trim())) {
        email.style.borderColor = "red";
        errorMessage.textContent += "Ingrese un correo electrónico válido. ";
        error = true;
    } else {
        email.style.borderColor = "";
    }

    if (password.value.trim().length < 8) {
        password.style.borderColor = "red";
        errorMessage.textContent += "La contraseña debe tener como mínimo 8 caracteres. ";
        error = true;
    } else {
        password.style.borderColor = "";
    }

    if (confirm.value.trim() !== password.value.trim()) {
        confirm.style.borderColor = "red";
        errorMessage.textContent += "Las contraseñas deben coincidir. "
        error = true;
    } else {
        confirm.style.borderColor = "";
    }

    if (error) {
        event.preventDefault();
    }
});

document.querySelector("form").setAttribute("action", "");
document.getElementById('login-button').addEventListener('click', function(event) {
    var username = document.getElementById('username-input');
    var password = document.getElementById('password-input');
    var errorMessage = document.getElementById('error-message');

    errorMessage.textContent = "";

    var error = false;

    if(username.value.trim().length < 8 || username.value.trim().length > 32) {
        username.style.borderColor = "red";
        errorMessage.textContent = "El nombre de usuario es incorrecto o no ha sido ingresado.";
        error = true;
    } else {
        username.style.borderColor = "";
    }

    if(password.value.trim().length < 8) {
        password.style.borderColor = "red";
        errorMessage.textContent = "La contraseña es incorrecta o no ha sido ingresada.";
        error = true;
    } else {
        password.style.borderColor = "";
    }

    if((username.value.trim().length < 8 || username.value.trim().length > 32) && password.value.trim().length < 8) {
        username.style.borderColor = "red";
        password.style.borderColor = "red";
        errorMessage.textContent = "El nombre de usuario y la contraseña son incorrectos o no han sido ingresados.";
        error = true;
    } else {
        username.style.borderColor = "";
        password.style.borderColor = "";
    }

    if (error) {
        event.preventDefault();
    }
});

document.querySelector("form").setAttribute("action", "");
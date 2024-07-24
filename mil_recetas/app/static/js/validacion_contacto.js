document.getElementById('boton-enviar').addEventListener('click', function(event) {
    var name = document.getElementById('name');
    var lastname = document.getElementById('lastname');
    var email = document.getElementById('email');
    var phone = document.getElementById('phone');
    var message = document.getElementById('message');
    var checkbox = document.getElementById('checkbox');
    var errorMessage = document.getElementById('error-message');
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var phoneRegex = /^\d{10,}$/;

    errorMessage.textContent = "";

    var error = false;

    if (name.value.trim() === "" || name.value.trim().length < 2 || /\d/.test(name.value.trim())) {
        name.style.borderColor = "red";
        errorMessage.textContent += "Debes ingresar tu nombre sin números. ";
        error = true;
    } else {
        name.style.borderColor = "";
    }

    if (lastname.value.trim() === "" || lastname.value.trim().length < 2 || /\d/.test(lastname.value.trim())) {
        lastname.style.borderColor = "red";
        errorMessage.textContent += "Debes ingresar tu apellido sin números. ";
        error = true;
    } else {
        lastname.style.borderColor = "";
    }

    if (!emailRegex.test(email.value.trim())) {
        email.style.borderColor = "red";
        errorMessage.textContent += "Ingresa un correo electrónico válido. ";
        error = true;
    } else {
        email.style.borderColor = "";
    }

    if (phone.value.trim() !== "" && !phoneRegex.test(phone.value.trim())) {
        phone.style.borderColor = "red";
        errorMessage.textContent += "Ingresa un número de teléfono válido (al menos 10 dígitos). ";
        error = true;
    } else {
        phone.style.borderColor = "";
    }

    if (message.value.trim() === "") {
        message.style.borderColor = "red";
        errorMessage.textContent += "Debes ingresar un mensaje. ";
        error = true;
    } else {
        message.style.borderColor = "";
    }

    if (!checkbox.checked) {
        checkbox.style.borderColor = "red";
        errorMessage.textContent += "Debes aceptar los términos y condiciones. ";
        error = true;
    } else {
        checkbox.style.borderColor = "";
    }

    if (error) {
        event.preventDefault();
    }
});

document.querySelector("form").setAttribute("action", "");
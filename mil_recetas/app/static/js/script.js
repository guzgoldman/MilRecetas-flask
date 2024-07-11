document.addEventListener('DOMContentLoaded', function () {
    const enlaces = document.querySelectorAll('a[href^="#"]');

    for (const enlace of enlaces) {
        enlace.addEventListener('click', function (event) {
            event.preventDefault();
            const id = this.getAttribute('href');
            const elemento = document.querySelector(id);

            if (elemento) {
                elemento.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    }
});

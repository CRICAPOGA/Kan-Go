const menuToggle = document.getElementById('menu');
const sidebar = document.querySelector('.sidebar');
const main = document.querySelector('main');
const menuLinks = document.querySelectorAll('.sidebar a');

// Función para alternar el menú en dispositivos móviles
menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('menu-toggle'); // Abre o cierra el sidebar
    main.classList.toggle('menu-toggle');    // Ajusta el contenido principal
});

// Cerrar el menú al hacer clic en una opción del menú
menuLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebar.classList.remove('menu-toggle'); // Cierra el sidebar
        main.classList.remove('menu-toggle');    // Ajusta el contenido principal
    });
});

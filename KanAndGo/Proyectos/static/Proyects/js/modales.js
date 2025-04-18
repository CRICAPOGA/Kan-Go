// Modal de crear proyecto
function openCreateModal() {
    document.getElementById('modalCrear').style.display = 'block';
}

function closeCreateModal() {
    document.getElementById('modalCrear').style.display = 'none';
}
// Cerrar modal si se da clic en el fondo oscuro
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}
// Restricción en la fecha (no anterior a hoy)
document.addEventListener('DOMContentLoaded', function () {
    const fechaInput = document.getElementById('id_fecha_finalizacion');
    if (fechaInput) {
        const today = new Date().toISOString().split('T')[0];
        fechaInput.min = today;
    }
});

// Interceptar el envío del formulario de edición para enviarlo mediante fetch() (AJAX)
document.addEventListener('submit', function (event) {
    if (event.target && event.target.id === 'editarProyectoForm') {
        event.preventDefault(); // Evitar envío tradicional del formulario

        const form = event.target;
        const formData = new FormData(form);
        const proyectoId = form.dataset.proyectoId;

        fetch(`/proyectos/editar/${proyectoId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
            .then(response => {
                if (response.ok) {
                    // Cerrar el modal y recargar el dashboard
                    document.getElementById('modalEditar').style.display = "none";
                    window.location.reload();
                } else {
                    return response.text().then(data => {
                        // Mostrar errores de validación si los hay
                        document.getElementById('modalFormContainer').innerHTML = data;
                    });
                }
            })
            .catch(error => {
                console.error('Error al guardar el proyecto:', error);
            });
    }
});

// Modal de editar y cargar contenido
function openModal(proyectoId) {
    // Realizar solicitud AJAX para obtener el formulario de edición
    fetch(`/proyectos/editar/${proyectoId}/`, {
        method: 'GET', // Método GET para obtener el contenido
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // Esto indica que es una solicitud AJAX
        }
    })
        .then(response => response.text())  // Procesar la respuesta como texto
        .then(data => {
            // Colocar contenido del formulario en el contenedor del modal
            document.getElementById('contenedorForm').innerHTML = data;
            // Mostrar modal
            document.getElementById('modalEditar').style.display = "block";
        })
        .catch(error => {
            console.error('Error al cargar el formulario:', error);
        });
}

function closeModal() {
    // Ocultar modal cuando el usuario le de en cerrar
    document.getElementById('modalEditar').style.display = "none";
}

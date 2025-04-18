// Permitir que un elemento sea soltado en una columna
function allowDrop(ev) {
    ev.preventDefault(); 
}
// Iniciar arrastre de una tarea
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id); // Guardar el id del elemento
}
// Al soltar una tarea en una columna
function drop(ev, estadoNuevo) {
    ev.preventDefault(); // permitir soltar
    var data = ev.dataTransfer.getData("text"); // recuperar id
    var tareaElement = document.getElementById(data); // encontrar elemento con ese id
    const columna = ev.target.closest('.column'); // encontrar columna donde se soltó
    columna.appendChild(tareaElement); // mover visualmente la tarea a esa columna

    ordenarTareasPorPrioridad(columna); // reordenar la columna según prioridad

    const tareaId = data.split('-')[1]; // obtener id
    const urlActualizar = document.body.dataset.urlActualizar; // obtener URL del <body>

    // Enviar los cambios al servidor con fetch
    fetch(urlActualizar, {
        // Enviar id y nuevo estado de la tarea
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content') // protección CSRF
        },        
        body: JSON.stringify({
            "tarea_id": tareaId,
            "estado": estadoNuevo
        })
    }).then(response => {
        if (!response.ok) {
            alert("Error al actualizar tarea.");
        }
    });
}

function ordenarTareasPorPrioridad(columna) {
    // Convertir en un array
    const tareas = Array.from(columna.querySelectorAll(".task"));
    // Ordenar según metodo obtenerPrioridad
    tareas.sort((a, b) => {
        return obtenerPrioridad(a) - obtenerPrioridad(b);
    });
    // Reinsertar en orden
    tareas.forEach(t => columna.appendChild(t));
}

function obtenerPrioridad(tarea) {
    // Obtener atributos del html
    const esUrgente = tarea.dataset.urgente === "true";
    const esImportante = tarea.dataset.importante === "true";
    // Asignar número según prioridad
    if (esUrgente && esImportante) return 0;
    if (esUrgente) return 1;
    if (esImportante) return 2;
    return 3;
}

// Modal de crear tarea
function abrirModalCrear() {
    document.getElementById('modalCrear').style.display = 'block';
}

function cerrarModalCrear() {
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
    const fechaInput = document.getElementById('id_fecha_vencimiento');
    if (fechaInput) {
        const today = new Date().toISOString().split('T')[0];
        fechaInput.min = today;
    }
});
// Modal de ver detalles tarea
function mostrarDetalleTarea(element) {
    document.getElementById('detalleTitulo').textContent = element.dataset.titulo;
    document.getElementById('detalleDescripcion').textContent = element.dataset.descripcion;
    document.getElementById('detalleFecha').textContent = element.dataset.fecha;
    document.getElementById('detalleUrgente').textContent = element.dataset.urgente;
    document.getElementById('detalleImportante').textContent = element.dataset.importante;

    document.getElementById('modalDetalle').style.display = 'block';
}

function cerrarDetalleModal() {
    document.getElementById('modalDetalle').style.display = 'none';
}

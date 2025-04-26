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
    const tarea = element.closest('.task');
    const urgente = tarea.dataset.urgente === 'true' ? 'Sí' : 'No';
    const importante = tarea.dataset.importante === 'true' ? 'Sí' : 'No';

    document.getElementById('detalleTitulo').textContent = tarea.dataset.titulo;
    document.getElementById('detalleDescripcion').textContent = tarea.dataset.descripcion;
    document.getElementById('detalleFecha').textContent = tarea.dataset.fecha;
    document.getElementById('detalleUrgente').textContent = urgente;
    document.getElementById('detalleImportante').textContent = importante

    document.getElementById('modalDetalle').style.display = 'block';
}

function cerrarDetalleModal() {
    document.getElementById('modalDetalle').style.display = 'none';
}

// Modal de eliminación
function abrirModalEliminar(tareaId, nombreTarea) {
    const form = document.getElementById('formEliminar');
    form.action = `/tareas/eliminar/${tareaId}/`; 
    document.getElementById('nombreTareaEliminar').textContent = `"${nombreTarea}"`;
    document.getElementById('modalEliminar').style.display = "block";
}

function cerrarModalEliminar() {
    // Ocultar modal cuando el usuario le de en cerrar
    document.getElementById('modalEliminar').style.display = "none";
}

function abrirModalEditar(elemento) {
    const modal = document.getElementById("modalEditar");

    // Obtener los datos desde el botón
    const tareaId = elemento.getAttribute("data-id");
    const titulo = elemento.getAttribute("data-titulo");
    const descripcion = elemento.getAttribute("data-descripcion");
    const fecha = elemento.getAttribute("data-fecha");
    const urgente = elemento.getAttribute("data-urgente") === "true";
    const importante = elemento.getAttribute("data-importante") === "true";

    // Llenar los campos del modal
    document.getElementById("edit_tarea_id").value = tareaId;
    document.getElementById("edit_titulo").value = titulo;
    document.getElementById("edit_descripcion").value = descripcion;
    document.getElementById("edit_fecha_vencimiento").value = fecha;
    document.getElementById("edit_es_urgente").checked = urgente;
    document.getElementById("edit_es_importante").checked = importante;

    // Actualiza el action del formulario
    const formEditar = document.getElementById("formEditar");
    formEditar.action = `/tareas/editar/${tareaId}/`;

    // Mostrar modal
    modal.style.display = "block";
}

function cerrarModalEditar() {
    document.getElementById("modalEditar").style.display = "none";
}

function abrirPomodoro(tituloTarea) {
    // Redirigir al temporizador Pomodoro con el título de la tarea como parámetro
    const urlPomodoro = `/pomodoro/?tarea=${encodeURIComponent(tituloTarea)}`;
    window.location.href = urlPomodoro;
}

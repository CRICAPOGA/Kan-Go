// Modal de crear proyecto
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
    const fechaInput = document.getElementById('id_fecha_finalizacion');
    if (fechaInput) {
        const today = new Date().toISOString().split('T')[0];
        fechaInput.min = today;
    }
});
// Modal de editar proyecto
function abrirModalEditar(elemento) {
    const modal = document.getElementById("modalEditar");

    // Obtener los datos desde el botón o elemento
    const proyectoId = elemento.getAttribute("data-id");
    const nombreProyecto = elemento.getAttribute("data-nombre");
    const descripcion = elemento.getAttribute("data-descripcion");
    const fechaFinalizacion = elemento.getAttribute("data-fecha-finalizacion");

    // Llenar los campos del modal
    document.getElementById("edit_proyecto_id").value = proyectoId;
    document.getElementById("edit_nombre_proyecto").value = nombreProyecto;
    document.getElementById("edit_descripcion").value = descripcion;
    document.getElementById("edit_fecha_finalizacion").value = fechaFinalizacion;

    // Actualizar la acción del formulario
    const formEditar = document.getElementById("formEditar");
    formEditar.action = `/proyectos/editar/${proyectoId}/`;

    // Mostrar modal
    modal.style.display = "block";
}

function cerrarModalEditar() {
    document.getElementById("modalEditar").style.display = "none";
}


// Modal de eliminación
function abrirModalEliminar(proyectoId, nombreProyecto) {
    const form = document.getElementById('formEliminar');
    form.action = `/proyectos/eliminar/${proyectoId}/`; 
    document.getElementById('nombreProyectoEliminar').textContent = `"${nombreProyecto}"`;
    document.getElementById('modalEliminar').style.display = "block";
}

function cerrarModalEliminar() {
    // Ocultar modal cuando el usuario le de en cerrar
    document.getElementById('modalEliminar').style.display = "none";
}

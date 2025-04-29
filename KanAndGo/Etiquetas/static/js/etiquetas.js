// Modal Crear Etiqueta
function abrirModalCrearEtiqueta() {
    document.getElementById('modalCrearEtiqueta').style.display = 'block';
}

function cerrarModalCrearEtiqueta() {
    document.getElementById('modalCrearEtiqueta').style.display = 'none';
}

function abrirModalEditarEtiqueta(id, nombre, color) {
    const modal = document.getElementById('modalEditarEtiqueta');
    modal.classList.add('show');

    document.getElementById('editEtiquetaId').value = id;
    document.getElementById('editEtiquetaNombre').value = nombre;
    document.getElementById('editEtiquetaColor').value = color;

    // Cambiar acción del form
    document.getElementById('formEditarEtiqueta').action = `/etiquetas/editar/${id}/`;
}

function cerrarModalEditarEtiqueta() {
    const modal = document.getElementById('modalEditarEtiqueta');
    modal.classList.remove('show');
}

// Modal de eliminar etiqueta
function abrirModalEliminarEtiqueta(etiquetaId, nombreEtiqueta) {
    const form = document.getElementById('formEliminar');
    form.action = `/etiquetas/eliminar/${etiquetaId}/`; 
    document.getElementById('nombreEtiquetaEliminar').textContent = `"${nombreEtiqueta}"`;
    document.getElementById('modalEliminarEtiqueta').style.display = "block";
}

function cerrarModalEliminarEtiqueta() {
    // Ocultar modal cuando el usuario le de en cerrar
    document.getElementById('modalEliminarEtiqueta').style.display = "none";
}
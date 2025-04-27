// Modal Crear Etiqueta
function abrirModalCrearEtiqueta() {
    document.getElementById('modalCrearEtiqueta').style.display = 'block';
}

function cerrarModalCrearEtiqueta() {
    document.getElementById('modalCrearEtiqueta').style.display = 'none';
}

function abrirModalEditarEtiqueta(button) {
    var etiquetaId = button.getAttribute("data-id");
    var etiquetaNombre = button.getAttribute("data-etiqueta");
    var etiquetaColor = button.getAttribute("data-color");

    // Asignar los valores a los campos del modal
    document.getElementById("editEtiquetaId").value = etiquetaId;
    document.getElementById("editEtiquetaNombre").value = etiquetaNombre;
    document.getElementById("editEtiquetaColor").value = etiquetaColor;

    // Mostrar el modal
    document.getElementById("modalEditarEtiqueta").style.display = "block";
}

function cerrarModalEditarEtiqueta() {
    // Cerrar el modal
    document.getElementById("modalEditarEtiqueta").style.display = "none";
}


// // Modal de eliminar etiqueta
// function abrirModalEliminarEtiqueta(usuarioId, nombreUsuario, apellidoUsuario) {
//     const form = document.getElementById('formEliminar');
//     form.action = `/usuarios/eliminar/${usuarioId}/`; 
//     document.getElementById('nombreUsuarioEliminar').textContent = `"${nombreUsuario} ${apellidoUsuario}"`;
//     document.getElementById('modalEliminarE').style.display = "block";
// }

// function cerrarModalEliminarEtiqueta() {
//     // Ocultar modal cuando el usuario le de en cerrar
//     document.getElementById('modalEliminarE').style.display = "none";
// }
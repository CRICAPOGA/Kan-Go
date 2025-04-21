// Modal de crear usuario
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

// Modal de eliminación
function abrirModalEliminar(usuarioId, nombreUsuario, apellidoUsuario) {
    const form = document.getElementById('formEliminar');
    form.action = `/usuarios/eliminar/${usuarioId}/`; 
    document.getElementById('nombreUsuarioEliminar').textContent = `"${nombreUsuario} ${apellidoUsuario}"`;
    document.getElementById('modalEliminar').style.display = "block";
}

function cerrarModalEliminar() {
    // Ocultar modal cuando el usuario le de en cerrar
    document.getElementById('modalEliminar').style.display = "none";
}
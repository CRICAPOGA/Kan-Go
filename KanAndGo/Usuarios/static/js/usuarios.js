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

function abrirModalEditar(elemento) {
    const modal = document.getElementById("modalEditar");

    // Obtener los datos desde el botón
    const usuarioId = elemento.getAttribute("data-id");
    const nombre = elemento.getAttribute("data-nombre");
    const apellido = elemento.getAttribute("data-apellido");
    const nombre_usuario = elemento.getAttribute("data-nombre_usuario");
    const correo = elemento.getAttribute("data-correo");
    const rol_id = elemento.getAttribute("data-rol_id");

    // Llenar los campos del modal
    document.getElementById("edit_usuario_id").value = usuarioId;
    document.getElementById("edit_nombre").value = nombre;
    document.getElementById("edit_apellido").value = apellido;
    document.getElementById("edit_nombre_usuario").value = nombre_usuario;
    document.getElementById("edit_correo").value = correo;
    document.getElementById("edit_rol_id").value = rol_id;

    // Actualiza el action del formulario
    const formEditar = document.getElementById("formEditar");
    formEditar.action = `/usuarios/editar/${usuarioId}/`;

    // Mostrar modal
    modal.style.display = "block";
}

function cerrarModalEditar() {
    document.getElementById("modalEditar").style.display = "none";
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
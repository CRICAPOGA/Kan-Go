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

//////////////////////////////////////////////////////////////////////////////////////////////////////

//Modal Crear Rol
function abrirModalCrearR() {
    document.getElementById('modalCrearR').style.display = 'block';
}

function cerrarModalCrearR() {
    document.getElementById('modalCrearR').style.display = 'none';
}

// Cerrar modal si se da clic en el fondo oscuro
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}

//Modal Editar Rol
function abrirModalEditarR(elemento) {
    const rolId = elemento.getAttribute('data-rol_id');
    const rolNombre = elemento.getAttribute('data-rol');

    const select = document.getElementById('edit_rol_id');
    const input = document.getElementById('editRolNombre');
    const form = document.getElementById('formEditar');

    // Selecciona el rol en el select
    for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value === rolId) {
            select.selectedIndex = i;
            break;
        }
    }

    // Establece el valor en el input
    input.value = rolNombre;

    // Actualiza la acción del formulario
    form.action = `/usuarios/roles/editar/${rolId}/`;

    document.getElementById('modalEditarR').style.display = 'block';
}

function actualizarInputRol(select) {
    const selectedOption = select.options[select.selectedIndex];
    const nombreRol = selectedOption.getAttribute('data-nombre');
    const rolId = selectedOption.value;

    document.getElementById('editRolNombre').value = nombreRol;
    document.getElementById('formEditar').action = `/usuarios/roles/editar/${rolId}/`;
}

function cerrarModalEditarR() {
    document.getElementById('modalEditarR').style.display = "none";
}

//Modal Eliminar Rol
function abrirModalEliminarR() {
    const modal = document.getElementById('modalEliminarR');
    const select = document.getElementById('selectRolEliminar');
    actualizarNombreRolEliminar(select);
    modal.style.display = 'block';
}

function actualizarNombreRolEliminar(select) {
    const selectedOption = select.options[select.selectedIndex];
    const nombreRol = selectedOption.getAttribute('data-nombre');
    const rolId = selectedOption.value;

    document.getElementById('nombreRolEliminar').textContent = nombreRol;
    document.getElementById('hiddenRolId').value = rolId;

    // Actualiza la acción del formulario
    document.getElementById('formEliminarRol').action = `/usuarios/roles/eliminar/${rolId}/`;
}

function cerrarModalEliminarR() {
    document.getElementById('modalEliminarR').style.display = "none";
}

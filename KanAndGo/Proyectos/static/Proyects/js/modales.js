// Modal de crear proyecto
function openCreateModal() {
    document.getElementById('modalCrear').style.display = 'block';
}

function closeCreateModal() {
    document.getElementById('modalCrear').style.display = 'none';
}

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

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
    ev.preventDefault();
    // Obtener id y moverla visualmente
    var data = ev.dataTransfer.getData("text");
    var tareaElement = document.getElementById(data);
    ev.target.appendChild(tareaElement);
    // Obtener id de la tarea
    const tareaId = data.split('-')[1];
    // Obtener URL del atributo del <body>
    const urlActualizar = document.body.dataset.urlActualizar;
    // Actualizar el estado de la tarea
    fetch(urlActualizar, {
        // Enviar id y nuevo estado de la tarea
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
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

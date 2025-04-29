document.addEventListener('DOMContentLoaded', function () {
    const filtro = document.getElementById('fecha_filtro');
    const fechas = document.getElementById('fechas_personalizadas');

    if (filtro && fechas) {
        const toggleFechas = () => {
            fechas.style.display = filtro.value === 'personalizado' ? 'block' : 'none';
        };

        // Al cargar la página
        toggleFechas();

        // Al cambiar el filtro
        filtro.addEventListener('change', toggleFechas);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const datosTareas = document.getElementById('datos-tareas');

    if (datosTareas) {
        const completadas = parseInt(datosTareas.dataset.completadas);
        const enProgreso = parseInt(datosTareas.dataset.enProgreso);
        const pendientes = parseInt(datosTareas.dataset.pendientes);
        const vencidas = parseInt(datosTareas.dataset.vencidas);

        const total = completadas + enProgreso + pendientes + vencidas;

        if (total > 0) {
            const ctx = document.getElementById('graficoTareas').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Completadas', 'En progreso', 'Pendientes', 'Vencidas'],
                    datasets: [{
                        data: [completadas, enProgreso, pendientes, vencidas],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.6)',   // Completadas
                            'rgba(255, 206, 86, 0.6)',   // En progreso
                            'rgba(255, 99, 132, 0.6)',    // Pendientes
                            'rgba(255, 99, 71, 0.6)' // Tomate (Rojo Naranja)

                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 71, 0.6)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw;
                                    const percentage = ((value / total) * 100).toFixed(2) + '%';
                                    return `${context.label}: ${value} (${percentage})`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const dataElement = document.getElementById('sesionesPorTareaData');
    const sesionesPorTarea = JSON.parse(dataElement.textContent);

    var canvas = document.getElementById('graficoSesiones');
    if (canvas) {
        var ctx = canvas.getContext('2d');
        // continuar usando ctx
    } else {
        console.warn("Canvas no encontrado");
    }

    if (Array.isArray(sesionesPorTarea) && sesionesPorTarea.length > 0) {
        const labels = sesionesPorTarea.map(item => item.tarea_id__titulo);
        const datos = sesionesPorTarea.map(item => item.total_sesiones);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total de Sesiones',
                    data: datos,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Número de Sesiones'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Tareas',
                        },
                        ticks: {
                            autoSkip: false,
                            maxRotation: 90,  // Aquí rotamos las etiquetas
                            minRotation: 90,   // Aseguramos que las etiquetas siempre estén rotadas a 90 grados
                        }
                    }
                }
            }
        });
    } else {
        console.log("No hay datos de sesiones para mostrar.");
    }
});

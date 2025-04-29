let temporizadorActual;
let temporizadorCorriendo = false;
let indiceTemporizador = 0; // Índice para rastrear el temporizador actual
let tiempoRestante; // Variable para almacenar el tiempo restante

// Función para inicializar y ejecutar los temporizadores de forma secuencial
function iniciarTemporizadorPersonalizado() {
    if (temporizadoresCreados.length === 0) {
        alert("No hay temporizadores creados.");
        return;
    }

    if (temporizadorCorriendo) {
        alert("Ya hay un temporizador en ejecución.");
        return;
    }

    if (tiempoRestante === undefined) {
        // Iniciar el primer temporizador en la lista si no hay tiempo restante almacenado
        indiceTemporizador = 0;
        ejecutarTemporizadorSecuencial();
    } else {
        // Reanudar el temporizador pausado
        temporizadorCorriendo = true;
        temporizadorActual = setInterval(() => {
            if (tiempoRestante <= 0) {
                clearInterval(temporizadorActual);
                temporizadorCorriendo = false;
                tiempoRestante = undefined;
                indiceTemporizador++;
                ejecutarTemporizadorSecuencial(); // Ejecutar el siguiente temporizador
                return;
            }

            tiempoRestante--;

            // Calcular horas, minutos y segundos restantes
            const horasRestantes = Math.floor(tiempoRestante / 3600);
            const minutosRestantes = Math.floor((tiempoRestante % 3600) / 60);
            const segundosRestantes = tiempoRestante % 60;

            // Actualizar la interfaz
            document.getElementById("horasCreados").innerText = formatearTiempo(horasRestantes);
            document.getElementById("minutosCreados").innerText = formatearTiempo(minutosRestantes);
            document.getElementById("segundosCreados").innerText = formatearTiempo(segundosRestantes);
        }, 1000);
    }
}

// Función para ejecutar un temporizador basado en el índice actual
function ejecutarTemporizadorSecuencial() {
    if (!Array.isArray(temporizadoresCreados) || temporizadoresCreados.length === 0) {
        console.error("No hay temporizadores creados o la lista no es válida.");
        return;
    }

    if (indiceTemporizador >= temporizadoresCreados.length) {
        console.log("No hay más temporizadores para ejecutar. Reiniciando al primero.");
        indiceTemporizador = 0; // Reiniciar al primer temporizador
    }

    const temporizador = temporizadoresCreados[indiceTemporizador];
    if (!temporizador) {
        console.error(`No se encontró un temporizador en el índice ${indiceTemporizador}`);
        return;
    }

    console.log(`Iniciando temporizador: ${temporizador.titulo}`);
    iniciarTemporizador(temporizador.horas, temporizador.minutos, temporizador.segundos, () => {
        // Callback al finalizar el temporizador actual
        indiceTemporizador++;
        ejecutarTemporizadorSecuencial(); // Ejecutar el siguiente temporizador
    });
}

// Función genérica para iniciar un temporizador
function iniciarTemporizador(horas, minutos, segundos, callback) {
    if (temporizadorCorriendo) {
        clearInterval(temporizadorActual); // Detener cualquier temporizador en ejecución
    }

    tiempoRestante = horas * 3600 + minutos * 60 + segundos; // Convertir todo a segundos
    temporizadorCorriendo = true;

    temporizadorActual = setInterval(() => {
        if (tiempoRestante <= 0) {
            clearInterval(temporizadorActual);
            temporizadorCorriendo = false;
            tiempoRestante = undefined;
            if (callback) callback(); // Llamar al callback para continuar con el siguiente temporizador
            return;
        }

        tiempoRestante--;

        // Calcular horas, minutos y segundos restantes
        const horasRestantes = Math.floor(tiempoRestante / 3600);
        const minutosRestantes = Math.floor((tiempoRestante % 3600) / 60);
        const segundosRestantes = tiempoRestante % 60;

        // Actualizar la interfaz
        document.getElementById("horasCreados").innerText = formatearTiempo(horasRestantes);
        document.getElementById("minutosCreados").innerText = formatearTiempo(minutosRestantes);
        document.getElementById("segundosCreados").innerText = formatearTiempo(segundosRestantes);
    }, 1000);
}

// Función para pausar el temporizador personalizado
function pausarTemporizadorPersonalizado() {
    if (temporizadorCorriendo) {
        clearInterval(temporizadorActual);
        temporizadorCorriendo = false;
    }
}

// Función para reiniciar el temporizador personalizado
function reiniciarTemporizadorPersonalizado() {
    if (temporizadorCorriendo) {
        clearInterval(temporizadorActual);
    }
    temporizadorCorriendo = false;

    // Reiniciar la interfaz a 00:00:00
    document.getElementById("horasCreados").innerText = "00";
    document.getElementById("minutosCreados").innerText = "00";
    document.getElementById("segundosCreados").innerText = "00";
}

// Función para formatear el tiempo (agregar ceros iniciales)
function formatearTiempo(tiempo) {
    return tiempo < 10 ? `0${tiempo}` : tiempo;
}
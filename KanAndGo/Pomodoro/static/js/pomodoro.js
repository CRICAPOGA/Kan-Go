// Temporizador principal de Pomodoro
let temporizadorPrincipal;
let segundosPrincipales = 0;
let minutosPrincipales = 25;
let horasPrincipales = 0;
let temporizadorPrincipalCorriendo = false;
let cicloPomodoro = 0; // Rastrea el número de ciclos completados
let esIntervaloTrabajo = true; // Rastrea si es un intervalo de trabajo o descanso

function iniciarTemporizadorPrincipal() {
  if (!temporizadorPrincipalCorriendo) {
    temporizadorPrincipal = setInterval(actualizarTemporizadorPrincipal, 1000);
    temporizadorPrincipalCorriendo = true;
  }
}

function actualizarTemporizadorPrincipal() {
  segundosPrincipales--;

  if (segundosPrincipales < 0) {
    segundosPrincipales = 59;

    minutosPrincipales--;

    if (minutosPrincipales < 0) {
      minutosPrincipales = 59;

      horasPrincipales--;

      if (horasPrincipales < 0) {
        clearInterval(temporizadorPrincipal);
        manejarCicloPomodoro();
        return;
      }
    }
  }

  actualizarPantallaTemporizadorPrincipal();
}

function manejarCicloPomodoro() {
  clearInterval(temporizadorPrincipal);
  temporizadorPrincipalCorriendo = false;

  if (esIntervaloTrabajo) {
    cicloPomodoro++;
    document.getElementById("intervalosTrabajo").innerText = cicloPomodoro; // Actualiza el contador en la interfaz
    if (cicloPomodoro % 4 === 0) {
      // Descanso largo después de 4 intervalos de trabajo
      minutosPrincipales = 15;
    } else {
      // Descanso corto
      minutosPrincipales = 5;
    }
    esIntervaloTrabajo = false;
  } else {
    // Volver al intervalo de trabajo
    minutosPrincipales = 25;
    esIntervaloTrabajo = true;
  }

  segundosPrincipales = 0;
  horasPrincipales = 0;
  actualizarPantallaTemporizadorPrincipal();
  iniciarTemporizadorPrincipal(); // Inicia automáticamente el siguiente intervalo
}

function actualizarPantallaTemporizadorPrincipal() {
  const horasFormateadas = formatearTiempo(horasPrincipales);
  const minutosFormateados = formatearTiempo(minutosPrincipales);
  const segundosFormateados = formatearTiempo(segundosPrincipales);

  document.getElementById("horas").innerText = horasFormateadas;
  document.getElementById("minutos").innerText = minutosFormateados;
  document.getElementById("segundos").innerText = segundosFormateados;
}

function pausarTemporizador() {
  clearInterval(temporizadorPrincipal);
  temporizadorPrincipalCorriendo = false;
}

function reiniciarTemporizador() {
  clearInterval(temporizadorPrincipal);
  temporizadorPrincipalCorriendo = false;
  segundosPrincipales = 0;
  minutosPrincipales = 25;
  horasPrincipales = 0;
  cicloPomodoro = 0;
  esIntervaloTrabajo = true;
  document.getElementById("intervalosTrabajo").innerText = cicloPomodoro; // Reinicia el contador en la interfaz
  actualizarPantallaTemporizadorPrincipal();
}

function formatearTiempo(tiempo) {
  return tiempo < 10 ? `0${tiempo}` : tiempo;
}

// Para temporizadores individuales
const temporizadores = {};

function iniciarTemporizadorIndividual(idTemporizador) {
  const minutosIniciales =
    parseInt(
      document.getElementById(`minutosIniciales${idTemporizador}`).innerText
    ) || 0;
  const segundosIniciales =
    parseInt(
      document.getElementById(`segundosIniciales${idTemporizador}`).innerText
    ) || 0;

  const totalSegundos = minutosIniciales * 60 + segundosIniciales;

  temporizadores[idTemporizador] = {
    temporizador: setInterval(
      () => actualizarTemporizadorIndividual(idTemporizador),
      1000
    ),
    corriendo: true,
    horas: 0,
    minutos: minutosIniciales,
    segundos: segundosIniciales,
    totalSegundos: totalSegundos,
    barraProgreso: document.getElementById(`barraProgreso${idTemporizador}`),
  };

  establecerDuracionBarraProgreso(idTemporizador, totalSegundos);
  actualizarPantallaTemporizadorIndividual(idTemporizador);
}

function establecerDuracionBarraProgreso(idTemporizador, duracion) {
  const barraProgreso = temporizadores[idTemporizador].barraProgreso;
  barraProgreso.style.setProperty("--duracion", duracion + "s");
}

function actualizarTemporizadorIndividual(idTemporizador) {
  let temporizador = temporizadores[idTemporizador];

  if (temporizador.corriendo) {
    temporizador.segundos--;

    if (temporizador.segundos < 0) {
      temporizador.segundos = 59;
      temporizador.minutos--;

      if (temporizador.minutos < 0) {
        temporizador.minutos = 59;
        temporizador.horas--;

        if (temporizador.horas < 0) {
          clearInterval(temporizador.temporizador);
          completarTemporizador(idTemporizador);
          temporizador.corriendo = false;
          return;
        }
      }
    }

    actualizarPantallaTemporizadorIndividual(idTemporizador);
    actualizarBarraProgreso(idTemporizador);
  }
}

function actualizarBarraProgreso(idTemporizador) {
  let temporizador = temporizadores[idTemporizador];

  if (temporizador.corriendo) {
    let segundosRestantes =
      temporizador.horas * 3600 +
      temporizador.minutos * 60 +
      temporizador.segundos;
    let porcentajeProgreso =
      ((temporizador.totalSegundos - segundosRestantes) /
        temporizador.totalSegundos) *
      100;

    temporizador.barraProgreso.style.width = `${porcentajeProgreso}%`;
  }
}

function pausarTemporizadorIndividual(idTemporizador) {
  const temporizador = temporizadores[idTemporizador];

  if (temporizador.corriendo) {
    clearInterval(temporizador.temporizador);
    temporizador.corriendo = false;
  }
}

function reanudarTemporizadorIndividual(idTemporizador) {
  const temporizador = temporizadores[idTemporizador];

  if (!temporizador.corriendo) {
    temporizador.temporizador = setInterval(
      () => actualizarTemporizadorIndividual(idTemporizador),
      1000
    );
    temporizador.corriendo = true;
  }
}

function reiniciarTemporizadorIndividual(idTemporizador) {
  const minutosIniciales =
    parseInt(
      document.getElementById(`minutosIniciales${idTemporizador}`).innerText
    ) || 0;
  const segundosIniciales =
    parseInt(
      document.getElementById(`segundosIniciales${idTemporizador}`).innerText
    ) || 0;

  let temporizador = temporizadores[idTemporizador];
  clearInterval(temporizador.temporizador);
  temporizador.corriendo = false;
  temporizador.segundos = segundosIniciales;
  temporizador.horas = 0;
  temporizador.minutos = minutosIniciales;
  actualizarPantallaTemporizadorIndividual(idTemporizador);
}

function completarTemporizador(idTemporizador) {
  console.log("Completado...");
}

function actualizarPantallaTemporizadorIndividual(idTemporizador) {
  let temporizador = temporizadores[idTemporizador];
  const horasFormateadas = formatearTiempo(temporizador.horas);
  const minutosFormateados = formatearTiempo(temporizador.minutos);
  const segundosFormateados = formatearTiempo(temporizador.segundos);

  document.getElementById(`horas${idTemporizador}`).innerText =
    horasFormateadas;
  document.getElementById(`minutos${idTemporizador}`).innerText =
    minutosFormateados;
  document.getElementById(`segundos${idTemporizador}`).innerText =
    segundosFormateados;
}

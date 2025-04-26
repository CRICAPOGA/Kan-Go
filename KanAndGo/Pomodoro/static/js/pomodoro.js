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


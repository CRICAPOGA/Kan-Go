document.addEventListener('DOMContentLoaded', () => {
  const calendarDays = document.getElementById('calendar-days');
  const monthYear = document.getElementById('month-year');
  const prevBtn = document.getElementById('prev-month');
  const nextBtn = document.getElementById('next-month');
  const selectedDateElem = document.getElementById('selected-date');
  const taskList = document.getElementById('task-list');

  // Recibir año y mes actuales desde URL
  const urlParams = new URLSearchParams(window.location.search);
  let currentYear = parseInt(urlParams.get('anio')) || new Date().getFullYear();
  let currentMonth = parseInt(urlParams.get('mes')) - 1 || new Date().getMonth();

  function renderCalendar() {
    calendarDays.innerHTML = '';

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const startDay = firstDay.getDay();
    const daysInMonth = lastDay.getDate();

    monthYear.textContent = firstDay.toLocaleDateString('es-ES', {
      month: 'long',
      year: 'numeric'
    });

    for (let i = 0; i < startDay; i++) {
      const empty = document.createElement('div');
      calendarDays.appendChild(empty);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, currentMonth, day);
      const dateStr = date.toISOString().split('T')[0];

      const dayElem = document.createElement('div');
      dayElem.textContent = day;

      if (dateStr === new Date().toISOString().split('T')[0]) {
        dayElem.classList.add('today');
      }

      if (tareasPorDia[dateStr]) {
        const badge = document.createElement('div');
        badge.classList.add('project-indicator');
        badge.textContent = `${tareasPorDia[dateStr].length} tareas`;
        dayElem.appendChild(badge);
      }

      dayElem.addEventListener('click', () => {
        selectedDateElem.textContent = `Tareas para ${date.toLocaleDateString('es-ES')}`;
        taskList.innerHTML = '';

        if (tareasPorDia[dateStr]) {
          tareasPorDia[dateStr].forEach(tarea => {
            const li = document.createElement('li');
            li.textContent = `📌 ${tarea.titulo} (${tarea.proyecto})`;
            taskList.appendChild(li);
          });
        } else {
          taskList.innerHTML = '<li>Sin tareas</li>';
        }
      });

      calendarDays.appendChild(dayElem);
    }
  }

  prevBtn.addEventListener('click', () => {
    currentMonth--;
    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
    }
    window.location.href = `?mes=${currentMonth + 1}&anio=${currentYear}`;
  });

  nextBtn.addEventListener('click', () => {
    currentMonth++;
    if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }
    window.location.href = `?mes=${currentMonth + 1}&anio=${currentYear}`;
  });

  renderCalendar();
});
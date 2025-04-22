const monthYear = document.getElementById("month-year");
const calendarDays = document.getElementById("calendar-days");
const taskList = document.getElementById("task-list");
const selectedDateText = document.getElementById("selected-date");
const taskInput = document.getElementById("task-input");
const addTaskBtn = document.getElementById("add-task-btn");

let currentDate = new Date();
let selectedDate = null;

function renderCalendar(date) {
  calendarDays.innerHTML = "";

  const year = date.getFullYear();
  const month = date.getMonth();

  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();

  monthYear.textContent = `${date.toLocaleString('es-ES', { month: 'long' })} ${year}`;

  for (let i = 0; i < firstDay; i++) {
    const empty = document.createElement("div");
    calendarDays.appendChild(empty);
  }

  for (let day = 1; day <= lastDate; day++) {
    const dayDiv = document.createElement("div");
    dayDiv.textContent = day;

    const thisDate = new Date(year, month, day);
    if (isToday(thisDate)) {
      dayDiv.classList.add("today");
    }

    dayDiv.addEventListener("click", () => {
      selectedDate = thisDate;
      showTasks();
    });

    calendarDays.appendChild(dayDiv);
  }
}

function isToday(date) {
  const today = new Date();
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
}

function showTasks() {
  if (!selectedDate) return;

  const key = selectedDate.toDateString();
  const tasks = JSON.parse(localStorage.getItem(key)) || [];

  selectedDateText.textContent = `Tareas para ${key}`;
  taskList.innerHTML = "";

  tasks.forEach(task => {
    const li = document.createElement("li");
    li.textContent = task;
    taskList.appendChild(li);
  });
}

addTaskBtn.addEventListener("click", () => {
  if (!selectedDate || taskInput.value.trim() === "") return;

  const key = selectedDate.toDateString();
  const tasks = JSON.parse(localStorage.getItem(key)) || [];
  tasks.push(taskInput.value.trim());
  localStorage.setItem(key, JSON.stringify(tasks));
  taskInput.value = "";
  showTasks();
});

document.getElementById("prev-month").addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar(currentDate);
});

document.getElementById("next-month").addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar(currentDate);
});

renderCalendar(currentDate);

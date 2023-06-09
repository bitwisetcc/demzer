// Função para abri e fechar o "Calendário" da Navbar lateral
function toggleCalendar() {
  var calendarContent = document.getElementById("calendar-content");
  var arrowRotate = document.getElementById("arrow_rotate");
  var bottomContent = document.getElementById("bottom-content");

  if (calendarContent.classList.contains("hidden")) {
    calendarContent.classList.remove("hidden");
  } else {
    calendarContent.classList.add("hidden");
  }

  if (arrowRotate.classList.contains("rotate-180")) {
    arrowRotate.classList.remove("rotate-180");
  } else{
    arrowRotate.classList.add("rotate-180");
  }

  if(bottomContent.classList.contains("mt-28")){
    bottomContent.classList.remove("mt-28");
    bottomContent.classList.add("mt-14");
  } else{
    bottomContent.classList.remove("mt-14");
    bottomContent.classList.add("mt-28");
  }
}

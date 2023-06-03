import Alpine from "alpinejs";
import mask from "@alpinejs/mask";
import tippy from "tippy.js";
import "boxicons";

window.Alpine = Alpine;
Alpine.plugin(mask);
Alpine.start();

tippy("#home-icon", { content: "Dashboard", placement: "bottom" });

// Função para abri e fechar o "Calendário" da Navbar lateral
function toggleCalendar() {
  var calendarContent = document.getElementById("calendar-content");
  
  if (dropdownContent.classList.contains("hidden")) {
    dropdownContent.classList.remove("hidden"); // Mostra a dropdown
  } else {
    dropdownContent.classList.add("hidden"); // Oculta a dropdown 
  }
}

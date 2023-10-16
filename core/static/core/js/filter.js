//FOR ALL FILTERS
document.getElementById("openModalButton").addEventListener("click", function () {
  document.getElementById("modal").classList.remove("hidden");
  document.getElementById("modal").classList.add("flex");
});

document.getElementById("closeModalButton").addEventListener("click", function () {
  document.getElementById("modal").classList.add("hidden");
  document.getElementById("modal").classList.remove("flex");
});


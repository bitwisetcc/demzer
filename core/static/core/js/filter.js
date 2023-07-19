document.getElementById("openModalButton").addEventListener("click", function () {
  document.getElementById("modal").classList.remove("hidden");
});

document.getElementById("closeModalButton").addEventListener("click", function () {
  document.getElementById("modal").classList.add("hidden");
});

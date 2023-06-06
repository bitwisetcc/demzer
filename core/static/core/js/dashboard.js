document.addEventListener("alpine:init", () => {
  Alpine.data("dashboard", () => ({
    active: "Alunos",
    headers: ["RM", "Nome", "Idade", "Gênero", "Celular", "E-mail", "CPF", "RG"],
    /**
     * @param {Event} e
     */
    reload(e) {
      this.active = e.target.innerText;
      const csrfToken = document.cookie.slice(document.cookie.indexOf("=") + 1);
      
      switch (e.target.dataset.section) {
        case "students":
          this.headers = ["RM", "Nome", "Idade", "Gênero", "Celular", "E-mail", "CPF", "RG"];
          break;
      
        case "courses":
          this.headers = ["Código", "Nome", "Descrição"];
          break;
      
        default:
          break;
      }

      fetch(e.target.dataset.url, { headers: { "X-CSRFToken": csrfToken } })
        .then((res) => res.json())
        .then(console.log)
        .catch(console.error);
    },
  }));
});

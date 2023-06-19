function getAge(birthday) {
  let ageDifMs = Date.now() - birthday.getTime();
  let ageDate = new Date(ageDifMs);
  return Math.abs(ageDate.getUTCFullYear() - 1970);
}

document.addEventListener("alpine:init", () => {
  Alpine.data("dashboard", () => ({
    active: "Alunos",
    headers: [""],
    rows: [[]],
    /**
     * @param {Event} e
     */
    reload(section, active, url) {
      this.rows = [[]];
      this.active = active;
      const csrfToken = document.cookie.slice(document.cookie.indexOf("=") + 1);

      switch (section) {
        case "courses":
          this.headers = ["Código", "Nome", "Descrição", "Turmas", "Alunos"];
          break;

        case "classrooms":
          this.headers = ["Código", "Alunos", "Notas"];
          break;

        default:
          this.headers = [
            "RM",
            "Nome",
            "Idade",
            "Gênero",
            "Celular",
            "E-mail",
            "CPF",
            "RG",
          ];

          fetch(url, { headers: { "X-CSRFToken": csrfToken } })
            .then((res) => res.json())
            .then((data) => {
              data.users.forEach((user) => {
                this.rows.push([
                  user.rm,
                  user.username,
                  getAge(new Date(user.birthdate)),
                  user.gender,
                  user.phone,
                  user.email,
                  user.cpf,
                  user.rg,
                ]);
              });
            });
          break;
      }
    },
  }));
});

function getAge(birthday) {
  let ageDifMs = Date.now() - birthday.getTime();
  let ageDate = new Date(ageDifMs);
  return Math.abs(ageDate.getUTCFullYear() - 1970);
}

document.addEventListener("alpine:init", () => {
  Alpine.data("dashboard", () => ({
    active: "Alunos",
    filterDialog: false,
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
        default:
          this.headers = [
            "RM",
            "Nome",
            "Idade",
            "Nascimento",
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
                  user.birthdate,
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

//To make Carousel in dashboard work!
const carousel1Swiper = new Swiper(".carousel1", {
  slidesPerView: 1,
  keyboard: {
    enabled: false,
  },
  navigation: {
    nextEl: ".carousel1 .swiper-button-next",
    prevEl: ".carousel1 .swiper-button-prev",
  },
});

function validateCPF(cpf) {
  let remainder = 0;
  let sum = 0;

  if (cpf == "00000000000" || cpf.length != 11) return false;

  for (let i = 1; i <= 9; i++)
    sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
  remainder = (sum * 10) % 11;

  if (remainder == 10 || remainder == 11) remainder = 0;
  if (remainder != parseInt(cpf.substring(9, 10))) return false;

  sum = 0;

  for (let i = 1; i <= 10; i++)
    sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
  remainder = (sum * 10) % 11;

  if (remainder == 10 || remainder == 11) remainder = 0;

  return remainder == parseInt(cpf.substring(10, 11));
}

const validateName = (e) =>
  !/[A-Za-záàâãéèêíóôõúçñ\s\.]+$/.test(e.key) && e.preventDefault();

const validateEmail = (e) => !/[a-z0-9@\.]/.test(e.key) && e.preventDefault();

/**
 *
 * @param {KeyboardEvent} e
 */
const validateNumber = (e) => {
  e.ctrlKey ||
    (e.key != "Backspace" &&
      e.key != "Delete" &&
      !/[0-9]+$/.test(e.key) &&
      e.preventDefault());
};

document.addEventListener("alpine:init", () => {
  Alpine.data("fields", (secret = false) => ({
    init() {
      if (secret && !confirm("Você deseja criar um conta administrativa?"))
        location.replace("{% url 'dashboard' %}");
    },
    secret: secret,
    role: "student",
    cpf: "",
    rg: "",
    tab: "identidade",
    errors: [],
    cpfOk: true,
    rgOk: true,
    confirmation: false,
    password: "",
    duplicate: "",
    imageName: null,
    checks: [
      {
        description: "Conter ao menos 10 caracteres",
        test: (s, _) => s.length >= 10,
      },
      {
        description: "Conter caracteres especiais e números",
        test: (s, _) => /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/.test(s),
      },
      {
        description: "Combinar letras maiúsculas e minúsculas",
        test: (s, _) => s != s.toLowerCase() && s != s.toUpperCase(),
      },
      {
        description: "Confirme a senha",
        test: (s, d) => s == d,
      },
    ],
    switchTab() {
      this.cpfOk = validateCPF(this.cpf.replace(/[\./-]/g, ""));
      this.rgOk = this.rg.length == 12;
      if (this.cpfOk && this.rgOk) {
        this.tab = "contato";
        if (secret) {
          this.confirmation = true;
        }
      }
    },
    submit(e) {
      this.errors = [];

      if (!validateCPF(this.cpf.replace(/[\./-]/g, ""))) {
        e.preventDefault();
        this.cpfOk = false;
      }

      if (this.rg.length != 12) {
        e.preventDefault();
        this.rgOk = false;
      }

      if (this.secret) {
        for (const check of this.checks)
          check.test(this.password, this.duplicate) || e.preventDefault();
      }
    },
  }));

  Alpine.data("address", () => ({
    state: "",
    city: "",
    neighborhood: "",
    street: "",
    fillCEP(cep) {
      fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then((res) => res.json())
        .then((data) => {
          this.city = data.localidade;
          this.neighborhood = data.bairro;
          this.street = data.logradouro;
        })
        .catch(console.error);
    },
  }));
});

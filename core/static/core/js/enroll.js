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
  !/[A-Za-záàâãéèêíóôõúçñ\s]+$/.test(e.key) && e.preventDefault();

const validateNumber = (e) => {
  e.key != "Backspace" &&
    e.key != "Delete" &&
    !/[0-9]+$/.test(e.key) &&
    e.preventDefault();
};

document.addEventListener("alpine:init", () => {
  Alpine.data("fields", () => ({
    role: "student",
    cpf: "",
    rg: "",
    tab: "identidade",
    errors: [],
    submit(e) {
      this.errors = [];

      if (!validateCPF(this.cpf.replace(/[\./-]/g, ""))) {
        e.preventDefault();
        this.errors.push("CPF inválido");
      }

      if (this.rg.length != 12) {
        e.preventDefault();
        this.errors.push("RG inválido");
      }
    },
  }));

  Alpine.data("address", () => ({
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

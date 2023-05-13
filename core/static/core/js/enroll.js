function validateCPF(cpf) {
  let remainder = 0;
  let sum = 0;
  const reset = () => (remainder *= !(remainder == 10 || remainder == 11));

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

document.addEventListener("alpine:init", () => {
  Alpine.data("fields", () => ({
    name: "",
    cpf: "",
    rg: "",
    city: "",
    neighborhood: "",
    street: "",
    dismiss: true,
    errors: [],
    submit(e) {
      const requirements = [
        { test: /^[a-zA-Z]+$/.test(this.name), error: "Nome deve conter apenas letras"},
        { test: validateCPF(this.cpf), error: "CPF inválido" },
        { test: this.rg.length == 9, error: "RG inválido" },
      ];

      for (const req of requirements) {
        if (req.test) {
          e.preventDefault();
          this.errors.push(req.error);
        }
      }
    },
    fillCEP(cep) {
      fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(res => res.json())
        .then(data => {
          console.log(data);
          this.city = data.localidade;
          this.neighborhood = data.bairro;
          this.street = data.logradouro;
        })
        .catch(console.error);
    },
  }));
});

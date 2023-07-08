const emailRegex =
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

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

const validations = [
  {
    i: 0,
    test: (s) => /[A-Za-záàâãéèêíóôõúçñ\s]+$/.test(s),
    tip: "Apenas letras, espaços e pontos.",
  },
  {
    i: 1,
    test: (s) => emailRegex.test(s),
    tip: "Endereço de e-mail inválido.",
  },
  {
    i: 3,
    test: (s) => emailRegex.test(s),
    tip: "Endereço de e-mail inválido.",
  },
  {
    i: 4,
    test: (s) => s.length == 11 && !s.split().some(isNaN),
    tip: "Deve conter 11 digitos sem pontuação.",
  },
  {
    i: 5,
    test: (s) => Boolean(Date.parse(s)),
    tip: "Deve estar no formato 'YYYY-mm-dd'",
  },
  {
    i: 6,
    test: (s) => ["M", "F", "NB"].includes(s),
    tip: "Deve ser 'M', 'F' ou 'NB'",
  },
  {
    i: 7,
    test: (s) => s.length == 9 && !s.split().some(isNaN),
    tip: "Deve conter 9 digitos sem pontuação.",
  },
  {
    i: 8,
    test: validateCPF,
    tip: "Deve conter 9 digitos sem pontuação.",
  },
  // TODO: 'public_schooling forward'
];

document.addEventListener("alpine:init", () => {
  Alpine.data("userData", () => ({
    required: [
      "username",
      "email",
      "contact_email",
      "phone",
      "birthdate",
      "gender",
      "rg",
      "cpf",
      "public_schooling",
      "afro",
      "civil_state",
      "cep",
    ],
    optional: [
      "password",
      "natural_state",
      "natural_city",
      "nationality",
      "country_of_origin",
      "city",
      "neighborhood",
      "street",
      "street_number",
      "complement",
      "distance",
    ],
    rows: [],
    headers: [],
    errors: [],
    role: "student",
    readFile(e) {
      let reader = new FileReader();

      reader.addEventListener("load", () => {
        const rows = reader.result.split("\n").map((row) => row.split(","));
        const headers = rows.shift();
        this.rows = rows;
        this.headers = headers;
      });
      reader.addEventListener("error", () => console.error(reader.error));

      reader.readAsText(e.target.files[0]);
    },

    submit(e) {
      for (const user of this.rows) {
        for (const v of validations) {
          if (!v.test(String(user[v.i])))
            this.errors.push(
              `Usuário: ${user[0]}\nCampo: ${this.headers[v.i]}\nDica: ${v.tip}`
            );
        }
      }

      if (this.errors.length != 0) {
        e.preventDefault();
      }
    },
  }));
});

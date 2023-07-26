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
    id: "username",
    test: (s) => /[A-Za-záàâãéèêíóôõúçñ\s]+$/.test(s) && s.length <= 150,
    tip: "Apenas letras, espaços e pontos.",
  },
  {
    id: "email",
    test: (s) => emailRegex.test(s),
    tip: "Endereço de e-mail inválido.",
  },
  {
    id: "contact_email",
    test: (s) => emailRegex.test(s),
    tip: "Endereço de e-mail inválido.",
  },
  {
    id: "phone",
    test: (s) => s.length == 11 && Boolean(Number(s)),
    tip: "Deve conter 11 digitos sem pontuação.",
  },
  {
    id: "birthdate",
    test: (s) => Boolean(Date.parse(s)),
    tip: "Deve estar no formato 'YYYY-mm-dd'",
  },
  {
    id: "gender",
    test: (s) => ["M", "F", "NB"].includes(s),
    tip: "Deve ser 'M', 'F' ou 'NB'",
  },
  {
    id: "rg",
    test: (s) => s.length == 9 && Boolean(Number(s)),
    tip: "Deve conter 9 digitos sem pontuação.",
  },
  {
    id: "cpf",
    test: validateCPF,
    tip: "Deve conter 11 digitos sem pontuação.",
  },
  {
    id: "public_schooling",
    test: (s) => ["C", "N", "E", "M", "H"].includes(s),
    tip: "Deve ser 'C' (completo), 'N' (nenhum), 'E' (primário), 'M' (fundamental) ou 'H' (médio).",
  },
  {
    id: "afro",
    test: (s) => ["1", "0", "true", "false"].includes(s),
    tip: "Deve ser '1', '0', 'true' ou 'false'",
  },
  {
    id: "civil_state",
    test: (s) => ["S", "M", "D", "W"].includes(s),
    tip: "Deve ser 'S' (solteiro), 'M' (Casado), 'D' (divorciado) ou 'W' (viúvo)",
  },
  {
    id: "natural_state",
    test: (s) => s.length == 2,
    tip: "Deve ser a abreviação de algum estado brasileiro",
  },
  {
    id: "natural_city",
    test: (s) => s.length <= 50,
    tip: "Deve ter até 50 caracteres.",
  },
  {
    id: "nationality",
    test: (s) => s.length <= 40,
    tip: "Deve ter até 40 caracteres.",
  },
  {
    id: "country_of_origin",
    test: (s) => s.length <= 40,
    tip: "Deve ter até 40 caracteres.",
  },
  {
    id: "cep",
    test: (s) => s.length <= 8 && Boolean(Number(s)),
    tip: "Deve ter até 8 caracteres.",
  },
  {
    id: "city",
    test: (s) => s.length <= 60,
    tip: "Deve ter até 60 caracteres.",
  },
  {
    id: "neighborhood",
    test: (s) => s.length <= 40,
    tip: "Deve ter até 40 caracteres.",
  },
  {
    id: "street",
    test: (s) => s.length <= 40,
    tip: "Deve ter até 40 caracteres.",
  },
  {
    id: "street_number",
    test: (s) => Boolean(Number(s)),
    tip: "Deve ser um número.",
  },
  {
    id: "complement",
    test: (s) => s.length <= 20,
    tip: "Deve ter até 20 caracteres.",
  },
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
      "public_schooling",
    ],
    rows: [],
    headers: [],
    data: [],
    errors: [],
    role: "student",
    readFile(e) {
      let reader = new FileReader();

      reader.addEventListener("load", () => {
        const rows = reader.result.split("\n").map((row) => row.split(","));
        const headers = rows.shift();
        this.rows = rows;
        this.headers = headers;

        this.data = rows.map((row) =>
          row.reduce((acc, cur, i) => {
            acc[headers[i]] = cur;
            return acc;
          }, {})
        );
      });

      reader.addEventListener("error", () => console.error(reader.error));
      reader.readAsText(e.target.files[0]);
    },

    submit(e) {
      for (const user of this.data)
        for (const v of validations)
          if (this.headers.includes(v.id) && !v.test(String(user[v.id])))
            this.errors.push({
              user: user[0],
              field: this.headers[v.id],
              msg: v.tip,
            });

      const passing = this.errors.length == 0;
      const headersOk = this.required.reduce(
        (acc, cur) => acc && this.headers.includes(cur),
        true
      );

      if (!passing || !headersOk) e.preventDefault();
    },
  }));
});

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

    /**
     * @param {SubmitEvent} e
     */
    submit(e) {
      const csrfToken = document.cookie.slice(document.cookie.indexOf("=") + 1);
      data = this.rows.map((row) => {
        console.log();
        const header = this.rows.header((header) => header[i]);
        return { header: row };
      });
      // data = this.headers.map((header, i) => ({
      //   data: this.rows.map((row) => row[i]),
      //   header: header,
      // }));
      console.log(data);
      return;

      fetch(e.target.action, {
        body: JSON.stringify(data),
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
      })
        .then((res) => res.json())
        .then(console.log)
        .catch(console.error);
    },
  }));
});

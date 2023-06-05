document.addEventListener("alpine:init", () => {
  Alpine.data("userData", () => ({
    required: [
      "username",
      "email",
      "password",
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

      fetch(e.target.action, {
        body: JSON.stringify({ message: "wanna do something after work? 🍨" }),
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
      });
    },
  }));
});

document.addEventListener("alpine:init", () => {
  Alpine.data("userData", () => ({
    table: [[]],
    errors: [],
    readFile(e) {
      let reader = new FileReader();
      reader.addEventListener("load", () => {
        let data = reader.result.split("\n");
        this.table = data.map((row) => row.split(","));
      });
      reader.addEventListener("error", () => console.error(reader.error));

      reader.readAsText(e.target.files[0]);
    },
  }));
});

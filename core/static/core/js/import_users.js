document.addEventListener("alpine:init", () => {
  Alpine.data("userData", () => ({
    table: [[]],
    errors: [],
    readFile(e) {
      let reader = new FileReader();
      reader.addEventListener("load", () => {
        this.table = reader.result.split("\n");
      });
      reader.addEventListener("error", () => console.error(reader.error));

      reader.readAsText(e.target.files[0]);
    },
  }));
});

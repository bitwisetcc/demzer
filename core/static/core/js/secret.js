if (!confirm("Você deseja criar um conta administrativa?"))
  location.replace("{% url 'dashboard' %}");

document.addEventListener("alpine:init", () => {
  Alpine.data("dialog", () => ({
    password: "",
    duplicate: "",
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
  }));
});

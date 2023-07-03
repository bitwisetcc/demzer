/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      backgroundImage: {
        "background": "{% static 'core/images/BGDemzer.png' %}"
      },
      colors: {
        "color-primary": "#32659A",
        "color-primary-dimm": "#365075",
        "color-secondary": "#E6A82E",
        "color-txt-perfil": "#054499",
        "color-bg-perfil": "#F5F5F5",
        "color-boletim": "#D7D4D4",
        "color-name-boletim": "#4A73AC",
        "color-dark-orange": "#D0A661",
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}


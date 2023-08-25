/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#32659A",
        "color-primary-dimm": "#365075",
        "color-secondary": "#E6A82E",
        "color-txt-perfil": "#054499",
        "color-bg-perfil": "#F5F5F5",
        "color-boletim": "#D7D4D4",
        "color-name-boletim": "#4A73AC",
        "color-dark-orange": "#CD9028",
        "color-grey": "#EDECEC",
        "color-hover": "#E8C17E",
      }
    },
    fontFamily: {
      'glacial': ['Glacial'],
      'mono': ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "Liberation Mono", "Courier New", "monospace"],
    },
    screens: {
      'md': '768px',
      'sm': '640px',
      'md2': {'max': '767px'},
      'sm2': {'max': '375px'},
      'ultrawide': '2500px',
    },
  },
  plugins: [require("@tailwindcss/forms")],
}


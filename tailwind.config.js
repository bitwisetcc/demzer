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
        "color-secondary": "#E6A82E"
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}


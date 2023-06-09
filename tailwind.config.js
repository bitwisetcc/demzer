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
        "color-secondary": "#cd9028"
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}


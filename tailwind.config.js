/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      backgroundImage: {
        "background": "{% static 'core/images/BGDemzer.png' %}"
      },
      colors: {
        "color-primary": "#054499",
        "color-primary-dimm": "#0a3c6f",
        "color-secondary": "#E6A82E",
        "color-secondary-dimm": "#E8C17E" 
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}

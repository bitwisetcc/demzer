/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#32659A"
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}


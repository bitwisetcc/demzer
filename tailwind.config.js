/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#32659A", //Blue Color
        "color-secundary": "#E2A161", //Orange Color
        "main-color": "#E6E3E3" //Background Color
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}

